#-*- coding:utf-8 -*- 

from flask import request,render_template, g, flash, url_for, redirect
from flask.ext.login import login_required
from app import app, db
from models import User, Questionnaire

@app.route('/user/<string:username>')
@login_required
def user(username):
    created = Questionnaire.query.filter_by(author_id = g.user.id).all()
    ques = g.user.quesanswers
    quess = []
    for each in ques:
        if each.ques_id not in quess:
            quess.append(each.ques_id)
    answerd = []
    for each in quess:
        answerd.append(Questionnaire.query.get(each))
    return render_template('user.html',
            g = g,
            ques_list_created = created,
            ques_list_filled = answerd)