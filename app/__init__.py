from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config.from_object('config')
db = SQLAlchemy(app)

#if not app.debug:
#    import logging
#    from logging.handlers import RotatingFileHandler
#    error = RotatingFileHandler('tmp/error.log', 'a', 1 * 1024 * 1024, 10)
#    error.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#    app.logger.setLevel(logging.INFO)
#    error.setLevel(logging.INFO)
#    app.logger.addHandler(error)
#    app.logger.info('Jane - syncing with SkyNet')

from app.core import api_views, web_views, models
