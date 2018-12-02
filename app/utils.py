import sys
sys.path.append('../')
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
    """
    Searches the Request table for the entry that correponds to a given url and returns it.

    # Input:
        - url (str): an url string.

    # Output:
        - the Request table entry corresponding to this url. 
    """
    return Request.query.filter_by(url=url).first()


def result_from_db(req):
    """
    Returns the Keywords and the Label associated with a request if it was previously classified as Restricted. 
    Otherwise, returns that the request was classified as Permitted, with no Keywords and Label associated.

    # Input:
        - req (Request): a Request entry from Request database.
    """
    if req.keywords:
        label = req.keywords[0].label.name
        expl_words = [kw.word for kw in req.keywords]
        veredict = 'RESTRICTED'
    else:
        label, expl_words = None, None
        veredict = 'PERMITTED'

    return label, expl_words, veredict


def get_result(urls, force_calc, callback=None):
    """
    Returns a tuple containing the urls' labels, the keywords highly correlated to the website's content, the veredict provided by the classification, the process' status, and a boolean indicating if a socket connection should be established with the client.

    # Input:
        - urls (list): list of urls strings to classify.
        - force_calc (boolean): indicates if the veredict from a previous classification should be used (force_calc=False) or not (force_calc=True).
        - callback (str, None): a callback url. 

    """
    if not force_calc:
        last_calc = search_db(urls[0])
        if last_calc is not None:
            return (*result_from_db(last_calc), 'done', 'False')

    Process(target=call_cls, args=(urls, callback, Keyword.query.all(), Label.query.all())).start()
    return None, None, None, 'wait', 'True'


def update_or_create_kws(words, req, db):
    """
    Creates or updates the keywords in the Keyword table.

    # Input:
        - words (list): a list of strings to be inserted or modified in the Keyword table.
        - req (Request): a Request to be associated with the words.
        - db (database): The app`s database.
    """
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
    """
    Provides the communication of the status and results between the classifier process, the main process and the client (when using via web interface).
    
    # Input:
        - urls (list): a list of urls to be classified.
        - callback(str): the callback url.
        - kws (list): list of pre-defined keywords in the database.
        - labels (list): list of pre-defined labels in the database.
    """
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:{PORT}'.format(PORT=ZMQ_LISTENING_PORT))
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    print("calling classifier")


    msg = None
    while msg is None and callback is None:
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
                socket.send_string(json.dumps({'status':status, 'url':url}))
                if status == 'error':
                    break
                gevent.sleep(0.1)
                msg = socket.recv()
            else:
                socket.send_string(json.dumps(status))
    else:
        print("calculating for direct post")
        results = []
        for url in urls:
            for status in cls.classify(url, kws, labels):
                if type(status) == str:
                    data = json.dumps({'status':status + " in url " + url})
                    print("sending status to callback")
                    requests.post(callback, json=data)
                    if status == 'error':
                        results += [{'url':url,
                                     'restrict':False,
                                     'reasons':['error']}]
                        break
                else:
                    results += [status]

        #TODO call update db
        data = json.dumps({'sites':results})
        print("sending results to callback")
        requests.post(callback, json=data)
    sys.exit()
