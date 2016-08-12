from flask import Flask
from flask import request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from config import DATABASE_URI,upload_folder,secret_key
import os

#create application object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URI
app.config['UPLOAD_FOLDER'] = upload_folder
app.secret_key = secret_key

db = SQLAlchemy(app)

from riskadvisors import routes
