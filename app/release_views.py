#-*- coding:utf-8 -*- 

from flask import request,render_template, flash, url_for, redirect
from flask.ext.login import login_required
from app import app, db
from models import Release
from datetime import datetime
import pickle

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
        special_participants = []
      else:
        if request.form['special_participants'] == '':
          special_participants = []
        else:
          special_participants = request.form['special_participants'].split(',')

      security.append(is_allow_anonymous)
      security.append(limit_num_participants)
      security.append(limit_num_ip)
      security.append(special_participants)
      print security
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
                          isclose = False)
        db.session.add(release)
        db.session.commit()
        flash("Release successfully")
        return redirect(url_for('questionnaire'))

    flash("Start time is later then end time")
    
    return render_template('release.html')