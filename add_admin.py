from app.models import User
from app import db

user = User(username = 'admin',
			password = 'admin',
			mail = 'admin@admin.com',
			is_admin = True,
			is_ban = False,)

db.session.add(user)
db.session.commit()
