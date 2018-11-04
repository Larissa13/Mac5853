import unittest as ut

from parser import *

class TestPreProcessTextMethods(ut.TestCase):
    
    def test_remove_stopwords(self):
        self.assertEqual(remove_stopwords(['este', 'é',  'um',  'teste']), ['é', 'teste'])
        self.assertEqual(remove_stopwords(['Este', 'é', 'UM', 'teste.']), ['Este', 'é', 'UM', 'teste.'])
    
    def test_remove_punctuation(self):
        self.assertEqual(remove_punctuation(['Este', 'é', 'UM', 'teste.']), ['Este', 'é', 'UM', 'teste'])
    
    def test_stemming(self):
        self.assertEqual(stemming(['sabia', 'pedraria', 'casarão', 'ferreiro']), ['sab', 'pedr', 'cas', 'ferr'])
    
    def test_lowercase(self):
        self.assertEqual(lowercase(['TEmoS', 'QUE', 'estAr', 'minÚscULas']), ['temos', 'que', 'estar', 'minúsculas'])
        
    def test_lemmatization(self):
        self.assertEqual(lemmatization(['é', 'quero', 'sei', 'vemos', 'lê']), ['ser', 'querer', 'saber', 'ver', 'ler'])
    
    def test_preprocess(self):
    	parse = Parser()
    	self.assertEqual(parse.preprocess(['Este', 'é', 'uM.', 'tesTe?', 'das', 'FUNÇÔES', 'ACima,', 'em', 'conjunto%'], use_stem = True, use_lemma = True), ['ser', 'test', 'funçô', 'acim', 'conjunt'])

    def test_preprocess_notlist(self):
    	parse = Parser()
    	with self.assertRaises(Exception) as context:
    		parse.preprocess("este é um teste") 
    	self.assertTrue('input must be a list' in str(context.exception))

class TestTextExtraction(ut.TestCase):
    simple_url = "https://linux.ime.usp.br/~larissadeop/"
    complex_url = "https://linux.ime.usp.br/~larissadeop/Teste_mac5853/"
    html_content = "This is a test page.\nLet\'s find out if the code can detect these texts.\nNow a link"
    crawler_url = "https://linux.ime.usp.br/~larissadeop/Mac0499/"
    links = ['https://linux.ime.usp.br/~larissadeop/Mac0499/Proposta TCC.pdf', 
             'https://linux.ime.usp.br/~larissadeop/Mac0499/Monografia.pdf', 
             'https://linux.ime.usp.br/~larissadeop/Mac0499/apreciacao.pdf', 
             'https://linux.ime.usp.br/~larissadeop/Mac0499/poster.pdf', 
             'https://linux.ime.usp.br/~larissadeop/Mac0499/Apresentacao.pdf']
    parser = Parser()

    def test_simple_text_from_web(self):
        self.assertEqual(self.parser.text_from_web(self.simple_url), '>\nMac0499\nTesteMac5853')
        
    def test_complex_text_from_web(self):
        self.assertEqual(self.parser.text_from_web(self.complex_url), self.html_content)
    
    def test_crawler(self):
        self.assertEqual(self.parser.crawler(self.complex_url), ['https://www.google.com'])
    
    def test_crawler_complex(self):
        self.assertEqual(self.parser.crawler(self.crawler_url), self.links)
    	
    
if __name__ == '__main__':
    ut.main()