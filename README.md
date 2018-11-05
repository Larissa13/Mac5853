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


## Como executar o sistema 
Abra a pasta do sistema 

Execute para popular a base de dados `python populate.py`

Execute o comando `python execute.py`

Aguarde que apareça as mensagens 

> loading w2v

> finished loading

Vá no browser e digite 127.0.0.1:5000 ou localhost:5000

Então, é possível utiizar o sistema, via interface gráfica.

# Como utilizar o sistema via interface gráfica
![Imagem da página inicial](/images/template.png "Imagem da página inicial do sistema")

No campo *URL* é possível incluir a url a ser testada.
Para executar o classificador, basta apertar, então, o botão *submit*.
Como os resultados da classificação das urls vistas são salvos no banco de dados, caso o usuário deseje que a classificação de uma dada url seja classificada novamente, basta que após incluir a url no campo *URL*, ele selecione também a checkbox *force calculation* e aperte *submit*.

![Imagem resultado permitido](/images/ans_perm.png "Imagem resultado permitido")


![Imagem resultado proibido](/images/ans_prob.png "Imagem resultado proibido")


# Como utilizar o sistema por meio de requisição HTTP com método POST



# Como executar os testes de unidade e funcionais
Na pasta do projeto, execute `pytest` .

Depois, abra a pasta app com `cd app` e execute o comando `pytest` .

Caso queira executar cada teste separadamente, faça `python [nome do arquivo de teste].py` .

# Dependências
`pip install flask_sqlalchemy`

`pip install Flask-Migrate`

`pip install flask_script`

`pip install psycopg2-binary`

`pip install psycopg2`

`pip install flask_sockets`

`pip install gensim`

`pip install pandas`

`pip install spacy`

`pip install gevent`

`pip install zmq`

`pip install requests`
 
`pip install beautifulsoup4`

`pip install lxml`

`python -m spacy download pt`
