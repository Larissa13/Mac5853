# Install dependencies
`pip install flask_sqlalchemy`
`pip install Flask-Migrate`
`pip install flask_script`
`pip install psycopg2-binary`
`pip install psycopg2`

# Create database
`sudo -u postgres psql`
`CREATE DATABASE forbidden_db;`

# Create models and populate database
`python manage.py db init`
`python manage.py db migrate`
