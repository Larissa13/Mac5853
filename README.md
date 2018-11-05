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
`git clone git@github.com:Larissa13/Mac5853.git

Ou vá no link [para download](https://github.com/Larissa13/Mac5853/archive/master.zip)


## Como executar o sistema 
Abra a pasta do sistema 

# Como utilizar o sistema


`pip install flask_sqlalchemy`

`pip install Flask-Migrate`

`pip install flask_script`

`pip install psycopg2-binary`

`pip install psycopg2`

`pip install flask_sockets`

`pip install gensim`

`pip install pandas`

`pip install spacy`

``

# Create database
`sudo -u postgres psql`

`ALTER USER postgres PASSWORD 'password';` 

`CREATE DATABASE forbidden;`
 # Create models and populate database
`python manage.py db init`

`python manage.py db migrate`

`python populate.py`
