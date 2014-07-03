#-*- coding:utf-8 -*- 

from flask import request,render_template,g, flash, url_for
from flask.ext.login import current_user,login_required
from app import app,db
import pickle
from datetime import datetime
from models import Questionnaire


@app.route('/questionnaire/create', methods = ['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        q_title = request.form['title']
        q_subject = request.form['subject']
        q_description = request.form['description']
        q = Questionnaire(title = q_title,
                          subject = q_subject,
                          description = q_description,
                          )
        db.session.add(q)
        db.session.commit()
        url_for('create_question',q_id=q.id)
    

@app.route('/questionnaire/<int:q_id>/create_question',methods = ['GET','POST'])
@login_required
def create_question(q_id):
    def get_questions():
        questions = []
        current_index = 0
        while True:
            ques_form = 'ques_' + str(current_index)  #example: ques_1
            if ques_form in request.form:
                current_question = {
                                    "type": request.form[ques_form + '.type'],  #example:ques_7.type 1单选 2多选3TF4大题（似乎）
                                    "description": request.form[ques_form + '.description'],    #example:ques_9.description
                                    "options": get_options(ques_form)
                                   }
                questions.append(current_question)
                current_index += 1
            else: break
        return questions
    
    def get_options(ques_form):
        options = []
        option_index = 0
        while True:
            option = ques_form + '.option_' + str(option_index)  #example: ques_3.option_3 'C.wow'
            if option in request.form: 
                options.append(request.form[option])
                option_index += 1
            else: break
        return options
                
        
    if request.method == 'POST':
        q = Questionnaire.query.get(q_id)
        questions = get_questions()
        dumped_questions = pickle.dumps(questions, protocol = 2)
        q.schema = dumped_questions
        q.create_time = datetime.now()
        q.author_id = g.user.id

        db.session.add(q)
        db.session.commit()
        flash("There be the URL?")
        
    return render_template('questionnaire_create.html')


            