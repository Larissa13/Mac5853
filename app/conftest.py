
from testing.postgresql import Postgresql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import app, create_app
from app import db as _db
import pytest

class TestConfig(object):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = 'test'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    

@pytest.yield_fixture(scope='session')
def app():
    _app = Flask(__name__)

    db = SQLAlchemy()
    _app.config['DEBUG'] = True
    _app.config['TESTING'] = True
    _app.config['ENV'] = 'test'
    with Postgresql() as postgresql:
        _app.config['SQLALCHEMY_DATABASE_URI'] = postgresql.url()
        _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        ctx = _app.app_context()
        ctx.push()

        db._app = _app
        db.init_app(_app)

        yield _app

        ctx.pop()


@pytest.fixture(scope='module')
def testapp():
    flask_app, db = create_app(TestConfig)
    test_client = flask_app.test_client()
   
    ctx = flask_app.app_context()
    ctx.push()
    yield test_client
    ctx.pop()


@pytest.yield_fixture(scope='session')
def db(app):
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)

    db.session = session_

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()