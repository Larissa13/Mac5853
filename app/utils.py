from app.models import Request, Keyword, Label
from  multiprocessing import Process
import requests


def answer(callback, result):
    requests.post(callback, json=result)


def search_db(url):
    return Request.query.filter_by(url=url).first()


def result_from_db(req):
    if req.keywords:
        label = req.keywords[0].name
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
            return result_from_db(last_calc), 'done', 'False'

    Process(target=call_cls, args=(urls, callback, Keyword.query.all(), Label.query.all())).start()
    return None, None, None, 'calculating', 'True'


def update_or_create_kws(words, req):
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

    msg = socket.recv()
    cls = Classifier()
    results = dict()

    if callback is None:
        url = urls[0]
        for status in cls.classify(url, kws, labels):
            if type(status) == str:
                socket.send_string(json.dumps({'status':status}))
                gevent.sleep(0.1)
                msg = socket.recv()
            else:
                socket.send_string(json.dumps(status))
    else:
        pass #TODO
