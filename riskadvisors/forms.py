from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class SignupForm(Form):
	name = TextField("Your Name", validators=[DataRequired(), Length(min=4, max=100)])
	username = TextField("Username", validators=[DataRequired(), Length(min=4, max=20)])
	email = TextField("email", validators=[DataRequired(), Length(min=4, max=120)])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=100)])
	
class LoginForm(Form):
	username = TextField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])