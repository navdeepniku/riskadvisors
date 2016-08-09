from flask import render_template
from flask import url_for
from flask import request, redirect
from flask import session
from flask import flash
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

from flaskstruct import app
from flaskstruct import forms
from flaskstruct.dbconnect import connection, commit

#login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash("Please login first.")
			return redirect(url_for('login'))
	return wrap

@app.route('/')
@login_required
def home():
    redirect(url_for('home'))
    return render_template("index.html")

@app.route('/welcome')
def welcome():
	return render_template("welcome.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('home'))
    title = "- Login"
    error= None
    form = forms.LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            co = connection()
            username=request.form['username']
            co.execute("select username, password from userinfo where username=%s;",[username])
            if co.rowcount != 1:
                error = 'Invalid login, Please try again.'
            else:
                info = co.fetchone()
                dbpassHash = str(info[1])
                if check_password_hash(dbpassHash,request.form['password']):		
                    session['logged_in']= True
                    flash ('You are logged in to My Cloud!')
                    return redirect(url_for('home'))
                else:
                    error = 'Invalid pw'
    return render_template('login.html',title=title, form= form, error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if 'logged_in' in session:
		flash ('Already Logged in')
		return redirect(url_for('home'))
	title = "- Sign up"
	error = None
	form = forms.SignupForm()

	if request.method == 'POST':
		if form.validate_on_submit():
			co = connection()
			username=request.form['username']
			co.execute("select username from userinfo where username=%s;",[username])
			if co.rowcount != 0:
				error = "username already exists, try another"
			else:
				password=generate_password_hash(request.form['password'])
				email=request.form['email']
				name=request.form['name']
				co.execute("insert into userinfo (username,password,name,email) values (%s,%s,%s,%s);",[username,password,name,email])
				commit()
			
				flash ('You successfully signed up on My Cloud! \n Login with your username and password')
				return redirect(url_for('login'))
	return render_template('signup.html',title=title, form=form, error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	flash ('You are logged out from My Cloud!')
	return redirect(url_for('welcome'))

@app.route('/dbtest')
def dbtest():
	co = connection()
	co.execute("insert into userinfo (username,password,email,user) values ('test','test','test','test');")
	commit()
	return "success"
