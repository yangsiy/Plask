#-*- coding:utf-8 -*- 

from flask import request,render_template, g, flash, url_for, redirect
from flask.ext.login import login_required
from app import app, db
from models import User, Questionnaire, QuesAnswer
from datetime import datetime, timedelta

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
        d = datetime.now()
        oneday = timedelta(days=1)
        questionnaires_week = []
        answer_week = []

        for i in range(7):
            date_from = datetime(d.year, d.month, d.day, 0, 0, 0)
            date_to = datetime(d.year, d.month, d.day, 23, 59, 59)
            questionnaires_week.append(
                (d.date(),
                Questionnaire.query.filter(
                Questionnaire.create_time >= date_from).filter(
                Questionnaire.create_time <= date_to).count()))
            answer_week.append(
                (d.date(),
                QuesAnswer.query.filter(
                QuesAnswer.date >= date_from).filter(
                QuesAnswer.date <= date_to).count()))
            d = d - oneday

        users = User.query.all()
        questionnaires = Questionnaire.query.all()

    return render_template('administrator.html',
        users = users,
        questionnaires = questionnaires,
        questionnaires_week = questionnaires_week,
        answer_week = answer_week)

@app.route('/administrator/ban_user/<int:userid>')
@login_required
def ban_user(userid):
    if is_not_admin():
        pass
    else:
        u = User.query.get(userid)
        if not u:
            flash("No such user",'error')
        elif u.is_ban:
            flash("The user has been banned",'error')
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
            flash("No such user",'error')
        elif not u.is_ban:
            flash("The user has been unbanned",'error')
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
            flash("No such questionnaire",'error')
        elif q.is_ban:
            flash("The questionnaire has been banned",'error')
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
            flash("No such questionnaire",'error')
        elif not q.is_ban:
            flash("The questionnaire has been unbanned",'error')
        else:
            q.is_ban = False
            db.session.add(q)
            db.session.commit()
            flash("Unban successfully")

    return redirect(url_for('administrator'))