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
    releases = [list(x.releases)[-1] if list(x.releases) else None for x in created]  #retrive last release for each ques
    
    #only show last answers
    ques_answers = []
    ques_ans = {}
    for qa in user.quesanswers:
        ques_ans[qa.ques_id] = qa
    for q_id in ques_ans:
        ques_answers.append(ques_ans[q_id])
        
    
    return render_template('user.html',
            g = g,
            user = user,
            ques_list_created = created,
            ques_list_releases = releases,
            ques_ans_list = ques_answers)