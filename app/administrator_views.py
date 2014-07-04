#-*- coding:utf-8 -*- 

from flask import request,render_template, g, flash, url_for, redirect
from flask.ext.login import login_required
from app import app, db
from models import User, Questionnaire

@app.route('/administrator/<string:username>')
@login_required
def administrator(username):
    user = g.user
    if user == None or user.isAdmin == False:
      pass
    else:
      users = User.query.all()
      questionnaires = Questionnaire.query.all()

    return render_template('administrator.html',
        users = users,
        questionnaires = questionnaires)
