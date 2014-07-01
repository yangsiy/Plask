#coding=utf-8
from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class LoginForm(Form):
	username = TextField('Userame', validators = [Required()])
	password = TextField('Password', validators = [Required()])

class RegisterForm(Form):
	username = TextField('Userame', validators = [Required()])
	password = TextField('Password', validators = [Required()])
	password_again = TextField('Password again', validators = [Required()])
	mail = TextField('Mail', validators = [Required()])