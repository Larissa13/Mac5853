from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'forbidden_db',
    'host': 'localhost',
    'port': '5432',
}

db = SQLAlchemy()

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.app = app
db.init_app(app)



from app.models import Request, Keyword, Label


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

    last_calc = search_db(url)

    if not force_calc and last_calc is not None:
        return result_from_db(last_calc), 'done', 'False'
    else:
        Process(target=call_cls, args=(urls, callback)).start()
        return None, None, None, 'calculating', 'True'


def update_or_create_kws(words, vecs, req):
    for word, vec in zip(words, vecs):
        kw = Keyword.query.filter_by(word=word).first()
        if kw is None:
            kw = Keyword(word=word, vector=vec, requests=[req])
            db.session.add(kw)
        else:
            kw.requests.append(req)

        db.session.commit()


@app.route('/', methods=('GET', 'POST'))
def index():
    status_dict = {'done':('success', '100'), 'calculating':('warning', '50'),
                   'allocating worker':('danger', '25'), 'formulating answer':('info', '75')}

    #TEMP VALUES
    key = 'done'
    veredict = 'PERMITTED'
    expl_words = ['cigarro', 'tabaco', 'tragar']
    label = 'Cigarros'
    #TEMP VALUES


    ws_on = 'False'
    status = status_dict[key]

    if request.method == 'POST':

        if request.is_json:
            in_json = request.get_json(force=True)
            sites = in_json['sites']
            callback = in_json['callback']
            _, _, _, key, _ = get_result(sites, True, callback=callback)

            #TODO answer with status
        else:

            url = request.form['url']
            keywords = request.form['keywords']
            force_calc = request.form.get('forcecalc')
            if force_calc is None: force_calc = False

            label, expl_words, veredict, key, ws_on = get_results([url], force_calc)

    else:
        key = request.args.get('key')
        veredict = request.args.get('veredict')
        expl_words = request.args.get('expl_words')
        word_vecs = request.args.get('word_vecs')
        label = request.args.get('label')
        url = request.args.get('url')

        status = status_dict[key]
        req = Request(url=url, status=status)
        db.session.add(req)

        if key == 'done':
            update_or_create_kws(expl_words, word_vecs, req)

        db.session.commit()

    return render_template('index.html', status=status, key=key,
                           veredict=veredict, expl_words=expl_words, label=label, ws_on=ws_on)



ZMQ_LISTENING_PORT = 6557
sockets = Sockets(app)
context = zmq.Context()


@app.route('/prepare')
def prepare():
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://localhost:{PORT}'.format(PORT=ZMQ_LISTENING_PORT))
    socket.send_string('send results')
    results = socket.recv()
    print(results)

    return redirect(url_for("index"), **result)

@sockets.route('/answer')
def send_data(ws):
    logger.info('Got a websocket connection, sending up data from zmq')
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://localhost:{PORT}'.format(PORT=ZMQ_LISTENING_PORT))
    gevent.sleep()

    while True:
        socket.send_string("send status")
        received = socket.recv()
        data = json.loads(received.decode('utf-8'))
        logger.info(data)
        ws.send(received)
        gevent.sleep()



from  multiprocessing import Process


def call_cls(urls, callback=None):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:{PORT}'.format(PORT=ZMQ_LISTENING_PORT))

    #for i in range(5):
    #    a = socket.recv()
    #    print(a)
    #    print(i)
    #    socket.send_string(json.dumps(dict(i=i))) 
    #    gevent.sleep(1)




import requests

def answer(callback, result):
    if callback is not None:
        requests.post(callback, json=result)
    else:
        
        return redirect(url_for("index"), **result)



if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.start()

