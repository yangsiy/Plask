#coding=utf-8
from flask import render_template, flash, redirect, url_for, g, request
from app import app, lm, db
from forms import LoginForm, RegisterForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import User
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.before_request
def before_request():
	if current_user.is_authenticated:
		g.user = current_user
	else:
		g.user = None


@app.route('/')
def index():
	if g.user is not None and g.user.is_authenticated():
		if g.user.is_admin == True:
			return redirect(url_for('administrator'))
		else:
			return redirect(url_for('user', username = g.user.username))
	
	return render_template("index.html")


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		if g.user.is_admin == True:
			return redirect(url_for('administrator'))
		else:
			return redirect(url_for('user', username = g.user.username))

	form = LoginForm()
	
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if (user is not None and user.password == form.password.data and not user.is_ban):
			login_user(user)
			flash("Login successfully")
			if user.is_admin == True:
				return redirect(request.args.get('next') or url_for('administrator'))
			else:
				return redirect(request.args.get('next') or url_for('user', username = user.username))
		form.password.data = ''
		flash("Login failed",'error')
	
	return render_template('login.html',
		g = g,
		form = form,
		islogin = True)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		email_re = re.compile(r'\S+@\S+.\S+')
		if not email_re.match(form.mail.data):
			form.password.data = ''
			form.password_again.data = ''
			flash("Email format invalid",'error')
			return render_template('register.html',
					g = g,
					form = form)

		if form.password.data == form.password_again.data:
			user = User(
				username = form.username.data,
				password = form.password.data,
				mail = form.mail.data)
			try:
				db.session.add(user)
				db.session.commit()
			except:
				form.username.data = ''
				form.password.data = ''
				form.password_again.data = ''
				flash("The username has been used",'error')
				return render_template('register.html',
						g = g,
						form = form)
			login_user(user);
			flash("Register successfully")
			return redirect(url_for('user', username = user.username))
		form.password.data = ''
		form.password_again.data = ''
		flash("Passwords are not the same",'error')

	return render_template('register.html',
		g = g,
		form = form)
