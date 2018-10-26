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
    print("ola")
    if request.method == 'POST':
        print("hey asas")
        url = request.form['url']
        keywords = request.form['keywords']
        force_calc = request.form.get('question')

        print(url, keywords, force_calc)

    return render_template('index.html')

