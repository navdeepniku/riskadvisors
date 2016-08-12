from flask import url_for
from flask import request, redirect, session
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import mapper, create_session, clear_mappers

import os
from riskadvisors import app,db

@app.route('/')
def index():
    return 'app running'

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
            session['filename']=filename
            return redirect(url_for('after_upload', filename = filename))
        
        

        return '''
            <!doctype html>
            <h1>Upload Xlsx file</h1>
            <form action="" method=post enctype=multipart/form-data>
                <p>Select File: <input type=file name=file>
                <input type=submit value=Upload>
                <p>For big files or slow upload speeds it is advised to use dropbox link option to prevent application timeout
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
        session['filename']=filename
        return redirect(url_for('after_upload', filename = filename))
    except:
        return "Enter valid file url"+" return to home: <a href='"+url_for('upload_file')+"'>File<a/>"


class sheet(object):
    pass

@app.route('/after_upload/<filename>')
def after_upload(filename):
        from openpyxl import load_workbook
        wb = load_workbook(filename=os.path.join(app.config['UPLOAD_FOLDER'],filename), read_only=True)
        #wb = load_workbook(filename='C://users/navdeep/Desktop/book.xlsx', read_only=True)
        
        ws = wb.active

        sheet_headers = []

        for row in ws.rows:
            for cell in row:
                sheet_headers.append(cell.value)
            break
        session['sheet_headers']=sheet_headers
        return redirect(url_for('db_model'))
        
        
@app.route('/db_model')
def db_model():
        sheet_headers = session['sheet_headers']
        e=create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        metadata = MetaData(bind=e)
        t = Table('sheet', metadata, Column('id', Integer, primary_key=True),*(Column(header, String(8000)) for header in sheet_headers))
        metadata.create_all()
        
        return redirect(url_for('db_commit'))
        

@app.route('/db_commit')
def db_commit():
    from openpyxl import load_workbook
    wb = load_workbook(filename=os.path.join(app.config['UPLOAD_FOLDER'],filename), read_only=True)
    sheet_headers=session['sheet_headers']
    
    #wb = load_workbook(filename='C://users/navdeep/Desktop/book.xlsx', read_only=True)
    ws = wb.active
    e=create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    metadata = MetaData(bind=e)
    t = Table('sheet', metadata, Column('id', Integer, primary_key=True),*(Column(header, String(8000)) for header in sheet_headers)) 
        
    clear_mappers() 
    mapper(sheet, t)
    db_session = create_session(bind=e, autocommit=False, autoflush=False)
        
    count=0  
    for r in ws.rows:
        if count>0:
            s = sheet()
            cou=0
            for c in r:
                setattr(s,sheet_headers[cou],c.value)
                cou+=1
            db_session.add(s)
                #if count%100==0:
                #    print 'yes upload'
                #    db_session.commit()
        count+=1

        
    db_session.commit()
    return "done"