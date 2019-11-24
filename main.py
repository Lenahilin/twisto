from flask import Flask, redirect, abort
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_admin.contrib.sqla import ModelView

import os

app = Flask(__name__)
app.secret_key = os.environ['appsecretkey']
app.config.from_pyfile('config.py')

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
  try:
    new_url = Links.query.filter_by(path=some_path).first().dest
  except AttributeError:
    abort(404)
  if not new_url.startswith('http'):
    new_url = 'http://' + new_url
  return redirect(new_url, code=301)

if __name__ == '__main__':
  admin = Admin(app)
  admin.add_view(ModelView(Links, db.session))
  app.run(host = '0.0.0.0', debug=True)