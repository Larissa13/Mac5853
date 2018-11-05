import unittest as ut 
from app.classifier import *
import numpy as np
from app.models import Keyword, Request, Label
import os
import pickle

class TestClassifier(ut.TestCase):
	pickle_path = 'model.pickle'
	if os.path.exists(pickle_path):
		with open(pickle_path, 'rb') as file:
			model = pickle.load(file)
	else:
		model = KeyedVectors.load_word2vec_format('wiki.pt/wiki.pt.vec')
		with open(pickle_path, 'wb') as file:
			pickle.dump(model, file)
	classifier =  Classifier(model = model)
	word = ['hahsbaja', 'casa', 'arma']

	def test_rm_unseen(self):
		self.assertEqual(self.classifier.rm_unseen(self.word), ['casa', 'arma'])

	def test_w2v_training(self):
		self.assertTrue(self.classifier.model.similarity('carro', 'caminhão') > 0.7)
		self.assertTrue(self.classifier.model.similarity('arma', 'munição') > 0.6)
		self.assertTrue(self.classifier.model.similarity('cigarro', 'fumar') > 0.65)

	def test_calc_dists(self):
		kw1 = Keyword(word = 'munição', requests=[])
		kw2 = Keyword(word = 'pistola', requests=[])
		kw3 = Keyword(word = 'espingarda', requests=[])
		self.assertTrue((self.classifier.calc_dists('arma', [kw1, kw2, kw3]) == np.array([0.677431  , 0.6866069 , 0.71047467], dtype='float32')).all())

	def test_classifier(self):

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

		kws = default_kw_armas+default_kw_cigarros+default_kw_prost+default_kw_remedio+default_kw_serv
		stat = []
		for status in self.classifier.classify(url = 'https://www.uol.com.br/', kws=kws, labels=labels):
			stat+=[status]
		self.assertEqual(stat[-1]['label'], "permitted")

if __name__ == '__main__':
    ut.main()