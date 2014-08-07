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
    def __init__(self, main_db, details_db, key, relationship, name):
        self.main_db = main_db
        self.details_db = details_db
        self.key = key
        self.relationship = relationship
        self.page = 1
        self.field = None
        self.name = name

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

    def make_public_domain(self, fields):
        uri = "{0}s.get_{0}".format(self.key)
        new = {}
        for field in fields:
            if field == self.relationship:
                new_domain['uri'] = url_for(
                        uri,
                        name=fields[self.relationship],
                        _external=True
                        )
            else:
                new_domain[field] = domain[field]
        return new_domain

    def getFilteredQuery(self, kwargs):
        """
        Stopping here, working on pagination, its no good
        """
        return self.main_db.query.filter_by(**kwargs).paginate(self.page, POSTS_PER_PAGE, False).items

    def serialize(self, fields):
        domain = [i.serialize for i in fields]
        domain = filter(lambda d: d[self.relationship] == self.name, domain)
        return domain

    def dataAsJson(self, key, dictionary):
        return jsonify({key: self.make_public_user(dictionary)})

    def getByField(self, field=None):
        if field:
            self.field = field
        return self.serialize(self.getFilteredQuery({self.relationship:self.field}))

    def log(self, module, action, message, status):
        from app.core.api_internal.views import Internal
        internal = Internal()
        internal.post(
                 endpoint='logging',
                 dictionary={
                     "logging_details":{
                         "module":module,
                         "action":action,
                         "message":message,
                         },
                     "status":status}
                 )

    def create(self, request, created):
        try:
            if not 'domain_details' in request.json:
                request.json['domain_details'] = {}
                request.json['domain_details']['group'] = 'apache'
                request.json['domain_details']['owner'] = 'apache'
                request.json['domain_details']['port'] = '80'
                request.json['domain_details']['document_root'] = '/var/www/vhosts/'+request.json['domain_name']
            from app.core.api_views import Api
            api = Api()
            request.json['created'] = created
            details = self.key + "_details"
            request.json[details][self.key] = request.json[self.relationship]
            create = api.create(
                    db_name=self.main_db,
                    db_join=self.details_db,
                    relationship=self.relationship,
                    key=self.key,
                    **request.json)
            request.json['created'] = dump_datetime(created)
            domain = self.getByField(field=request.json[self.relationship])[0]
            #Ansi("domain").run({'user':user})
            self.log(
                    status='success',
                    module=self.key,
                    action='create',
                    message="New {0} created: {1}".format(
                        self.key, self.name
                        )
                    )
            return domain
        except Exception, e:
            db.session.rollback()
            self.log(
                    status='error',
                    module=self.key,
                    action='create',
                    message="New {0} failed to create: {1} :::: {2}".format(
                        self.key, self.name, e
                        )
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
