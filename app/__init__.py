import json
import gevent
from flask_sockets import Sockets
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging
import zmq.green as zmq
import os
import json


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def create_app():


    app = Flask(__name__)

    app.config.from_object(Config)
    db = SQLAlchemy()

    app.config['DEBUG'] = True
    
    db.app = app
    db.init_app(app)

    sockets = Sockets(app)
    @app.route('/', methods=('GET', 'POST'))
    def index():
        status_dict = {'done':('success', '100'), 'calculating':('warning', '50'),
                       'extracting words from website':('danger', '25'),
                       'formulating answer':('info', '75'), 'wait':('', '0')}

        #TEMP VALUES
        #key = 'done'
        veredict = 'PERMITTED'
        expl_words = ['cigarro', 'tabaco', 'tragar']
        label = 'Cigarros'
        #TEMP VALUES

        key = 'wait'
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

                label, expl_words, veredict, key, ws_on = get_result([url], force_calc)
                logger.info("called post, websocket: " + str(ws_on))
                print("called post, websocket: " + str(ws_on))
        else:
            key = request.args.get('key')
            veredict = request.args.get('veredict')
            expl_words = request.args.get('expl_words')
            label = request.args.get('label')
            url = request.args.get('url')

            status = status_dict[key] if key is not None else status_dict['wait']

            if key is not None:
                req = Request(url=url, status=status)
                db.session.add(req)

                if key == 'done':
                    update_or_create_kws(expl_words, req)

                db.session.commit()

        return render_template('index.html', status=status, key=key,
                               veredict=veredict, expl_words=expl_words, label=label, ws_on=ws_on)


    @app.route('/prepare')
    def prepare():
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://localhost:{PORT}'.format(PORT=ZMQ_LISTENING_PORT))
        socket.send_string('send results')
        result = socket.recv()
        data = json.loads(result.decode('utf-8'))
        logger.info(data)

        prepared = dict()
        prepared['veredict'] = 'RESTRICTED' if data['restrict'] else 'PERMITTED'
        prepared['expl_word'] = [word for word, _ in data[reasons][1].items()]
        prepared['key'] = 'done'
        prepared['label'] = data['label']
        prepared['url'] = data['url']

        return redirect(url_for("index"), **prepared)

    @sockets.route('/answer')
    def send_data(ws):
        print('Got a websocket connection, sending up data from zmq')
        logger.info('Got a websocket connection, sending up data from zmq')
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://localhost:{PORT}'.format(PORT=ZMQ_LISTENING_PORT))
        
        gevent.sleep()

        while True:
            socket.send_string("send status")
            received = socket.recv()
            print("received to socket: ", received)
            data = json.loads(received.decode('utf-8'))
            logger.info(data)
            ws.send(json.dumps(data))
            if data['status'] == "formulating answer":
                break
            gevent.sleep()


    return app, db


app, db = create_app()
logger = logging.getLogger(__name__)
context = zmq.Context()
ZMQ_LISTENING_PORT = 6557

from app.utils import *


