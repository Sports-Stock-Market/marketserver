from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from social_flask.routes import social_auth
from social_flask_sqlalchemy.models import init_social

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

app.register_blueprint(social_auth)
init_social(app, db.session)

from app import routes, models
