from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), index=True, unique=True)
	password = db.Column(db.String(16))
	mail = db.Column(db.String(50))
	isAdmin = db.Column(db.Boolean)
	isClosed = db.Column(db.Boolean)

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

	releases = db.relationship("Release", backref='questionnaire', lazy='dynamic')
	quesanswers = db.relationship("QuesAnswer", backref='questionnaire', lazy='dynamic')

class Release(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ques_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
	start_time = db.Column(db.DateTime)
	end_time = db.Column(db.DateTime)
	security = db.Column(db.PickleType)
	isclose = db.Column(db.Boolean)

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
