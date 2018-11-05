from app.models import Request, Keyword, Label
from  multiprocessing import Process
import requests
import zmq.green as zmq
from app.classifier import Classifier
from gensim.models import KeyedVectors
import json
import gevent
import pickle
import os

ZMQ_LISTENING_PORT = 6557
print("loading w2v")
pickle_path = 'model.pickle'

if os.path.exists(pickle_path):
    with open(pickle_path, 'rb') as file:
        model = pickle.load(file)
else:
    model = KeyedVectors.load_word2vec_format('wiki.pt/wiki.pt.vec')
    with open(pickle_path, 'wb') as file:
        pickle.dump(model, file)

print("finished loading")


def search_db(url):
    return Request.query.filter_by(url=url).first()


def result_from_db(req):
    if req.keywords:
        label = req.keywords[0].label.name
        expl_words = [kw.word for kw in req.keywords]
        veredict = 'RESTRICTED'
    else:
        label, expl_words = None, None
        veredict = 'PERMITTED'

    return label, expl_words, veredict


def get_result(urls, force_calc, callback=None):

    if not force_calc:
        last_calc = search_db(urls[0])
        if last_calc is not None:
            return (*result_from_db(last_calc), 'done', 'False')

    Process(target=call_cls, args=(urls, callback, Keyword.query.all(), Label.query.all())).start()
    return None, None, None, 'calculating', 'True'


def update_or_create_kws(words, req, db):
    print("updating keywords: ", words)
    if words is None: return
    for word in words:
        kw = Keyword.query.filter_by(word=word).first()
        if kw is None:
            kw = Keyword(word=word, requests=[req])
            db.session.add(kw)
        else:
            kw.requests.append(req)

        db.session.commit()


def call_cls(urls, callback, kws, labels):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:{PORT}'.format(PORT=ZMQ_LISTENING_PORT))
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    print("calling classifier")

    msg = None
    while msg is None:
        socks = dict(poller.poll())
        if socket in socks:
            msg = socket.recv()

    print("callback: ", callback)
    cls = Classifier(model=model)
    results = dict()
    if callback is None:
        url = urls[0]
        for status in cls.classify(url, kws, labels):
            print("status:", status)
            if type(status) == str:
                socket.send_string(json.dumps({'status':status}))
                if status == 'error':
                    break
                gevent.sleep(0.1)
                msg = socket.recv()
            else:
                socket.send_string(json.dumps(status))
    else:
        results = []
        for url in urls:
            for status in cls.classify(url, kws, labels):
                if type(status) == str:
                    data = json.dumps({'status':status + " in url " + url})
                    request.post(callback, json=data)
                    if status == 'error':
                        results += [{'url':url,
                                     'restrict':False,
                                     'reasons':['error']}]
                        break
                else:
                    results += [status]

        #TODO call update db
        data = json.dumps({'sites':results})
        request.post(callback, json=data)
