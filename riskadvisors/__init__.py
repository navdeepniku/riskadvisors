from flask import Flask
from flask import request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from config import DATABASE_URI,upload_folder
import os

#create application object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URI
app.config['UPLOAD_FOLDER'] = upload_folder

db = SQLAlchemy(app)

#create db model
'''
class Stock(db.Model):
    __tablename__ = ""
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

db.create_all()
'''
from riskadvisors import routes
