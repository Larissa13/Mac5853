import sys
sys.path.append('../')

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


class ConfigDev(object):
    """
    Sets app's development configuration.
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app(Config):
    """
    Creates the website's pages behavior and the app's database. Returns app object and database object.
    """
    app = Flask(__name__)

    app.config.from_object(Config)
    db = SQLAlchemy()

    app.config['DEBUG'] = True

    db.app = app
    db.init_app(app)

    sockets = Sockets(app)


    @app.route('/', methods=('GET', 'POST'))
    def index():
        """
        Creates and desplays the main page (index). Returns the rendered webpage.
        """
        status_dict = {'done':('success', '100'), 'calculating':('warning', '50'),
                       'extracting words from website':('danger', '25'),
                       'formulating answer':('info', '75'), 'wait':('', '0')}

        #TEMP VALUES
        #key = 'done'
        veredict = 'PERMITTED'
        expl_words = ['cigarro', 'tabaco', 'tragar']
        label = 'Cigarros'
        #TEMP VALUES

        url = None
        key = 'wait'
        ws_on = 'False'
        status = status_dict[key]

        if request.method == 'POST':

            if request.is_json:
                in_json = json.loads(request.get_json())
                sites = in_json['sites']
                callback = in_json['callback']
                _, _, _, key, _ = get_result(sites, True, callback=callback)

                return "calling classifier"

            else:

                url = request.form['url']
                keywords = request.form['keywords']
                force_calc = request.form.get('forcecalc') != None

                label, expl_words, veredict, key, ws_on = get_result([url], force_calc)
                status = status_dict[key]
                print("called post, websocket: " + str(ws_on))
                print(label, expl_words, veredict, key, force_calc)
        else:
            key = request.args.get('key')
            veredict = request.args.get('veredict')

            n_words = request.args.get('n_words')
            n_words = n_words if n_words is not None else 0
            expl_words = []
            for i in range(int(n_words)):
                expl_words += [request.args.get('expl_words_' + str(i))]

            label = request.args.get('label')
            url = request.args.get('url')
            status = status_dict[key] if key is not None else status_dict['wait']

            if key is not None:
                req = Request(url=url, status=key)
                db.session.add(req)
                db.session.commit()
                if key == 'done':
                    update_or_create_kws(expl_words, req, db)

                db.session.commit()

        return render_template('index.html', status=status, key=key,
                               veredict=veredict, expl_words=expl_words, label=label, ws_on=ws_on, url=url)


    @app.route('/prepare')
    def prepare():
        """
        Creates an intermediate page that prepares the classification answer to be presented. Returns an redirection to the main page.
        """
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://localhost:{PORT}'.format(PORT=ZMQ_LISTENING_PORT))
        socket.send_string('send results')
        result = socket.recv()
        data = json.loads(result.decode('utf-8'))
        print("data received from classifier: ", data)

        prepared = dict()
        prepared['veredict'] = 'RESTRICTED' if data['restrict'] else 'PERMITTED'

        for i, (word, _) in enumerate(data['reasons'][1].items()):
            prepared['expl_words_' + str(i)] = word

        n_words = len(data['reasons'][1])
        prepared['key'] = 'done'
        prepared['label'] = data['label']
        prepared['url'] = data['url']
        prepared['n_words'] = n_words

        print("number of keywords: ", n_words)
        print([prepared['expl_words_' + str(i)] for i in range(n_words)])

        return redirect(url_for("index", **prepared))


    @sockets.route('/answer')
    def send_data(ws):
        """
        Establishes a socjet connection with the server to receive status from classification and redirects to prepare page when the result is received.
        """
        print('Got a websocket connection, sending up data from zmq')
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://localhost:{PORT}'.format(PORT=ZMQ_LISTENING_PORT))
        gevent.sleep()

        while True:
            socket.send_string("send status")
            received = socket.recv()
            print("received to socket: ", received)

            data = json.loads(received.decode('utf-8'))

            ws.send(json.dumps(data))
            if data['status'] == "formulating answer" or data['status'] == 'error':
                break
            gevent.sleep()


    return app, db


app, db = create_app(ConfigDev)
logger = logging.getLogger(__name__)
context = zmq.Context()
ZMQ_LISTENING_PORT = 6557

from app.utils import *
