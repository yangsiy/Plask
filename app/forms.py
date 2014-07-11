#coding=utf-8
from flask.ext.wtf import Form
from wtforms import TextField
from wtforms import PasswordField
from wtforms.validators import Required
from flask_wtf.html5 import EmailField

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class LoginForm(Form):
	username = TextField('Userame', validators = [Required()])
	password = PasswordField('Password', validators = [Required()])

class RegisterForm(Form):
	username = TextField('Userame', validators = [Required()])
	password = PasswordField('Password', validators = [Required()])
	password_again = PasswordField('Password again', validators = [Required()])
	mail = TextField('Mail', validators = [Required()])
