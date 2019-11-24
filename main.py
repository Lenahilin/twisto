from flask import Flask, redirect
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
import os

app = Flask(__name__)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.environ['msqluser']
app.config['MYSQL_PASSWORD'] = os.environ['msqlpassword']
app.config['MYSQL_DB'] = 'twisto_db'

app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = os.environ['appsecretkey']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + os.environ['msqluser'] + ':' + app.config['MYSQL_PASSWORD']+ '@localhost/twisto_db'
app.config['SQLALCHEMY_DATABASE_URI'] = ''

db = SQLAlchemy(app)

class Links(db.Model):
  id = db.Column(db.Integer, primary_key=True, unique=True)
  path = db.Column(db.String(45), unique=True)
  dest = db.Column(db.String(300))

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/<some_path>')
def redirect_to_path(some_path):
  new_url = 'http://www.google.com/' + some_path
  return redirect(new_url, code=301)

if __name__ == '__main__':
  admin = Admin(app)
  admin.add_view(ModelView(Links, db.session))

  app.run(host = '0.0.0.0', debug=True)