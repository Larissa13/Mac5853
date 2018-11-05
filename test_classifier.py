import unittest as ut 
from classifier import *
import numpy as np
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
		self.assertTrue((self.classifier.calc_dists('arma', ['munição', 'pistola', 'espingarda']) == np.array([0.677431  , 0.6866069 , 0.71047467], dtype='float32')).all())


if __name__ == '__main__':
    ut.main()