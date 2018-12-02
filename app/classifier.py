import sys
sys.path.append('../')
from gensim.models import KeyedVectors
from app.parser import Parser
import numpy as np
import pandas as pd



class Classifier:
    """
        A classifier based on calculation of distances between words. It can classify the text in forbidden/restrict (ie. 'armas', 'cigarro', 'prostituição', 'remédios', serviços) or permitted classes.


        # Attributes:
        model (KeyedVector object, None): a word2vec trained from wikipedia(portuguese) model. 
                     Otherwise, if it is 'None', the model will be trained in the initialization of the classifier.
                     Default value: None
        status (str): indicates the text's level of processinf during classification.
    """
    def __init__(self, model=None):
        self.parser = Parser()
        if model is None:
            #TODO download if inexistent
            self.model = KeyedVectors.load_word2vec_format('wiki.pt/wiki.pt.vec')

        else:
            self.model = model

        self.status = "extracting words from website"

    def calc_dists(self, word, kws):
        """
        Calculates the distance between a word and a list of words based on the similarity of their word2vec representation.

        # Input:
            - word (str): The word that will be compared (based on similarity) to a list of keywords.
            - kws (list): List of Keywords.

        # Output:
            - dists (list): a list of distances (float) calculated between the word and each keyword in kws.
        """
        dists = []
        for kw in kws:
            dists += [self.model.similarity(word, kw.word)]

        return np.array(dists)


    def check_in_vocab(self, word):
        """
        Checks whether a word is in the vocabulary of the model or not.

        # Input:
            - word (str): the word to be verified.

        #Output:
            - boolean valeu indicating if the word is part of the model's vocabulary.
        """
        if type(word) == str:
            return word in self.model.wv.vocab
        else:
            return word.word in self.model.wv.vocab


    def rm_unseen(self, words):
        """
        Given a list of words, returns a list of those that are part of the model's vocabulary. 

        # Input:
            - words (list): A list of strings.
        
        # Output:
            - list of strings of word that are present in the model`s vocabulary.
        """

        return [word for word in words if self.check_in_vocab(word)]


    def prepare_result(self, result, url, thresh, kw_result):
        """
        Prepares the answer structure to be displayed in the website for the user.

        # Input:
            - result (dict): maps from label to veredict. 
            - url (str): an url string.
            - thresh (float): minimum similarity for a keyword to be considered present in the content.
            - kw_result (dict): maps from label name to a pandas` series which maps from keywords to similarity

        #Output:
            - answer (dict): contains url, the classification, the reasons (keywords and label).
        """
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
        """
        Classifies an url based on the word2vec  similarity of words extracted from its html content. The result is the output of the prepare_result function.

        # Input:
            - url (str): an url string.
            - kws (list): a list of Keywords from Keyword database.
            - labels (list): a list od Labels from Label database.

        *Optional:*
            - dist_thresh (float, 0.20): minimum similarity for a label to be considered present in the content.
            - kws_thresh (float, 0.49): minimum similarity for a keyword to be considered present in the content.

        """
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

