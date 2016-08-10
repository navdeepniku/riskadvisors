from flask import url_for
from flask import request, redirect

import os

from riskadvisors import app

@app.route('/')
def home():
    redirect(url_for('home'))
    u1 = User("email")

    return "hi"+os.environ["Database"]+" email for u1 :"+u1.__repr__()
