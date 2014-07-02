from app.core.logging import Logging
from app.core.ansible import Ansi
from app.core.models import Users, UserDetails
from app.modules.users.inc import DatabaseModel
from flask import Blueprint, jsonify, make_response, url_for, abort, request
from app import app, db
import datetime
import json


def dump_datetime(value):
    """ Deserialize datetime object into string form for JSON processing. """
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

mod = Blueprint('users', __name__, url_prefix='/api')
def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'username':
            new_user['uri'] = url_for(
                    'users.get_user',
                    username=user['username'],
                    _external=True
                    )
        else:
            new_user[field] = user[field]
    return new_user

@mod.route('/users', methods=['GET'])
@mod.route('/users/<int:page>', methods=['GET'])
def get_users(page=1):
    """ Get a list of all the users that have been added """
    from app.core.api_views import Api
    api = Api()
    return api.getList(
            db_name=Users,
            page=page,
            key='users'
            )

@mod.route('/users/<username>', methods=['GET'])
@mod.route('/users/<username>/<int:page>', methods=['GET'])
def get_user(username, page=1):
    """ Get a specific user from the database """
    from app.core.api_views import Api
    api = Api()
    return api.getByFields(
            db_name=Users,
            page=page,
            key='username',
            kwargs={'username':username}
            )

@mod.route('/users', methods=['POST'])
def create_user():
    ansi = Ansi("useradd")
    """ Create a new user """
    if not request.json or not 'username' in request.json:
        abort(404)
    # Grab a user and check if it exists.  If it does, kick to 409 response
    dm = DatabaseModel(request.json['username'])
    if dm.validateUser():
        abort(409)
    created = datetime.datetime.utcnow()
    user = dm.createUser(request, created)
    return dm.dataAsJson(
            key='user',
            dictionary=user
            )

@mod.route('/users/<username>', methods=['PUT'])
def update_task(username):
    """ update User information """
    dm = DatabaseModel(username=username)
    user = dm.appendUserDetails(request)
    return  dm.dataAsJson(
            key='user',
            dictionary=user
            )

@mod.route('/count/<db_name>', methods=['GET'])
def get_counts(db_name):
    from app.core.api_views import Api
    api = Api()
    key = db_name
    if db_name == "users":
        db_name = Users
    if db_name == "logging":
        db_name = Logging
    return api.getCount(
            db_name=db_name,
            key=key
            )

