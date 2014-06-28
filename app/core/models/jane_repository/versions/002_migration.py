from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user_details = Table('user_details', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('last', String(length=64)),
    Column('first', String(length=64)),
    Column('company', String(length=128)),
    Column('phone', String(length=64)),
    Column('email', String(length=128)),
    Column('user', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user_details'].columns['company'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user_details'].columns['company'].drop()
