import nltk
nltk.download('stopwords')
nltk.download('rslp')
nltk.download('punkt')

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk import tokenize
import spacy
import string, re


def tokenize_text(sentences):
    """
    Receives a list of sentences, ie. a sequence of words and returns a  tokenized version of it.
    """
    words = [tokenize.word_tokenize(sent, language='portuguese') for sent in sentences]
    words = sum(words, [])

    return words


def remove_stopwords(text):
    """
    Receives a list of strings and returns a version of it without stopwords.
   
    # Input:
        - text (list): a list of words (strings).
   
    # Output: 
        - new_text (list): returns a list of words without portuguese stopwords.
    """
    new_text = []
    stop_words = set(stopwords.words('portuguese'))
    for word in text:
        if word not in stop_words:
            new_text += [word]

    return new_text


def remove_punctuation(text):
    """
    Receives a list of strings and returns a version of it without punctuation.
    
    # Input:
        - text (list): a list of words (strings).
    
    # Output: 
        - new_text (list): a list of words without punctuation.
    """
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    new_text = [regex.sub('', word) for word in text]

    return new_text


def stemming(text):
    """
    Receives a list of strings and returns a list containing the stemmed version of them.
   
    # Input:
        - text (list): a list of words (strings).
    
    # Output: 
        - new_text (list): list of string containing stemmed words.
    """
    text = [word for word in text if word != ""]
    stemmer = RSLPStemmer()
    new_text = [stemmer.stem(word) for word in text]

    return new_text


def lowercase(text):
    """
    Receives a list of strings and returns a list with the corresponding lowercase version of these strings.
    
    # Input:
        - text (list): a list of words (strings).
    
    # Output:
        - new_text (list): a list of strings with only lowercase characters.
    """

    new_text = [word.lower() for word in text]

    return new_text


def lemmatization(text):
    """
    Receives a list of strings and returns a list with the lemmatized version of the verbs contained in the input.
    
    # Input:
        - text (list): list of words (strings).
    
    # Output:
        - new_text (list): list of words with verbs lemmatized (if there is any).
    """

    nlp = spacy.load('pt')
    new_text = []
    for word in text:
        token = nlp(word)[0]
        if token.pos_ == 'VERB':
            new_text += [token.lemma_ ]
        else:
            new_text +=[word]
    return new_text


class Parser:
    """
        A parser to deal extract text from a url's html, tokenize the text and process it though operations such as stopword and punctuation removal, stemming, lemmatization and lowercase.
    """
    def extract(self, url):
        """
            Extract text from a url's html using BeautifulSoup Module. The output is a BeautifulSoup object.

            # Input:
                - url (str): an url string.

            # Output:
                -soup (beautifulSoup object): A nested data structure containing the url's hmtl elements and content.
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

        try:
            req = Request(url=url, headers=headers)
            html = urlopen(req).read()
        except:
            return None
        soup = BeautifulSoup(html, "lxml")

        return soup


    def text_from_web(self, url):
        """
            Extract text from url's html and returns a list of the strings present on it.

            # Input:
                - url (str): an url string.

            # Output:
                -text (list): a list ofstrings extracted from the url's html. 
        """
        soup = self.extract(url)
        if soup is None:
            return ""

        for script in soup(["script", "style"]):
            script.extract()

        text = soup.body.get_text()

        lines = (line.strip() for line in text.splitlines())

        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text


    def crawler(self, url, limit=10):
        """
        Receives an url and returns a list of links (another urls)  present on its html.

        # Input:
            - url (str): an url string.
            - limit (int, 10): a int number, referring to the maximum of links to return. Default value: 10.

        # Output:
            - links (list): a list of links found on the url's html.
        """
        soup = self.extract(url)
        if soup is None:
            return []

        possible_links = soup.find_all('a', href=True) #TODO shuffle
        links = []
        for i, link in enumerate(possible_links):
            link_url = link.get('href')
            if not link_url:
                continue
            if link_url[0] == '/':
                links += [url[:-1] + link_url]
            elif 'https' in link_url:
                links += [link_url]
            else:
                links += [url + link_url]

            if i > limit:
                break

        return links


    def parse(self, url):
        """
        Receives an url and returns a list of strings extracted from its html already preprocessed (see Parse.preprocess for more information).

        # Input:
            - url (str): an url string.

        # Output:
            - a list of strings that were extracted from the given url's html and that were processed in order to be lowercase, without stopwords and punctuation.      
        """
        text = [self.text_from_web(url)] + [self.text_from_web(link) for link in self.crawler(url)]
        text = sum([sentences.split('\n') for sentences in text], [])

        return self.preprocess(tokenize_text(text))


    def preprocess(self, text, use_stem=False, use_lemma=False):
        """
        Receives a list of strings and returns a list os strings in lowercase, with punctuation and stopwords removed. 
        Optionally, the words are also lemmatized and stemmed.

        # Input:
            - text (list): a list of words (strings). 

        *Optional:* 

            - use_stem (boolean, False): True, if it is to perform stemming in the strings. Default value: False.
            - use_lemma (boolean, False): True, if it is to perform lemmatization in the strings. Default value: False.

        # Output :
            - text (list): list of words with all strings in the lowercase version and also with punctuation and stopwords removed. (Optionally, the strings may also be stemmed and lemmatized).
        """

        assert type(text) == list, "input must be a list"
        text = lowercase(text)
        text = remove_punctuation(text)
        text = remove_stopwords(text)
        if use_stem:
            text = stemming(text)
        if use_lemma:
            text  = lemmatization(text)

        return text
