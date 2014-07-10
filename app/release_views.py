#-*- coding:utf-8 -*- 

from flask import request,render_template, flash, url_for, redirect, g
from flask.ext.login import login_required
from app import app, db
from models import Release, Questionnaire
from datetime import datetime
import pickle

@app.route('/questionnaire/<int:questionnaire_id>')
@login_required
def questionnaire(questionnaire_id):
    q = Questionnaire.query.get(questionnaire_id)
    if not q:
        return "ERROR!"
    elif q.get_status() == 'Banned':
            return render_template('message.html',
                message = 'Sorry, the questionnaire is banned')
    else:
        title = q.title
        subject = q.subject
        description = q.description

        release = None
        count = 0
        for r in q.releases:
            count += 1
            if not r.is_closed:
                release = r
                break

        start_time = None
        end_time = None
        is_allow_anonymous = None
        limit_num_participants = None
        limit_num_ip = None
        special_participants = ''
        if release:
            start_time = r.start_time
            end_time = r.end_time
            security = pickle.loads(r.security)
            is_allow_anonymous = security['anonymous']
            limit_num_participants = security['limit_per_user']
            limit_num_ip = security['limit_per_ip']
            if security['limit_participants']:
                special_participants = ', '.join(security['limit_participants'])
        state = q.get_status()

        ques_list = get_ques_list(q)

        return render_template('questionnaire_report.html',
            questionnaire_id = questionnaire_id,
            title = title,
            subject = subject,
            description = description,
            state = state,
            start_time = start_time,
            end_time = end_time,
            is_allow_anonymous = is_allow_anonymous,
            limit_num_participants = limit_num_participants,
            limit_num_ip = limit_num_ip,
            special_participants = special_participants,
            q_id = questionnaire_id,
            ques_list = ques_list)

@app.route('/questionnaire/<int:questionnaire_id>/release', methods = ['GET', 'POST'])
@login_required
def release(questionnaire_id):
    def get_security():
        def to_int(string):
            try: return int(string)
            except ValueError: return None
        
        security = {}

        if 'is_allow_anonymous' not in request.form:
            is_allow_anonymous = False
        else:
            is_allow_anonymous = True

        if 'limit_num_participants' not in request.form:
            limit_num_participants = None
        elif not request.form['limit_num_participants']:
            limit_num_participants = None
        else:
            limit_num_participants = to_int(request.form['limit_num_participants'])

        if 'limit_num_ip' not in request.form:
            limit_num_ip = None
        elif not request.form['limit_num_ip']:
              limit_num_ip = None
        else:
            limit_num_ip = to_int(request.form['limit_num_ip'])

        if 'special_participants' not in request.form:
            special_participants = None
        else:
            data = request.form['special_participants']
            if not data:
                special_participants = None
            else:
                special_participants = data.split(',')
                for i in special_participants:
                    i = i.strip()
                  

        security['anonymous'] = is_allow_anonymous
        security['limit_per_user'] = limit_num_participants
        security['limit_per_ip'] = limit_num_ip
        security['limit_participants'] = special_participants
          
        return security

    if request.method == 'POST':
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        if start_time <  end_time:
            security = get_security()
            dumped_security = pickle.dumps(security, protocol = 2)
            release = Release(ques_id = questionnaire_id,
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S'),
                end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S'),
                security = dumped_security,
                is_closed = False)
            db.session.add(release)
            db.session.commit()
            return render_template('release_success.html',
                g = g,
                q_id = questionnaire_id,
                message = 'Release successfully')
        else:
            flash("Start time is later then end time",'error')

    return render_template('release.html')

@app.route('/questionnaire/<int:questionnaire_id>/close', methods = ['GET'])
@login_required
def close(questionnaire_id):
    q = Questionnaire.query.get(questionnaire_id)
    release = None
    for r in q.releases:
        if not r.is_closed:
            release = r
            break
    if not release:
        flash("The release has been closed",'error')
    else:
        release.is_closed = True
        db.session.add(release)
        db.session.commit()
        flash("Close successfully")
  
    return redirect(url_for('questionnaire', questionnaire_id = questionnaire_id))

def get_ques_list(q):
    schema = pickle.loads(q.schema)
    ques_list = []
    for i in range(len(schema)):
        each = schema[i]
        dic = {}
        dic['description'] = each['description']
        dic['type'] = each['type']
        if each['type'] == '3':
            dic['option_list'] = []
        elif each['type'] == '2':
            dic['option_list'] = ['true', 'false']
            dic['num_list'] = [0,0]
        else:
            dic['option_list'] = each['options']
            dic['num_list'] = []
            for option in dic['option_list']:
                dic['num_list'].append(0)

        quesanswers = q.quesanswers.all()
        for quesanswer in quesanswers:
            answers = quesanswer.probanswers.filter_by(prob_id = i)
            if each['type'] == '3':
                for answer in answers:
                    dic['option_list'].append(answer.ans)
                print str(dic['option_list'])
            elif each['type'] == '2':
                for answer in answers:
                    if answer.ans=='1':
                        dic['num_list'][0] = dic['num_list'][0] + 1;
                    else:
                        dic['num_list'][1] = dic['num_list'][1] + 1;
            else:
                for answer in answers:
                    dic['num_list'][int(answer.ans)] = dic['num_list'][int(answer.ans)] + 1
        ques_list.append(dic)

    return ques_list