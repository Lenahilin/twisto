from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'twisto_db'

app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = ''

db = SQLAlchemy(app)

@app.route('/')
def hello_world():
  return 'Hello, World!'

class Links(db.Model):
  id = db.Column(db.Integer, primary_key=True, unique=True)
  path = db.Column(db.String(45), unique=True)
  dest = db.Column(db.String(300))

if __name__ == '__main__':
  admin = Admin(app)
  admin.add_view(ModelView(Links, db.session))

  app.run(host = '0.0.0.0', debug=True)