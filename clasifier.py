
from gensim.models import KeyedVectors
from parser import Parser
import numpy as np
import pandas as pd


class Classifier:

    def __init__(self, model=None):
        self.parser = Parser()
        if model is None:
            self.model = KeyedVectors.load_word2vec_format('wiki.pt/wiki.pt.vec')
        else:
            self.model = model


    def calc_dists(self, word, kws):
        dists = []
        for kw in kws:
            dists += [self.model.similarity(word, kw)]

        return np.array(dists)


    def rm_unseen(self, words):
        return [word for word in words if word in self.model.wv.vocab]


    def classify(self, url, kws, labels, dist_thresh=0.20, kws_thresh=0.5):
        kws = self.rm_unseen(kws)
        words = self.parser.parse(url)
        words = self.rm_unseen(words)
        for label in labels:
            label.keywords = self.rm_unseen(label.keywords)
        dists = []
        for word in words:
            dists += [self.calc_dists(word, kws)]

        dists = np.array(dists)

        df = pd.DataFrame(dists, columns=kws)

        result = dict()
        for label in labels:
            print(df[label.keywords].mean(axis=0))
            print(label.name, (df[label.keywords].mean(axis=0) > dist_thresh).mean())
            result[label.name] = (df[label.keywords].mean(axis=0) > dist_thresh).mean() > kws_thresh

        return result
