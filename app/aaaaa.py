from app.models import Request, Keyword, Label
from app import app, db
from datetime import datetime

def test_models():
	new_request = Request(id=13, url='https://www.google.com', status='aguardando')
	new_keyword = Keyword(word= 'teste', vector=[0.13, 0.9, 0.0], requests=[new_request])
	new_label = Label(name='armas', restrict=True, keywords=[new_keyword])

	assert new_request.id == 13
	assert new_request.url == 'https://www.google.com'
	assert new_request.status == 'aguardando'

	assert new_keyword.word == 'teste'
	assert new_keyword.vector == [0.13, 0.9, 0.0]

	assert new_label.name == 'armas'
	assert new_label.restrict == True
