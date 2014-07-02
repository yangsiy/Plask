#coding=utf-8
from flask.ext.wtf import Form
from wtforms import TextField
from wtforms import BooleanField
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

class ReleaseForm(Form):
  start_time = TextField('Start time', validators = [Required()])
  close_time = TextField('Close time', validators = [Required()])
  is_allow_anonymous = BooleanField('Allow anonymous')
  limit_num_participants = TextField('Limit delivery number for participant')
  limit_num_ip = TextField('Limit delivery number for IP address')
  special_participants = TextField('Special participants')