from sqlalchemy.types import ARRAY
from datetime import datetime
from app import db


request_keyword = db.Table('request_keyword',
                           db.Column('keyword_word', db.String(50), db.ForeignKey('keyword.word')),
                           db.Column('request_id', db.Integer, db.ForeignKey('request.id')))


class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(50), nullable=False)


class Keyword(db.Model):
    __tablename__ = 'keyword'
    word = db.Column(db.String(50), primary_key=True)
    #vector = db.Column(ARRAY(db.Float), nullable=False)

    label_name = db.Column(db.String(50), db.ForeignKey('label.name'))
    requests = db.relationship(Request, backref='keywords', secondary=request_keyword)



class Label(db.Model):
    __tablename__ = 'label'
    name = db.Column(db.String(50), primary_key=True)
    restrict = db.Column(db.Boolean, nullable=False)
    keywords = db.relationship(Keyword, backref='label', lazy=True)
