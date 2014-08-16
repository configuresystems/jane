from app.modules.users.inc import DatabaseModel
from app.modules.users.forms import AddUser
from app.core.logging import Logging
from app.core.ansible import Ansi
from app.core.models import Users, UserDetails
from app.core.common import ModuleController, AttrDict
from passlib.hash import sha512_crypt
from flask import Blueprint, jsonify, make_response, url_for, abort, request, render_template, redirect
from app import app, db
import datetime
import json


mod = Blueprint('users', __name__, url_prefix='/api')
web = Blueprint('web_users', __name__)
def dump_datetime(value):
    """ Deserialize datetime object into string form for JSON processing. """
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

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
    #ansi = Ansi("useradd")
    """ Create a new user """
    if not request.json or not 'username' in request.json:
        abort(404)
    # Grab a user and check if it exists.  If it does, kick to 409 response
    dc = DatabaseModel(
            request=request
            )
    print request.json
    user = dc.create()
    #Ansi("useradd").run({'user':user})
    return dc.dataAsJson(
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

@web.route('/users', methods=['GET'])
@web.route('/users/<int:page>', methods=['GET'])
def users(page=1):
    """ Get a list of all the users that have been added """
    return render_template(
            'user_list.html',
            title="Users",
            )

@web.route('/users/<user>', methods=['GET'])
def user(user):
    """ Get a list of all the users that have been added """
    return render_template(
            'user_details.html',
            title=user,
            )

@web.route('/users/add', methods=['GET','POST'])
def user_add():
    form = AddUser()
    if form.validate_on_submit:
        if form.username.data and \
                form.password.data:
            request = AttrDict()
            request.json = {
                    "username":form.username.data,
                    "password":form.password.data
                    }
            dc = DatabaseModel(request=request)
            dc.create()
            return redirect(url_for('web_users.user', user=form.username.data))
    return render_template(
            'user_add.html',
            title='Add New User',
            form=form
            )
