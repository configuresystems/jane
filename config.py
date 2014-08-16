import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app/core/models/jane.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'app/core/models/jane_repository')

CSRF_ENABLED = True
SECRET_KEY = 'special keys'

DATABASE_QUERY_TIMEOUT = 0.5
POSTS_PER_PAGE = 25
THEME = "sb-admin-2"
HOST = "23.253.242.179"
PORT = "80"
