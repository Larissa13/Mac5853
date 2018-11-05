from app.models  import Request, Keyword, Label

#CRUD test
def test_base(session, db):
	request = Request(id=13, url='http://www.google.com', status = 'done')
	keyword = Keyword(word='carros', requests=[request])
	label = Label(name='veículos', restrict=True, keywords = [keyword])

	db.create_all()
	db.session.add(label)
	db.session.commit()

	#test create
	assert session.query(Request).count() == 1
	assert session.query(Keyword).count() == 1
	assert session.query(Label).count() == 1

	#test read
	assert Request.query.filter_by(id = 13).first().url == "http://www.google.com"
	assert Keyword.query.filter_by(word = 'carros').first().requests[0].id == 13
	assert Label.query.filter_by(name = 'veículos').first().restrict == True 

	#test update 
	request.url = "http://www.twitch.tv"
	db.session.commit()
	assert Request.query.filter_by(id = 13).first().url == "http://www.twitch.tv"
	label.restrict = False

	assert not Label.query.filter_by(name = 'veículos').first().restrict

	#test delete
	db.session.delete(label)
	db.session.commit()

	assert Label.query.filter_by(name='veículos').first() == None
	assert Request.query.filter_by(id = 13).first().url == "http://www.twitch.tv"
	assert Keyword.query.filter_by(word = 'carros').first().requests[0].id == 13


