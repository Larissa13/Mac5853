import unittest as ut 
from classifier import *
import numpy as np

class TestClassifier(ut.TestCase):
	classifier =  Classifier()
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