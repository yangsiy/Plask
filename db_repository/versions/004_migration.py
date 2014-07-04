from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
prob_answer = Table('prob_answer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('ques_ans_id', Integer),
    Column('prob_id', Integer),
    Column('ans', Text),
)

ques_answer = Table('ques_answer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('ques_id', Integer),
    Column('user_id', Integer),
    Column('ip', String(length=50)),
    Column('date', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['prob_answer'].create()
    post_meta.tables['ques_answer'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['prob_answer'].drop()
    post_meta.tables['ques_answer'].drop()
