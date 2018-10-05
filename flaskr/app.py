from flask import Flask
from models import db, Request, Keyword, Label
from datetime import datetime

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'forbidden_db',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


example_req = [Request(id=0, url='www.fumorio.com', status='aguardando')]
example_kw = [Keyword(word='narguile', vector=[0.2, 0.1, 0.0], requests=[example_req[0]])]
example_label = [Label(name='cigarro', restrict=True, keywords=[example_kw[0]]), Label(name='permitted', restrict=False, keywords=[])]

db.app = app
db.init_app(app)

with app.app_context():
    db.create_all()

for example in example_label:
    db.session.add(example)
db.session.commit()


