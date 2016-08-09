
from flask import Flask

#create application object
app = Flask(__name__)



#creating a secret key for app
app.secret_key = "my cloud secret key"

#config to anable WTF_CSRF
app.wtf_csrf_enabled = True

from flaskstruct import routes