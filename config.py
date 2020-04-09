import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    #Settings for social-auth (login through third parties, i.e. Google)
    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        'social_core.backends.google.GoogleOAuth2',
    )
    SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index'
    SOCIAL_AUTH_LOGIN_ERROR_URL = '/login'
    SOCIAL_AUTH_USER_MODEL = 'app.models.User'
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_ID')
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_SECRET')
