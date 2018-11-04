from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def create_app():
    pass

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


def get_result(url, force_calc, callback=None):

    last_calc = search_db(url)

    if not force_calc and last_calc is not None:
        return result_from_db(last_calc), 'done'
    else:
        #call classifier
        print(url, keywords, force_calc, callback)
        return None, None, None, 'calculating'


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

    status = status_dict[key]

    if request.method == 'POST':

        if request.is_json:
            in_json = request.get_json(force=True)
            sites = in_json['sites']
            callback = in_json['callback']
            results = []
            for url in sites:
                _, _, _, key = get_result(url, True, callback=callback)

            #ans = {"sites":[{"url":url, "restrict":(label is not None), "reasons":expl_words} for url, label, expl_words, veredict, _ in results]}
            #ta errado, algumas urls podem ja existir e outras nao. Force calc em todas??

        else:

            url = request.form['url']
            keywords = request.form['keywords']
            force_calc = request.form.get('forcecalc')
            if force_calc is None: force_calc = False

            label, expl_words, veredict, key = get_results(url, force_calc)

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
                           veredict=veredict, expl_words=expl_words, label=label)



import requests

def answer(callback, result):
    if callback is not None:
        requests.post(callback, json=result)
    else:
        
        return redirect(url_for("index"), **result)




