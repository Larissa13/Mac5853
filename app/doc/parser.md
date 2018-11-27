[nltk_data] Downloading package stopwords to
[nltk_data]     /home/larissa/nltk_data...
[nltk_data]   Package stopwords is already up-to-date!
[nltk_data] Downloading package rslp to /home/larissa/nltk_data...
[nltk_data]   Package rslp is already up-to-date!
[nltk_data] Downloading package punkt to /home/larissa/nltk_data...
[nltk_data]   Package punkt is already up-to-date!
# parser

## tokenize_text
```python
tokenize_text(sentences)
```

Receives a list of sentences, ie. a sequence of words and returns a  tokenized version of it.

## remove_stopwords
```python
remove_stopwords(text)
```

Receives a list of strings and returns a version of it without stopwords.

__Input:__

    - text (list): a list of words (strings).

__Output:__

    - new_text (list): returns a list of words without portuguese stopwords.

## remove_punctuation
```python
remove_punctuation(text)
```

Receives a list of strings and returns a version of it without punctuation.

__Input:__

    - text (list): a list of words (strings).

__Output:__

    - new_text (list): a list of words without punctuation.

## stemming
```python
stemming(text)
```

Receives a list of strings and returns a list containing the stemmed version of them.

__Input:__

    - text (list): a list of words (strings).

__Output:__

    - new_text (list): list of string containing stemmed words.

## lowercase
```python
lowercase(text)
```

Receives a list of strings and returns a list with the corresponding lowercase version of these strings.

__Input:__

    - text (list): a list of words (strings).

__Output:__

    - new_text (list): a list of strings with only lowercase characters.

## lemmatization
```python
lemmatization(text)
```

Receives a list of strings and returns a list with the lemmatized version of the verbs contained in the input.

__Input:__

    - text (list): list of words (strings).

__Output:__

    - new_text (list): list of words with verbs lemmatized (if there is any).

## Parser
```python
Parser(self, /, *args, **kwargs)
```

A parser to deal extract text from a url's html, tokenize the text and process it though operations such as stopword and punctuation removal, stemming, lemmatization and lowercase.

### extract
```python
Parser.extract(self, url)
```

Extract text from a url's html using BeautifulSoup Module. The output is a BeautifulSoup object.

__Input:__

    - url (str): a url string.

__Output:__

    -soup (beautifulSoup object): A nested data structure containing the url's hmtl elements and content.

### text_from_web
```python
Parser.text_from_web(self, url)
```

Extract text from url's html and returns a list of the strings present on it.

__Input:__

    - url (str): a url string.

__Output:__

    -text (list): a list ofstrings extracted from the url's html.

### crawler
```python
Parser.crawler(self, url, limit=10)
```

Receives a url and returns a list of links (another urls)  present on its html.

__Input:__

    - url (str): a url string.
    - limit (int, 10): a int number, referring to the maximum of links to return. Default value: 10.

__Output:__

    - links (list): a list of links found on the url's html.

### parse
```python
Parser.parse(self, url)
```

Receives a url and returns a list of strings extracted from its html already preprocessed (see Parse.preprocess for more information).

__Input:__

    - url (str): a url string.

__Output:__

    - a list of strings that were extracted from the given url's html and that were processed in order to be lowercase, without stopwords and punctuation.

### preprocess
```python
Parser.preprocess(self, text, use_stem=False, use_lemma=False)
```

Receives a list of strings and returns a list os strings in lowercase, with punctuation and stopwords removed.
Optionally, the words are also lemmatized and stemmed.

__Input:__

    - text (list): a list of words (strings).

*Optional:*

    - use_stem (boolean, False): True, if it is to perform stemming in the strings. Default value: False.
    - use_lemma (boolean, False): True, if it is to perform lemmatization in the strings. Default value: False.

__Output :__

    - text (list): list of words with all strings in the lowercase version and also with punctuation and stopwords removed. (Optionally, the strings may also be stemmed and lemmatized).

