
pip install flask_sqlalchemy
pip install Flask-Migrate
pip install flask_script
pip install psycopg2-binary
pip install psycopg2
postgres=# CREATE DATABASE forbidden_db;
python manage.py db init
python manage.py db migrate
