from gensim.models import KeyedVectors
from app.parser import Parser
import numpy as np
import pandas as pd


class Classifier:

    def __init__(self, model=None):
        self.parser = Parser()
        if model is None:
            #TODO download if inexistent
            self.model = KeyedVectors.load_word2vec_format('wiki.pt/wiki.pt.vec')

        else:
            self.model = model
        self.status = "extracting words from website"


    def calc_dists(self, word, kws):
        dists = []
        for kw in kws:
            dists += [self.model.similarity(word, kw.word)]

        return np.array(dists)


    def check_in_vocab(self, word):
        if type(word) == str:
            return word in self.model.wv.vocab
        else:
            return word.word in self.model.wv.vocab


    def rm_unseen(self, words):
        return [word for word in words if self.check_in_vocab(word)]


    def prepare_result(self, result, url, thresh, kw_result):
        answer = dict()
        answer['url'] = url
        max_res = (None, thresh)
        for label, res in result.items():
            if res > max_res[1]:
                max_res = (label, res)

        restrict = max_res[0] is not None
        permit_ans = "not very correlated to any restrict categories"

        answer['restrict'] = restrict

        reason = "highly correlated to " + max_res[0].name if restrict else permit_ans
        other_reason = kw_result[max_res[0].name].to_dict() if restrict else dict()
        other_reason = {key.word:value for key, value in other_reason.items()}
        answer['reasons'] = [reason, other_reason if restrict else dict()]
        answer['label'] = max_res[0].name if restrict else 'permitted'

        return answer


    def classify(self, url, kws, labels, dist_thresh=0.20, kws_thresh=0.49):
        kws = self.rm_unseen(kws)

        yield self.status
        words = self.parser.parse(url)

        if len(words) == 0 or len(words) == 1 and words[0] == "":
            yield "error"
            return

        words = self.rm_unseen(words)
        for label in labels:
            label.keywords = self.rm_unseen(label.keywords)

        self.status = "calculating"
        yield self.status
        dists = []
        for word in words:
            dists += [self.calc_dists(word, kws)]

        dists = np.array(dists)

        df = pd.DataFrame(dists, columns=kws)

        result = dict()
        key_results = dict()
        for label in labels:
            key_mean = df[label.keywords].mean(axis=0)
            key_results[label.name] = key_mean
            result[label] = (key_mean > dist_thresh).mean()

        self.status = "formulating answer"
        yield self.status

        yield self.prepare_result(result, url, kws_thresh, key_results)

