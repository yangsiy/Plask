#-*- coding:utf-8 -*- 

from flask import request,render_template,g, flash, url_for, redirect
from flask.ext.login import current_user,login_required
from app import app,db
import pickle
from datetime import datetime
from models import Questionnaire
from _bsddb import DB_AFTER


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
        return redirect(url_for('create_question',q_id=q.id))
    
    return render_template('questionnaire_create.html')
    

@app.route('/questionnaire/<int:q_id>/create_question',methods = ['GET','POST'])
@login_required
def create_question(q_id):
    def get_questions():
        questions = []
        current_index = 0
        while True:
            ques_form = 'ques_' + str(current_index)  #example: ques_1
            if ques_form+'.type' in request.form:
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
                
    q = Questionnaire.query.get(q_id)
    if not q:
        return "ERROR!"
    if request.method == 'POST':
        questions = get_questions()
        dumped_questions = pickle.dumps(questions, protocol = 2)
        q.schema = dumped_questions
        q.create_time = datetime.now()
        q.author_id = g.user.id

        db.session.add(q)
        db.session.commit()
        return "success!"
    
    return render_template('questionnaire_create_question.html')

@app.route('/questionnaire/<int:q_id>/fill',methods = ['GET','POST'])
def fill(r_id):
    q = Questionnaire.query.get(q_id)
    if not q:
        return "ERROR!"
    
    if request.method == 'GET':
        return render_template('questionnaire_fill.html', questionnaire = q)
    
    elif request.method == 'POST':
        questions = pickle.loads(q.schema)  
        ans = QuesAnswer(
                         ques_id = q.id,
                         user_id = g.user.id if g.user else None,
                         ip = request.remote_addr,
                         date = datetime.now()
                         )
        db.session.add(ans)
        db.session.commit()
        for prob_id in range(len(questions)):
            if questions[prob_id]['type'] in ['0','2','3']:
                #single-selection, true/false ,or essay question
                p_ans = ProbAnswer(ques_ans_id = ans.id,
                                    prob_id = prob_id,
                                    ans = request.form['ques_' + prob_id + '.ans'],  #example: ques_3.ans 2(that is, C)
                                    )
                db.session.add(p_ans)
            elif questions[prob_id]['type'] == '1':
                #multi-selection
                for choice_id in range(len(questions[prob_id]["options"])):
                    if 'ques_' + prob_id + '.ans_' + choice_id in request.form: #example: ques_4.ans_7 which is a checkbox
                        p_ans = ProbAnswer(ques_ans_id = ans.id,
                                           prob_id = prob_id,
                                           ans = str(choice_id),  
                                          )
                        db.session.add(p_ans)
        db.session.commit()
        return "Thank you!"
    
    
            