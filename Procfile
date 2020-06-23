web: gunicorn app:app
heroku addons:create heroku-postgresql:hobby-dev
set FLASK_APP=fanbase.py
flask db init
flask db migrate -m "fanbase"
flask db upgrade
flask run
