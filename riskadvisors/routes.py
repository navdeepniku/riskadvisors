from flask import url_for
from flask import request, redirect

import os

from riskadvisors import app


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


@app.route('/file', methods=['GET','POST'])
def upload_file():
    try:
        if request.method == 'POST' and  'file_url' in request.form:
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
                <p><input type=file name=file>
                <input type=submit value=Upload>
            </form>
            <h2>OR</h2>
            <form action="" method=post>
                <p> Enter Dropbox file url </p>
                <p><input type=text name=file_url value=file_url> 
                <input type=submit value=Upload>
            </form>
            '''
    except:
        return "error occourred! return to home: <a href='"+url_for('upload_file')+"'>File<a/>"
@app.route('/dropbox_handle/')
def dropbox_handle():
    try:
        import wget
        file_url = request.args.get('file_url')
        filename = "f1.xlsx"
        f = wget.download(file_url,os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return redirect(url_for('after_upload', filename = filename))
    except:
        return "Enter valid file url"+" return to home: <a href='"+url_for('upload_file')+"'>File<a/>"


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