import os

SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = ""

SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"

FLASK_ADMIN_SWATCH = 'cerulean'

MYSQL_HOST = 'localhost'
MYSQL_USER = os.environ['msqluser']
MYSQL_PASSWORD = os.environ['msqlpassword']
MYSQL_DB = 'twisto_db'
SESSION_TYPE = 'filesystem'

SQLALCHEMY_TRACK_MODIFICATIONS = False
