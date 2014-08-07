from flask.ext.sqlalchemy import get_debug_queries
from app.core.logging import Logging
from app.core.ansible import Ansi
#from app.modules.domains.models import Domains, DomainDetails
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


class ModuleController():
    def __init__(self, main_db, details_db, key, relationship, domain_name):
        self.main_db = main_db
        self.details_db = details_db
        self.key = key
        self.relationship = relationship
        self.page = 1
        self.field = None
        self.domain_name = domain_name

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

    def make_public_domain(self, domain):
        new_domain = {}
        for field in domain:
            if field == 'domain_name':
                new_domain['uri'] = url_for(
                        'domains.get_domain',
                        domain_name=domain['domain_name'],
                        _external=True
                        )
            else:
                new_domain[field] = domain[field]
        return new_domain

    def serialize(self, fields):
        domain = [i.serialize for i in fields]
        domain = filter(lambda d: d['domain_name'] == self.domain_name, domain)
        return domain

    def getFilteredQuery(self, kwargs):
        """
        Stopping here, working on pagination, its no good
        """
        return self.main_db.query.filter_by(**kwargs).paginate(self.page, POSTS_PER_PAGE, False).items

    def getInsertIDofField(self, field):
        id = self.main_db.query.get(field.id)
        return id

    def databaseInsert(self, data):
        try:
            db.session.add(data)
            db.session.commit()
        except:
            db.session.rollback()
            abort(500)

    def create(self, request, created):
        try:
            from app.core.api_views import Api
            api = Api()
            request.json['created'] = created
            details = self.key + "_details"
            request.json[details][self.key] = request.json[self.relationship]
            print request
            #create = api.create(
            #        db_name=self.main_db,
            #        db_join=self.details_db,
            #        relationship=self.relationship,
            #        key=self.key,
            #        **request.json)
            request.json['created'] = dump_datetime(created)
            #domain = self.getByField(field=request.json[self.relationship])[0]
            #Ansi("domain").run({'user':user})
            from app.core.api_internal.views import Internal
            #internal = Internal()
            #internal.post(
            #         endpoint='logging',
            #         dictionary={
            #             "logging_details":{
            #                 "module":"domains",
            #                 "action":"create",
            #                 "message":"created domain {0}".format(
            #                    request.json[self.relationship]
            #                    ),
            #                 },
            #             "status":"success"}
            #         )
            #return domain
        except Exception, e:
            db.session.rollback()
            from app.core.api_internal.views import Internal
            internal = Internal()
            internal.post(
                     endpoint='logging',
                     dictionary={
                         "logging_details":{
                             "module":"domains",
                             "action":"create",
                             "message":"an error occurred when create the domain: {0} - {1}".format(
                                request.json[self.relationship, e]
                                ),
                             },
                         "status":"error"}
                     )
            abort(500)

#    def appendUserDetails(self, request):
#        try:
#            from app.core.api_internal.views import Internal
#            internal = Internal()
#            user = internal.get(endpoint='users', field=self.username)['username'][0]
#            from app.core.api_views import Api
#            api = Api()
#            print user
#            if len(user) == 0:
#                abort(404)
#            if not request.json:
#                print 'broken' + request.json
#                abort(400)
#            user['password'] = 'Password has been updated'
#            user['sudoer'] = request.json.get('sudoer', user['sudoer'])
#            user['shell'] = request.json.get('shell', user['shell'])
#            updates = {}
#            for check in request.json:
#                if request.json[check]:
#                    updates[check] = request.json[check]
#            db.session.query(Users).filter(Users.username==self.username).update(updates)
#            db.session.commit()
#            if request.json['password']:
#                user['password'] = self.createShellPassword(request.json['password'])
#            update = Ansi("useradd").run({'user':user})
#            user['password'] = request.json['password']
#            internal.post(
#                     endpoint='logging',
#                     dictionary={
#                         "logging_details":{
#                             "module":"users",
#                             "action":"update",
#                             "message":"updated user {0}".format(
#                                self.username
#                                ),
#                             },
#                         "status":"success"}
#                     )
#            return user
#        except Exception, e:
#            print e
#            db.session.rollback()
#            from app.core.api_internal.views import Internal
#            internal = Internal()
#            internal.post(
#                     endpoint='logging',
#                     dictionary={
#                         "logging_details":{
#                             "module":"users",
#                             "action":"update",
#                             "message":"failed to update user {0}".format(
#                                self.username
#                                ),
#                             },
#                         "status":"success"}
#                     )
#            #abort(50

    def validateUser(self):
        if Users.query.filter(Users.username == self.username).count() > 0:
            return True

    def getByField(self, field=None):
        if field:
            self.field = field
        #if self.validateUser():
        return self.serialize(self.getFilteredQuery({self.key+"_name":self.field}))
        #    return user

    def getAllUsers(self, db_name):
        #if db_name == "Users":
        return db_name.query.all()

    def getCount(self):
        return db.session.query(Users.id).count()

    def dataAsJson(self, key, dictionary):
        return jsonify({key: self.make_public_domain(dictionary)})

