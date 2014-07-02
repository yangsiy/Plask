#-*- coding:utf-8 -*- 

from flask import request,render_template, flash
from flask.ext.login import login_required
from app import app, db
from models import Release
import pickle

@app.route('/questionnaire/release', methods = ['GET', 'POST'])
@login_required
def release():
    def get_sercurity():
      sercurity = []
      return sercurity


    form = ReleaseForm()

    if form.validate_on_submit():
      security = get_security()
      dumped_security = pickle.dumps(security, protocol = 2)
      release = Release(ques_id = 
                        start_time = form.start_time.data,
                        end_time = form.end_time.data,
                        security = dumped_security,
                        isclose = false)
      db.session.add(release)
      db.session.commit()
      flash("Release successfully")
    
    return render_template('release.html')