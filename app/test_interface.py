from app.models import Request, Keyword, Label


def test_interface(testapp):
	response = testapp.get('/')
	assert response.status_code == 200
	assert b'URL' in response.data
	assert b'Submit' in response.data
	assert b'Forbidden Content Detector' in response.data
	assert b'Force Recalculation' in response.data
	assert b'Type an URL and press Submit.' in response.data
	assert b'A Machine Learning model will analyse the website and classify it\'s content' in response.data



'''def test_interface_post(testapp, session, db):
	request = Request(id=13, url='http://www.google.com', status = 'done')
	keyword = Keyword(word='carros', requests=[request])
	label = Label(name='veículos', restrict=True, keywords = [keyword])

	db.create_all()
	db.session.add(label)
	db.session.commit()
	data = {'url' : 'http://www.google.com'}
	response = testapp.post('/', data = data)

	assert response.status_code == 200'''


