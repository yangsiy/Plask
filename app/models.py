from app import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), index=True, unique=True)
	password = db.Column(db.String(16))
	mail = db.Column(db.String(50))
	is_admin = db.Column(db.Boolean)
	is_ban = db.Column(db.Boolean)

	questionnaires = db.relationship("Questionnaire", backref='user', lazy='dynamic')
	quesanswers = db.relationship("QuesAnswer", backref='user', lazy='dynamic')

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.username)

class Questionnaire(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	subject = db.Column(db.String(100))
	description = db.Column(db.Text)
	create_time = db.Column(db.DateTime)
	schema = db.Column(db.PickleType)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	is_ban = db.Column(db.Boolean)

	releases = db.relationship("Release", backref='questionnaire', lazy='dynamic')
	quesanswers = db.relationship("QuesAnswer", backref='questionnaire', lazy='dynamic')

	def get_status(self):
		if self.is_ban:
			return 'Banned'
		releases = list(self.releases)
		if not releases:
			return 'In creating'
		release = releases[-1]
		if release.get_status():
			if len(releases) > 1:
				return 'In reopening'
			else:
				return 'In releasing'
		return 'Closed'

	def get_last_release(self):
		releases = list(self.releases)
		if not releases:
			return None
		else:
			return releases[-1]


class Release(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ques_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
	start_time = db.Column(db.DateTime)
	end_time = db.Column(db.DateTime)
	security = db.Column(db.PickleType)
	is_closed = db.Column(db.Boolean)

	def get_status(self):
		current_time = datetime.now()
		if current_time >= self.start_time and current_time <= self.end_time and not self.is_closed:
			return True
		else:
			return False

class QuesAnswer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ques_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	ip = db.Column(db.String(50))
	date = db.Column(db.DateTime)

	probanswers = db.relationship("ProbAnswer", backref='ques_answer', lazy='dynamic')

class ProbAnswer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ques_ans_id = db.Column(db.Integer, db.ForeignKey('ques_answer.id'))
	prob_id = db.Column(db.Integer)
	ans = db.Column(db.Text)
