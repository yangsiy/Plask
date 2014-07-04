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

@app.route('/administrator/<string:username>/ban/<int:userid>')
@login_required
def ban(username, userid):
    user = g.user
    if user == None or user.isAdmin == False:
      pass
    else:
      u = User.query.get(userid)
      if u == None:
        flash("No such user")
      elif u.isClosed == 1:
        flash("The user has been banned")
      else:
        u.isClosed = 1
        db.session.add(u)
        db.session.commit()
        flash("Ban successfully")
  
    return redirect(url_for('administrator', username = username))

@app.route('/administrator/<string:username>/unban/<int:userid>')
@login_required
def unban(username, userid):
    user = g.user
    if user == None or user.isAdmin == False:
      pass
    else:
      u = User.query.get(userid)
      if u == None:
        flash("No such user")
      elif u.isClosed == 0:
        flash("The user has been unbanned")
      else:
        u.isClosed = 0
        db.session.add(u)
        db.session.commit()
        flash("Unban successfully")
  
    return redirect(url_for('administrator', username = username))