
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import DATABASE_URI

#create application object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URI
db = SQLAlchemy(app)

#create db model

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
    self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

db.create_all()

from riskadvisors import routes


