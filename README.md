# Projeto para classificar as Urls com conteúdo ilegal

## Objetivo
 Este projeto tem como objetivo a classificação de urls por meio da comparação da versão vetorizada palavras extraídas e pré-processadas do html das páginas. As classes são:
* Armas de fogo
* Cigarro
* Prostituição
* Remédios de venda controlada ou proibida
* Serviços ilegais
* Urls permitidas (isto é sem conteúdo ilegal)

## Como instalar o sistema

Para instalar o sistema execute em um terminal
`git clone git@github.com:Larissa13/Mac5853.git`

Ou vá no link [para download](https://github.com/Larissa13/Mac5853/archive/master.zip)

O sistema necessita de 8GB de RAM pelo menos:

Baixe o [modelo word2vec](https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.pt.vec) pré-treinado.

Crie uma pasta chamada wiki.pt e coloque dentro o arquivo baixado.


### Normal

Instale as dependências executando os seguintes comandos:

`pip install -r requirements.txt`

`python -m spacy download pt`


### Docker (Demora cerca de 30 minutos)

Certifique-se de que possui o Docker instalado e execute os seguintes comandos:

`docker build -t forbidden_cls:latest .`

`docker run --name forbidden_cls -d -p 5000:5000 forbidden_cls:latest`

## Como executar o sistema 

Se o sistema foi instalado com o Docker, pule para o passo 5

1.Abra a pasta do sistema 

2.Execute para popular a base de dados `python populate.py`

3.Execute o comando `python execute.py`

4.Aguarde que apareça as mensagens 

> loading w2v

> finished loading

5.Vá no browser e digite 127.0.0.1:5000 ou localhost:5000

Então, é possível utiizar o sistema, via interface gráfica.

# Como utilizar o sistema via interface gráfica
![Imagem da página inicial](/images/template.png "Imagem da página inicial do sistema")

No campo *URL* é possível incluir a url a ser testada.
Para executar o classificador, basta apertar, então, o botão *submit*.
Como os resultados da classificação das urls vistas são salvos no banco de dados, caso o usuário deseje que a classificação de uma dada url seja classificada novamente, basta que após incluir a url no campo *URL*, ele selecione também a checkbox *force calculation* e aperte *submit*.

![Imagem resultado permitido](/images/ans_perm.png "Imagem resultado permitido")


![Imagem resultado proibido](/images/ans_prob.png "Imagem resultado proibido")


# Como utilizar o sistema por meio de requisição HTTP com método POST
Abra a pasta do sistema 

Execute para popular a base de dados `python populate.py`

Execute o comando `python execute.py`

Aguarde que apareça as mensagens 

> loading w2v

> finished loading

Execute o servidor que receberá os callbacks com o comando:

`python callback_listener.py`

Em outra aba do terminal, execute o seguinte:

```
python 

>>> import requests
>>> import json
>>> url = "http://127.0.0.1:5000/"
>>> callback_port = "5001"
>>> callback = "http://127.0.0.1:" + callback_port

>>> req_content = {'sites': ["http://www.exemplo1.com",
                             "http://www.exemplo2.com",
                             "http://www.exemplo3.com",
                             "http://www.exemplo4.com"], "callback":callback}
                             
>>> requests.post(url, json=json.dumps(req_content))
```


# Como executar os testes de unidade e funcionais
Na pasta do projeto, execute `pytest` .

Depois, abra a pasta app com `cd app` e execute o comando `pytest` .

Caso queira executar cada teste separadamente, faça `python [nome do arquivo de teste].py` .




