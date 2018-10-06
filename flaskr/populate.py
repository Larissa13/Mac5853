from app import app, db

example_req = [Request(id=0, url='www.fumorio.com', status='aguardando')]
example_kw = [Keyword(word='narguile', vector=[0.2, 0.1, 0.0], requests=[example_req[0]])]
example_label = [Label(name='cigarro', restrict=True, keywords=[example_kw[0]]), Label(name='permitted', restrict=False, keywords=[])]

with app.app_context():
    db.create_all()

for example in example_label:
    db.session.add(example)
db.session.commit()

