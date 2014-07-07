#-*- coding:utf-8 -*- 

from flask import request,render_template, g, flash, url_for, redirect, abort
from flask.ext.login import login_required
from app import app, db
from models import User, Questionnaire

@app.route('/user/<string:username>')
@login_required
def user(username):
    users = list(User.query.filter_by(username = username))
    if not users:
        abort(404)
    user = users[0]
    created = Questionnaire.query.filter_by(author_id = user.id).all()
    created = list(created)
    releases = [x.retrive_last_release() for x in created]
    
    ques_answers = list(user.quesanswers)
    print str(ques_answers)
    '''
    quess = []
    for each in ques:
        if each.ques_id not in quess:
            quess.append(each.ques_id)
    answerd = []
    for each in quess:
        answerd.append(Questionnaire.query.get(each))
    '''
    return render_template('user.html',
            g = g,
            ques_list_created = created,
            ques_list_releases = releases,
            ques_ans_list = ques_answers)