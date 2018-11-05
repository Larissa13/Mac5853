from app.models import Request, Keyword, Label

def test_db(session):
	example_req = [Request(id=0, url='www.fumorio.com', status='aguardando')]
	example_kw = [Keyword(word='narguile', vector=[0.2, 0.1, 0.0], requests=[example_req[0]])]
	example_label = [Label(name='cigarro', restrict=True, keywords=[example_kw[0]]), Label(name='permitted', restrict=False, keywords=[])]
	for example in example_label:
		session.add(example_label)
	session.commit()

	assert Request.query.filter_by(id).count() == 1
	assert Label.query.filter_by(name).count() == 2
	assert Keyword.query.filter_by(word).count() == 1
	

