#coding=utf-8
from flask import render_template, flash, redirect, url_for, g
from app import app, lm, db
from forms import LoginForm, RegisterForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import User

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.before_request
def before_request():
	if current_user.is_authenticated():
		g.user = current_user
	else:
		g.user = None


@app.route('/')
@login_required
def index():
	return 'Hello, World!'


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))

	form = LoginForm()
	
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if (user is not None and user.password == form.password.data):
			login_user(user);
			flash("Login successfully")
			return redirect(url_for('index'))
		form.password.data = ''
		flash("Login failed")
	
	return render_template('login.html',
		g = g,
		form = form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		if form.password.data == form.password_again.data:
			user = User(
				username = form.username.data,
				password = form.password.data,
				mail = form.mail.data)
			db.session.add(user)
			db.session.commit()
			login_user(user);
			flash("Register successfully")
			return redirect(url_for('index'))
		form.password.data = ''
		form.password_again.data = ''
		flash("Passwords are not the same")

	return render_template('register.html',
		g = g,
		form = form)
