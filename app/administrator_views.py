#-*- coding:utf-8 -*- 

from flask import request,render_template, g, flash, url_for, redirect
from flask.ext.login import login_required
from app import app, db
from models import User, Questionnaire

def is_not_admin():
    user = g.user
    if not user or not user.is_admin:
        return True
    return False

@app.route('/administrator')
@login_required
def administrator():
    if is_not_admin():
        pass
    else:
        users = User.query.all()
        questionnaires = Questionnaire.query.all()

    return render_template('administrator.html',
        users = users,
        questionnaires = questionnaires)

@app.route('/administrator/ban_user/<int:userid>')
@login_required
def ban_user(userid):
    if is_not_admin():
        pass
    else:
        u = User.query.get(userid)
        if not u:
            flash("No such user")
        elif u.is_ban:
            flash("The user has been banned")
        else:
            u.is_ban = True
            db.session.add(u)
            db.session.commit()
            flash("Ban successfully")

    return redirect(url_for('administrator'))

@app.route('/administrator/unban_user/<int:userid>')
@login_required
def unban_user(userid):
    if is_not_admin():
        pass
    else:
        u = User.query.get(userid)
        if not u:
            flash("No such user")
        elif not u.is_ban:
            flash("The user has been unbanned")
        else:
            u.is_ban = False
            db.session.add(u)
            db.session.commit()
            flash("Unban successfully")

    return redirect(url_for('administrator'))

@app.route('/administrator/ban_questionnaire/<int:qid>')
@login_required
def ban_questionnaire(qid):
    if is_not_admin():
        pass
    else:
        q = Questionnaire.query.get(qid)
        if not q:
            flash("No such questionnaire")
        elif q.is_ban:
            flash("The questionnaire has been banned")
        else:
            q.is_ban = True
            db.session.add(q)
            db.session.commit()
            flash("Ban successfully")

    return redirect(url_for('administrator'))

@app.route('/administrator/unban_questionnaire/<int:qid>')
@login_required
def unban_questionnaire(qid):
    if is_not_admin():
        pass
    else:
        q = Questionnaire.query.get(qid)
        if not q:
            flash("No such questionnaire")
        elif not q.is_ban:
            flash("The questionnaire has been unbanned")
        else:
            q.is_ban = False
            db.session.add(q)
            db.session.commit()
            flash("Unban successfully")

    return redirect(url_for('administrator'))