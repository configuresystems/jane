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

mod = Blueprint('api', __name__, url_prefix='/api')
def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'username':
            new_user['uri'] = url_for(
                    'api.get_user',
                    username=user['username'],
                    _external=True
                    )
        else:
            new_user[field] = user[field]

    return new_user

@mod.route('/users', methods=['GET'])
def get_users():
    """ Get a list of all the users that have been added """
    dm = DatabaseModel()
    users = dm.getAllUsers(db_name="Users")
    return jsonify(users=[i.serialize for i in users])

@mod.route('/users/<username>', methods=['GET'])
def get_user(username):
    """ Get a specific user from the database """
    dm = DatabaseModel(username)
    user = dm.getUserByUsername()

    if len(user) == 0:
        abort(404)

    return jsonify(user=user)

@mod.route('/users', methods=['POST'])
def create_user():
    """ Create a new user """
    if not request.json or not 'username' in request.json:
        abort(404)

    # Grab a user and check if it exists.  If it does, kick to 409 response
    dm = DatabaseModel(request.json['username'])
    if dm.validateUser():
        abort(409)

    created = datetime.datetime.utcnow()
    user = dm.createUser(request, created)
    user['created'] = dump_datetime(created)

    return  dm.dataAsJson(
            key='user',
            dictionary=user
            )

@mod.route('/users/<username>', methods=['PUT'])
def update_task(username):
    """ update User information """
    dm = DatabaseModel(username)
    user = dm.getUserByUsername()
    if len(user) == 0:
        abort(404)
    if not request.json:
        abort(400)
    for field in ['password', 'shell']:
        if field in request.json and type(request.json[field]) is not unicode:
            abort(400)
    for field in ['sudoer']:
        if field in request.json and type(request.json[field]) is not bool:
            abort(400)
    user[0]['password'] = 'Password has been updated'
    user[0]['sudoer'] = request.json.get('sudoer', user[0]['sudoer'])
    user[0]['shell'] = request.json.get('shell', user[0]['shell'])
    updates = {}
    for check in request.json:
        if request.json[check]:
            updates[check] = request.json[check]
    dm.appendUserDetails(updates)
    return  dm.dataAsJson(
            key='user',
            dictionary=user[0]
            )

@mod.route('/users/overview', methods=['GET'])
def user_overview():
    """ get user overview """
    dm = DatabaseModel()
    count = dm.getCount()
    return jsonify({'users':count})