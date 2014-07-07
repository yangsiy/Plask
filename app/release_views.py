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
    if q == None:
      pass
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
        is_allow_anonymous = security[0]
        limit_num_participants = security[1]
        limit_num_ip = security[2]
        if security[3]:
          special_participants = ', '.join(security[3])
        if count > 1:
          state = 'In reopening'
        else:
          state = 'In releasing'
      else:
        if count > 0:
          state = 'Closed'
        else:
          state = 'In creating'

    return render_template('questionnaire.html',
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
        q_id = questionnaire_id)

@app.route('/questionnaire/<int:questionnaire_id>/release', methods = ['GET', 'POST'])
@login_required
def release(questionnaire_id):
    def get_security():
      security = []

      if 'is_allow_anonymous' not in request.form:
        is_allow_anonymous = 0
      else:
        is_allow_anonymous = 1

      if 'limit_num_participants' not in request.form:
        limit_num_participants = 0
      else:
        if request.form['limit_num_participants'] == '':
          limit_num_participants = 0
        else:
          limit_num_participants = int(request.form['limit_num_participants'])

      if 'limit_num_ip' not in request.form:
        limit_num_ip = 0
      else:
        if request.form['limit_num_ip'] == '':
          limit_num_ip = 0
        else:
          limit_num_ip = int(request.form['limit_num_ip'])

      if 'special_participants' not in request.form:
        special_participants = None
      else:
        data = request.form['special_participants'].replace(' ', "")
        if data == '':
          special_participants = None
        else:
          special_participants = data.split(',')

      security.append(is_allow_anonymous)
      security.append(limit_num_participants)
      security.append(limit_num_ip)
      security.append(special_participants)
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
        flash("Release successfully")
        #return redirect(url_for('questionnaire', questionnaire_id = questionnaire_id))
        return render_template('release_success.html',
                g = g,
                q_id = questionnaire_id,
                message = 'Questionnaire Created Successfully')

    flash("Start time is later then end time")
    return render_template('release.html')

@app.route('/questionnaire/<int:questionnaire_id>/close', methods = ['GET'])
@login_required
def close(questionnaire_id):
    q = Questionnaire.query.get(questionnaire_id)
    release = None
    for r in q.releases:
      if r.is_closed == 0:
        release = r
        break
    if release == None:
      flash("The release has been closed")
    else:
      release.is_closed = 1
      db.session.add(release)
      db.session.commit()
      flash("Close successfully")
  
    return redirect(url_for('questionnaire', questionnaire_id = questionnaire_id))
