#-*- coding:utf-8 -*- 

from flask import request,render_template, flash
from flask.ext.login import login_required
from app import app, db
from models import Release
import pickle

@app.route('/questionnaire/<int:questionnaire_id>/release', methods = ['GET', 'POST'])
@login_required
def release():
    def get_sercurity():
      sercurity = []
      sercurity.append(request.form['is_allow_anonymous'])
      sercurity.append(request.form['limit_num_participants'])
      sercurity.append(request.form['limit_num_ip'])

      special_participants = request.form['special_participants'].split(',')
      sercurity.append(special_participants)
      return sercurity


    form = ReleaseForm()

    if form.validate_on_submit():
      if start_time <  end_time:
        security = get_security()
        dumped_security = pickle.dumps(security, protocol = 2)
        release = Release(ques_id = questionnaire_id,
                          start_time = request.form['start_time'],
                          end_time = request.form['end_time'],
                          security = dumped_security,
                          isclose = false)
        db.session.add(release)
        db.session.commit()
        flash("Release successfully")
        return redirect(url_for('questionnaire/<int:questionnaire_id>'))

      flash("Start time is later then end time")
    
    return render_template('release.html')