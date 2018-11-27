[nltk_data] Downloading package stopwords to
[nltk_data]     /home/larissa/nltk_data...
[nltk_data]   Package stopwords is already up-to-date!
[nltk_data] Downloading package rslp to /home/larissa/nltk_data...
[nltk_data]   Package rslp is already up-to-date!
[nltk_data] Downloading package punkt to /home/larissa/nltk_data...
[nltk_data]   Package punkt is already up-to-date!
loading w2v
finished loading
# classifier

## Classifier
```python
Classifier(self, model=None)
```

A classifier based on calculation of distances between words. It can classify the text in forbidden/restrict (ie. 'armas', 'cigarro', 'prostituição', 'remédios', serviços) or permitted classes.


__Attributes:__

model (KeyedVector object, None): a word2vec trained from wikipedia(portuguese) model.
             Otherwise, if it is 'None', the model will be trained in the initialization of the classifier.
             Default value: None
status (str): indicates the text's level of processinf during classification.

### calc_dists
```python
Classifier.calc_dists(self, word, kws)
```

Calculates the distance between a word and a list of words based on the similarity of their word2vec representation.

__Input:__

    -word (str): The word that will be compared (based on similarity) to a list of keywords.
    -kws (list): List of Keywords.

__Output:__

    -dists (list): a list of distances (float) calculated between the word and each keyword in kws.

### check_in_vocab
```python
Classifier.check_in_vocab(self, word)
```

Checks whether a word is in the vocabulary of the model or not.

__Input:__

    -word (str): the word to be verified.

#Output:
    -boolean valeu indicating if the word is part of the model's vocabulary.

### rm_unseen
```python
Classifier.rm_unseen(self, words)
```

Given a list of words, returns a list of those that are part of the model's vocabulary.

__Input:__

    - words (list): A list of strings.

__Output:__

    - list of strings of word that are present in the model`s vocabulary.

### prepare_result
```python
Classifier.prepare_result(self, result, url, thresh, kw_result)
```

Prepares the answer structure to be displayed in the website for the user.

__Input:__

    -result (dict):
    -url (str):
    -thresh (float):
    -kw_result (dict):

#Output:
    -answer (dict):

### classify
```python
Classifier.classify(self, url, kws, labels, dist_thresh=0.2, kws_thresh=0.49)
```

Classifies a url based on the word2vec  similarity of words extracted from its html content. The result is the output of the prepare_result function.

__Input:__

    -url (str): a url string.
    -kws (list): a list of Keywords from Keyword database.
    -labels (list): a list od Labels from Label database.

*Optional:*
    -dist_thresh (float, 0.20):
    -kws_thresh (float, 0.49):


