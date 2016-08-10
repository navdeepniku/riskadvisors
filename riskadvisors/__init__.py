
from flask import Flask
from flask import request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from config import DATABASE_URI
import os

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


@app.route('/')
def home():
    
    '''u1 = User("email")

    db.session.add(u1)
    db.session.commit()
    '''
    us = User.query.all()
    for u in us:
        email=u.email
    return "hi"+os.environ["Database"]+" email for u1 :"+email

#from riskadvisors import routes

#upload_folder = 'C://Users/navdeep/Documents/Github/riskadvisors/tmp/'
upload_folder = "/tmp/"
app.config['UPLOAD_FOLDER'] = upload_folder

@app.route('/file', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename  = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('after_upload', filename = filename))
    return '''
        <!doctype html>
        <h1>Upload Xlsx file</h1>
        <form action="" method=post enctype=multipart/form-data>
            <p><input type=file name=file>
               <input type=submit value=Upload>
        </form>
        '''
@app.route('/test')
def test():
    import wget
    #file = wget.download("https://www.dropbox.com/s/zt1xyzqhqfdqxr0/Stock%20Data.xlsx?dl=1")
    #return redirect(url_for('after_upload', filename = file))
    return os.system("pwd")

@app.route('/after_upload/<filename>')
def after_upload(filename):
    from openpyxl import load_workbook
    wb = load_workbook(filename=os.path.join(app.config['UPLOAD_FOLDER'],filename), read_only=True)
    ws = wb.active
    for row in ws.rows:
        for cell in row:
            return (cell.value)
