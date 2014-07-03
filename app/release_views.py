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
      security.append(request.form['is_allow_anonymous'])
      security.append(request.form['limit_num_participants'])
      security.append(request.form['limit_num_ip'])

      special_participants = request.form['special_participants'].split(',')
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
                          isclose = False)
        db.session.add(release)
        db.session.commit()
        flash("Release successfully")
        return redirect(url_for('questionnaire/<int:questionnaire_id>'))

    flash("Start time is later then end time")
    
    return render_template('release.html')