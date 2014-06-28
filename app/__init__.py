from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config.from_object('config')
db = SQLAlchemy(app)

from app.core import api_views, models
