from app import app, db
from app.models import Request, Keyword, Label
default_req = [Request(id = 0, url = ' ', status = 'done')] 

default_req = [Request(id = 0, url = ' ', status = 'done')] 

default_kw_armas = [Keyword(word='arma', requests=[default_req[0]]), Keyword(word='munição', requests=[default_req[0]]), Keyword(word='calibre', requests=[default_req[0]]),
					 Keyword(word='revólver', requests=[default_req[0]]), Keyword(word='cano', requests=[default_req[0]]), Keyword(word='carabina', requests=[default_req[0]]), 
					 Keyword(word='espingarda', requests=[default_req[0]])]

default_kw_cigarros = [Keyword(word='cigarro', requests=[default_req[0]]), Keyword(word='vape', requests=[default_req[0]]), Keyword(word='narguile', requests=[default_req[0]]),
					   Keyword(word='fumar', requests=[default_req[0]]), Keyword(word='tragar', requests=[default_req[0]]), Keyword(word='tabaco', requests=[default_req[0]]), 
					   Keyword(word='nicotina', requests=[default_req[0]]), Keyword(word='vaporizador', requests=[default_req[0]]), Keyword(word='ervas', requests=[default_req[0]])]

default_kw_prost = [Keyword(word='sexo', requests=[default_req[0]]), Keyword(word='prostituta', requests=[default_req[0]]), Keyword(word='fetiche', requests=[default_req[0]]), 
					Keyword(word='cache', requests=[default_req[0]]), Keyword(word='acompanhante', requests=[default_req[0]]), Keyword(word='programa', requests=[default_req[0]]),
					Keyword(word='seios', requests=[default_req[0]]), Keyword(word='bunda', requests=[default_req[0]]), Keyword(word='travesti', requests=[default_req[0]]),
					Keyword(word='gostosa', requests=[default_req[0]])]

default_kw_remedio = [Keyword(word='remédio', requests=[default_req[0]]), Keyword(word='aborto', requests=[default_req[0]]), Keyword(word='comprimido', requests=[default_req[0]]), 
					  Keyword(word='secundários', requests=[default_req[0]]), Keyword(word='efeitos', requests=[default_req[0]])]

default_kw_serv = [Keyword(word='operadora', requests=[default_req[0]]), Keyword(word='cabo', requests=[default_req[0]]), Keyword(word='assinatura', requests=[default_req[0]]), 
				   Keyword(word='liberação', requests=[default_req[0]]), Keyword(word='sem', requests=[default_req[0]]), Keyword(word='aparelhos', requests=[default_req[0]]),
				   Keyword(word='net', requests=[default_req[0]]), Keyword(word='vivo', requests=[default_req[0]])]

labels = [Label(name='Armas de fogo', restrict=True, keywords=default_kw_armas), Label(name = 'Cigarros', restrict=True, keywords=default_kw_cigarros),
		Label(name='Prostutuição', restrict=True, keywords=default_kw_prost), Label(name='Remédios', restrict=True, keywords=default_kw_remedio),

		Label(name='Serviços ilegais', restrict=True, keywords=default_kw_serv), Label(name='Site permitido', restrict=False, keywords=[])]

with app.app_context():
    db.create_all()

for label in labels:
	db.session.add(label)
db.session.commit()

