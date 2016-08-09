from flask import url_for
from flask import request, redirect

import os

from riskadvisors import app

@app.route('/')
def home():
    redirect(url_for('home'))
    return "hi"+os.environ["Database"]
