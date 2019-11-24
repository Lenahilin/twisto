from flask import Flask, redirect, abort, url_for
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

roles_users = db.Table(
  'roles_users',
  db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
  db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True)
  password = db.Column(db.String(255))
  active = db.Column(db.Boolean())
  roles = db.relationship('Role', secondary=roles_users,
                          backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create customized model view class
class MyModelView(sqla.ModelView):
  def is_accessible(self):
    return (current_user.is_active and
            current_user.is_authenticated and
            current_user.has_role('superuser')
    )

  def _handle_view(self, name, **kwargs):
    if not self.is_accessible():
      if current_user.is_authenticated:
        # permission denied
        abort(403)
      else:
        # login
        return redirect(url_for('security.login', next=request.url))

admin = flask_admin.Admin(
  app,
  'Example: Auth',
  base_template='my_master.html',
  template_mode='bootstrap3',
)

# admin.add_view(MyModelView(Role, db.session))
# admin.add_view(MyModelView(User, db.session))

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
  return dict(
    admin_base_template=admin.base_template,
    admin_view=admin.index_view,
    h=admin_helpers,
    get_url=url_for
  )

def build_sample_db():
  """
  Populate a small db with some example entries.
  """

  import string
  import random

  db.create_all()

  with app.app_context():
    user_role = Role(name='user')
    super_user_role = Role(name='superuser')
    db.session.add(user_role)
    db.session.add(super_user_role)
    db.session.commit()

    test_user = user_datastore.create_user(
      email='admin',
      password=encrypt_password('admin'),
      roles=[user_role, super_user_role]
    )
    db.session.commit()
  return

class Links(db.Model):
  id = db.Column(db.Integer, primary_key=True, unique=True)
  path = db.Column(db.String(45), unique=True)
  dest = db.Column(db.String(300))

admin.add_view(MyModelView(Links, db.session))

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
  # admin = Admin(app)
  # admin.add_view(ModelView(Links, db.session))

  # build_sample_db()
  app.run(host = '0.0.0.0', debug=True)