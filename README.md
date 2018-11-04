# Install dependencies

`sudo apt-get install postgresql postgresql-contrib libpq-dev`

`pip install flask`

`pip install flask_sqlalchemy`

`pip install Flask-Migrate`

`pip install flask_script`

`pip install psycopg2-binary`

`pip install psycopg2`

`pip install flask_sockets`

# Create database
`sudo -u postgres psql`

`ALTER USER postgres PASSWORD 'password';` 

`CREATE DATABASE forbidden;`

# Create models and populate database
`python manage.py db init`

`python manage.py db migrate`

`python populate.py`
