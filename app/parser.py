from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer 
from nltk import tokenize
import spacy
import string, re

def tokenize_text(sentences):
    words = [tokenize.word_tokenize(sent, language='portuguese') for sent in sentences]
    words = sum(words, [])

    return words


def remove_stopwords(text):
    new_text = []
    stop_words = set(stopwords.words('portuguese'))
    for word in text:
        if word not in stop_words:
            new_text += [word]

    return new_text


def remove_punctuation(text):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    new_text = [regex.sub('', word) for word in text]

    return new_text


def stemming(text):
    text = [word for word in text if word != ""]
    stemmer = RSLPStemmer()
    new_text = [stemmer.stem(word) for word in text]

    return new_text


def lowercase(text):
    new_text = [word.lower() for word in text]

    return new_text


def lemmatization(text):
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
    def extract(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        req = Request(url=url, headers=headers)
        try:
            html = urlopen(req).read()
        except:
            return None
        soup = BeautifulSoup(html, "lxml")

        return soup


    def text_from_web(self, url):

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
        soup = self.extract(url)
        if soup is None:
            return []

        possible_links = soup.find_all('a', href=True) #TODO shuffle
        links = []
        for i, link in enumerate(possible_links):
            link_url = link.get('href')
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
        text = [self.text_from_web(url)] + [self.text_from_web(link) for link in self.crawler(url)]
        text = sum([sentences.split('\n') for sentences in text], [])

        return self.preprocess(tokenize_text(text))


    def preprocess(self, text, use_stem=False, use_lemma=False):
        assert type(text) == list, "input must be a list"
        text = lowercase(text)
        text = remove_punctuation(text)
        text = remove_stopwords(text)
        if use_stem:
            text = stemming(text)
        if use_lemma:
            text  = lemmatization(text)

        return text
