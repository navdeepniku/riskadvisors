from flask import url_for
from flask import request, redirect, session
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import mapper, create_session, clear_mappers
import uuid

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
            session['table_name']=request.form['table_name']
            return redirect(url_for('dropbox_handle', file_url=file_url))
            
        elif request.method == 'POST':
            session['table_name']=request.form['table_name']
            file = request.files['file']
            filename  = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['filename']=filename
            return redirect(url_for('after_upload'))
        
        

        return '''
            <!doctype html>
            <h1>Upload Xlsx file</h1>
            <form action="" method=post enctype=multipart/form-data>
                <p>Select File: <input type=file name=file>
                <p>Choose Table name to Store in Database: <input type=text name=table_name value='''+str(uuid.uuid4()).replace('-',"")+'''>
                <input type=submit value=Upload>
                <p>For big files or slow upload speeds it is advised to use dropbox link option to prevent application timeout
            </form>
            <h2>OR</h2>
            <form action="" method=post>
                <p> Enter Dropbox file url </p>
                <p><input type=text name=file_url value=file_url> 
                <p>Choose Table name to Store in Database: <input type=text name=table_name value='''+str(uuid.uuid4()).replace('-',"")+'''>
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
        return redirect(url_for('after_upload'))
    except:
        return "Enter valid file url"+" return to home: <a href='"+url_for('upload_file')+"'>File<a/>"

class sheet(object):
    pass


@app.route('/after_upload/')
def after_upload():
        filename=session['filename']
        from openpyxl import load_workbook
        wb = load_workbook(filename=os.path.join(app.config['UPLOAD_FOLDER'],filename), read_only=True)
        #wb = load_workbook(filename='C://users/navdeep/Desktop/book.xlsx', read_only=True)
        
        ws = wb.active

        sheet_headers = []
        row_count=0
        for row in ws.rows:
            for cell in row:
                sheet_headers.append(cell.value)
            break
        for row in ws.rows:
            row_count+=1
        session['row_count'] = row_count;
        session['sheet_headers']=sheet_headers
        session['handle_size']=10000
        session['handler_count']=1

        return redirect(url_for('db_model'))
        
        
@app.route('/db_model')
def db_model():
        sheet_headers = session['sheet_headers']
        tab=session['table_name']
        e=create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        metadata = MetaData(bind=e)
        t = Table(tab, metadata, Column('id', Integer, primary_key=True),*(Column(header, String(8000)) for header in sheet_headers))
        metadata.create_all()
        clear_mappers() 
        mapper(sheet, t)
    
        return redirect(url_for('database_handler'))

@app.route('/db_commit')
def db_commit():
    from openpyxl import load_workbook
    wb = load_workbook(filename=os.path.join(app.config['UPLOAD_FOLDER'],session['filename']), read_only=True)
    sheet_headers=session['sheet_headers']
    
    #wb = load_workbook(filename='C://users/navdeep/Desktop/book.xlsx', read_only=True)
    ws = wb.active
    
    e=create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    metadata = MetaData(bind=e)
    tab=session['table_name']
    t = Table(tab, metadata, Column('id', Integer, primary_key=True),*(Column(header, String(8000)) for header in sheet_headers)) 
        
    clear_mappers() 
    mapper(sheet, t)
    db_session = create_session(bind=e, autocommit=False, autoflush=False)

      
    handler_count = session['handler_count']
    handle_size = session['handle_size']
    count=0
    handle_size_counter=0
    for r in ws.rows:
        count+=1
        if handler_count>count-1:
            continue
        else:
            handle_size_counter+=1
            if count%100==0: print count,handle_size_counter,handle_size
            s = sheet()
            cou=0
            for c in r:
                setattr(s,sheet_headers[cou],c.value)
                cou+=1
                
            db_session.add(s)
            if handle_size_counter-1==handle_size:
                break
    session['handler_count']=handler_count+1+session['handle_size']
    db_session.commit()
    return redirect(url_for('database_handler'))

@app.route("/database_handler", methods=['GET','POST'])
def database_handler():
    

    if request.method == 'POST' and  session['handler_count']<session['row_count']:
        return redirect(url_for('db_commit'))
            
    elif request.method == 'POST' and session['handler_count']>=session['row_count']:
        return "done"
        

    return  '''
            <!doctype html>
            <h1>Please Wait! Saving table to Database</h1>
            <h2>Completed '''+str((int(session['handler_count'])*100)/int(session['row_count']))+'''%</h2>
            <form action="" method=post>
                <input id="autoclick" style='visibility:hidden;' type=submit value=Proceed>
            </form>
            <script>
            document.getElementById("autoclick").click();
            </script>
            '''
