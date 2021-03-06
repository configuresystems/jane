from app.modules.users.views import mod as users
from app.modules.domains.views import mod as domains
from app.modules.overview.views import mod as overview
from app.core.logging.views import mod as logging
from app.core.logging import Logging
from app.core.models import Users, UserDetails
from app.modules.domains.models import Domains, DomainDetails
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

            list = {key:[i.serialize for i in list]}
        except Exception, e:
            abort(500)
        if len(list) == 0:
            abort(404)
        return jsonify(list)

    def getList(self, db_name, page, key):
        list = db_name.query.paginate(page, POSTS_PER_PAGE, False)
        list = {key:[i.serialize for i in list.items]}
        list['count'] = db.session.query(db_name.id).count()
        return jsonify(list)

    def getCount(self, db_name, key):
        list = db.session.query(db_name.id).count()
        return jsonify({key:list})

    def getOverviewCount(self, db_name, key, field):
        error = db.session.query(db_name.id).filter(
                db_name.status_code=='error').count()
        success = db.session.query(db_name.id).filter(
                db_name.status_code=='success').count()
        users = db.session.query(Users.id).count()
        domains = db.session.query(Domains.id).count()
        to_return = {
                'logs': [
                    {
                        'name': 'domains',
                        'count': domains
                        },
                    {
                        'name': 'users',
                        'count': users,
                        },
                    {
                        'name': 'success',
                        'count': success
                        },
                    {
                        'name': 'error',
                        'count': error,
                        },
                    ]
                }
        return jsonify(to_return)

    def create(self, db_name, db_join, relationship, key, **kwargs):
        """
        db_name == database name
        relationship = status or username
        """
        try:
            # inserting into db
            to_pop = key + "_details"
            d = kwargs.pop(to_pop)
            insert = db_name(**kwargs)
            db.session.add(insert)
            db.session.commit()
            id = db_name.query.get(insert.id)
        except Exception, e:
            print e
            db.session.rollback()
            id = db_name.query.get(relationship)
        try:
            # Get ID of the last insert
            details = {}
            # set relationship
            append = db_join(**d)
            db.session.add(append)
            db.session.commit()
        except Exception, e:
            print e
            db.session.rollback()
            abort(500)

app.register_blueprint(users)
app.register_blueprint(domains)
app.register_blueprint(logging)
app.register_blueprint(overview)

#@app.route('/')
#def index():
#    return "hello world"

@app.errorhandler(400)
def bad_request(error):
    db.session.rollback()
    return make_response(jsonify({'error':'Bad Request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not Found'}), 404)

@app.errorhandler(409)
def conflict(error):
    return make_response(jsonify({'error':'Entity Exists'}), 409)

@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return make_response(jsonify({'error':'Internal Server Error'}), 500)

