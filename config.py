import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app/core/models/jane.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'app/core/models/jane_repository')

CSRF_ENABLED = True
SECRET_KEY = 'special keys'

DATABASE_QUERY_TIMEOUT = 0.5
