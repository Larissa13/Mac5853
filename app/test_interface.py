def test_interface(testapp):
	response = testapp.get('/')
	assert response.status_code == 200
	assert b'URL' in response.data
	assert b'Submit' in response.data
	assert b'Forbidden Content Detector' in response.data
	assert b'Force Recalculation' in response.data
	assert b'keywords' in response.data

def test_interface_post(testapp):
	data = dict(url = 'http://www.google.com')
	response = testapp.post('/', data, follow_redirects=True)
	assert response.status_code == 200