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
    if request.method == 'POST' and  request.form['file_url'] != 'file_url':
        file_url = request.form['file_url']
        file_url = file_url[0:-1]+'1'
        return redirect(url_for('dropbox_handle', file_url=file_url))

    elif request.method == 'POST':
        file = request.files['file']
        filename  = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('after_upload', filename = filename))
    
    

    return '''
        <!doctype html>
        <h1>Upload Xlsx file</h1>
        <form action="" method=post enctype=multipart/form-data>
            <p><input type=file name=file></p>
            <p>OR</p>
            <p> Enter Dropbox file url </p>
            <p><input type=text name=file_url value=file_url> 
               <input type=submit value=Upload>
        </form>
        '''
@app.route('/dropbox_handle/<file_url>')
def dropbox_handle(file_url):
    try:
        import wget
        filename = "f1.xlsx"
        f = wget.download(file_url,os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return redirect(url_for('after_upload', filename = filename))
    except:
        return "Enter valid file url"
@app.route('/after_upload/<filename>')
def after_upload(filename):
    try:
        from openpyxl import load_workbook
        wb = load_workbook(filename=os.path.join(app.config['UPLOAD_FOLDER'],filename), read_only=True)
        ws = wb.active
        for row in ws.rows:
            for cell in row:
                return (cell.value)
    except:
        return "not a valid file"