from flask import Flask, render_template, request
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

@app.route('/', methods=('GET', 'POST'))
def index():
    status_dict = {'done':('success', '100'), 'calculating':('warning', '50'),
                   'allocating worker':('danger', '25'), 'formulating answer':('info', '75')}

    #TEMP VALUES
    key = 'done'
    status = status_dict[key]
    veredict = 'PERMITTED'
    expl_words = ['cigarro', 'tabaco', 'tragar']
    label = 'Cigarros'
    #TEMP VALUES

    print("ola")
    if request.method == 'POST':
        print("hey fat cats")
        url = request.form['url']
        keywords = request.form['keywords']
        force_calc = request.form.get('forcecalc')

        print(url, keywords, force_calc)

    return render_template('index.html', status=status, key=key,
                           veredict=veredict, expl_words=expl_words, label=label)

