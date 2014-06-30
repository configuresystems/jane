from app.modules.users.views import mod as users
from app.core.logging.views import mod as logging
from app.core.logging import Logging
from app.core.models import Users, UserDetails
from sqlalchemy import func, distinct, exists
from config import DATABASE_QUERY_TIMEOUT, POSTS_PER_PAGE
from flask import make_response, jsonify, abort
from app import app, db
import json

### API VIEWS

class Api():
    def __init__(self):
        pass

    def make_public_user(self, item):
        new = {}
        for field in item:
            if field == 'username':
                new['uri'] = url_for(
                        'api.get_user',
                        username=user['username'],
                        _external=True
                        )
            else:
                new[field] = item[field]
        return new

    def getByFields(self, db_name, page, key, kwargs):
        try:
            list = db_name.query.filter_by(
                    **kwargs
                    ).paginate(
                            page,
                            POSTS_PER_PAGE,
                            False,
                            ).items
        except Exception, e:
            abort(500)
        if len(list) == 0:
            abort(404)
        return jsonify({key:[i.serialize for i in list]})

    def getList(self, db_name, page, key):
        list = db_name.query.paginate(page, POSTS_PER_PAGE, False).items
        return jsonify({key:[i.serialize for i in list]})

    def getCount(self, db_name, key):
        list = db.session.query(db_name.id).count()
        return jsonify({key:list})

app.register_blueprint(users)
app.register_blueprint(logging)

@app.route('/')
def index():
    return "hello world"

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error':'Bad Request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not Found'}), 404)

@app.errorhandler(409)
def conflict(error):
    return make_response(jsonify({'error':'Entity Exists'}), 409)

@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error':'Internal Server Error'}), 500)

