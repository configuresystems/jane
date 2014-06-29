from flask.ext.sqlalchemy import get_debug_queries
from app.core.logging import Logging
from app.core.ansible import Ansi
from app.core.models import Users, UserDetails
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


class DatabaseModel():
    def __init__(self, username=None):
        self.username = username
        self.page = 1

    def make_public_user(self, user):
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

    def serialize(self, fields):
        user = [i.serialize for i in fields]
        user = filter(lambda u: u['username'] == self.username, user)
        return user

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
            user = {
                    'username': request.json['username'],
                    'domain': request.json.get('domain', ""),
                    'shell': request.json['shell'],
                    'sudoer': request.json['sudoer'],
                    'password': request.json['password'],
                    'created': created,
                    }
            insert = Users(**user)
            self.databaseInsert(insert)
            id = self.getInsertIDofUser(insert)
            user['username'] = id.username
            user['user_details'] = []
            user_details = {
                    'phone': request.json['user_details']['phone'],
                    'company': request.json['user_details']['company'],
                    'last': request.json['user_details']['last'],
                    'first': request.json['user_details']['first'],
                    'email': request.json['user_details']['email'],
                    'user': id.username
                    }
            user['user_details'].append(user_details)
            details = UserDetails(**user_details)
            self.databaseInsert(details)
            self.insertLog(
                    type="add",
                    action="create",
                    message="created user {0}".format(
                        request.json['username']
                        ),
                    )
        except:
            db.session.rollback()
            self.insertLog(
                    type="error",
                    action="create",
                    message="could not create {0}".format(
                        request.json['username']
                        ),
                    )
            #abort(500)
        return user

    def appendUserDetails(self, updates):
        try:
            db.session.query(Users).filter(Users.username==self.username).update(updates)
            db.session.commit()
            self.insertLog(
                    type="add",
                    action="update",
                    message="{0} has been updated".format(
                        self.username,
                        ),
                    )
        except:
            self.insertLog(
                    type="error",
                    action="update",
                    message="an error occurred when trying to update user {0}".format(
                        self.username,
                        ),
                    )
            abort(500)

    def validateUser(self):
        if Users.query.filter(Users.username == self.username).count() > 0:
            return True

    def getUserByUsername(self):
        if self.validateUser():
            user = self.serialize(self.getUsersFilteredQuery({'username':self.username}))
            return user

    def getAllUsers(self, db_name):
        if db_name == "Users":
            return Users.query.all()

    def getCount(self):
        return db.session.query(Users.id).count()

    def dataAsJson(self, key, dictionary):
        return jsonify({key: self.make_public_user(dictionary)})

    def insertLog(self, type, action, message):
        try:
            created = datetime.datetime.utcnow()
            log = {
                    'timestamp': created,
                    'type': type,
                    'action': action,
                    'module': 'users',
                    'message': message
                    }
            insert = Logging(**log)
            db.session.add(insert)
            db.session.commit()
        except:
            abort(505)

    def getLogs(self):
        return Logging.query.all()

    def getUserLogCount(self):
        return db.session.query(Logging.id, Logging.module).count()
        #return db.session.query(func.count(Logging.id)).\
        #                group_by(Logging.module)

