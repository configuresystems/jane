from flask.ext.sqlalchemy import get_debug_queries
from app.core.logging import Logging
from app.core.ansible import Ansi
from app.core.models import Users, UserDetails
from passlib.hash import sha512_crypt
from sqlalchemy import func, distinct, exists
from config import DATABASE_QUERY_TIMEOUT, POSTS_PER_PAGE
from flask import abort, jsonify, url_for
from app import app, db
import datetime


@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (query.statement, query.parameters, query.duration, query.context))
    return response


def dump_datetime(value):
    """ Deserialize datetime object into string form for JSON processing. """
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class DatabaseModel():
    def __init__(self, username=None):
        self.username = username
        self.page = 1

    def make_public_user(self, user):
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

    def serialize(self, fields):
        user = [i.serialize for i in fields]
        user = filter(lambda u: u['username'] == self.username, user)
        return user

    def createShellPassword(self, password):
        return sha512_crypt.encrypt(password)

    def getUsersFilteredQuery(self, kwargs):
        """
        Stopping here, working on pagination, its no good
        """
        return Users.query.filter_by(**kwargs).paginate(self.page, POSTS_PER_PAGE, False).items

    def getLogsFilteredQuery(self, kwargs):
        """
        Stopping here, working on pagination, its no good
        """
        return Logging.query.filter_by(**kwargs).paginate(self.page, POSTS_PER_PAGE, False).items

    def getInsertIDofUser(self, user):
        id = Users.query.get(user.id)
        return id

    def databaseInsert(self, data):
        try:
            db.session.add(data)
            db.session.commit()
        except:
            db.session.rollback()
            abort(500)

    def createUser(self, request, created):
        try:
            from app.core.api_views import Api
            api = Api()
            request.json['created'] = created
            request.json['user_details']['user'] = request.json['username']
            create = api.create(
                    db_name=Users,
                    db_join=UserDetails,
                    relationship='username',
                    key='user',
                    **request.json)
            request.json['created'] = dump_datetime(created)
            request.json['password'] = self.createShellPassword(request.json['password'])
            user = self.getUserByUsername(request.json['username'])[0]
            user['password'] = self.createShellPassword(request.json['password'])
            Ansi("useradd").run({'user':user})
            user['password'] = request.json['password']
            from app.core.api_internal.views import Internal
            internal = Internal()
            internal.post(
                     endpoint='logging',
                     dictionary={
                         "logging_details":{
                             "module":"users",
                             "action":"create",
                             "message":"created user {0}".format(
                                request.json['username']
                                ),
                             },
                         "status":"success"}
                     )
        except:
            db.session.rollback()
            from app.core.api_internal.views import Internal
            internal = Internal()
            internal.post(
                     endpoint='logging',
                     dictionary={
                         "logging_details":{
                             "module":"users",
                             "action":"create",
                             "message":"an error occurred when create the user: {0}".format(
                                request.json['username']
                                ),
                             },
                         "status":"error"}
                     )
            abort(500)
        return user

    def appendUserDetails(self, request):
        try:
            from app.core.api_internal.views import Internal
            internal = Internal()
            user = internal.get(endpoint='users', field=self.username)['username'][0]
            print user
            if len(user) == 0:
                abort(404)
            if not request.json:
                print 'broken' + request.json
                abort(400)
            user['password'] = 'Password has been updated'
            user['sudoer'] = request.json.get('sudoer', user['sudoer'])
            user['shell'] = request.json.get('shell', user['shell'])
            updates = {}
            for check in request.json:
                if request.json[check]:
                    updates[check] = request.json[check]
            db.session.query(Users).filter(Users.username==self.username).update(updates)
            db.session.commit()
            if request.json['password']:
                user['password'] = self.createShellPassword(request.json['password'])
            update = Ansi("useradd").run({'user':user})
            user['password'] = request.json['password']
            internal.post(
                     endpoint='logging',
                     dictionary={
                         "logging_details":{
                             "module":"users",
                             "action":"update",
                             "message":"updated user {0}".format(
                                self.username
                                ),
                             },
                         "status":"success"}
                     )
            return user
        except Exception, e:
            print e
            db.session.rollback()
            from app.core.api_internal.views import Internal
            internal = Internal()
            internal.post(
                     endpoint='logging',
                     dictionary={
                         "logging_details":{
                             "module":"users",
                             "action":"update",
                             "message":"failed to update user {0}".format(
                                self.username
                                ),
                             },
                         "status":"success"}
                     )
            #abort(500)

    def validateUser(self):
        if Users.query.filter(Users.username == self.username).count() > 0:
            return True

    def getUserByUsername(self, username=None):
        if username:
            self.username = username
        if self.validateUser():
            user = self.serialize(self.getUsersFilteredQuery({'username':self.username}))
            return user

    def getAllUsers(self, db_name):
        #if db_name == "Users":
        return db_name.query.all()

    def getCount(self):
        return db.session.query(Users.id).count()

    def dataAsJson(self, key, dictionary):
        return jsonify({key: self.make_public_user(dictionary)})

