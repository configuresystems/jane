from flask.ext.sqlalchemy import get_debug_queries
from app.core.logging import Logging
from app.core.ansible import Ansi
from app.modules.domains.models import Domains, DomainDetails, DomainSSLDetails
from app.core.common import ModuleController
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
        return
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class DomainController():
    def __init__(self, request=None, database=DomainDetails, key='domain'):
        if request:
            self.request = request
            self.mc = ModuleController(
                    main_db=Domains,
                    details_db=database,
                    relationship='domain_name',
                    key=key,
                    name=self.request.json['domain_name']
                    )

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

    def dataAsJson(self, key, dictionary):
        return jsonify({key: self.make_public_domain(dictionary)})

    def checkFields(self):
        if not self.request.json or not 'domain_name' in self.request.json:
            abort(404)
        if not 'domain_details' in self.request.json:
            self.request.json['domain_details'] = {}
        if not 'group' in self.request.json['domain_details']:
            self.request.json['domain_details']['group'] = 'apache'
        if not 'owner' in self.request.json['domain_details']:
            self.request.json['domain_details']['owner'] = 'apache'
        if not 'port' in self.request.json['domain_details']:
            self.request.json['domain_details']['port'] = '80'
        if not 'document_root' in self.request.json['domain_details']:
            self.request.json['domain_details']['document_root'] = '/var/www/vhosts/'+self.request.json['domain_name']
        return True

    def create(self):
        created = datetime.datetime.utcnow()
        if self.checkFields():
            ansi = Ansi("domain")
            ansi.run(self.request)
            return self.mc.create(self.request, created)
        else:
            abort(500)

    def create_csr(self):
        created = datetime.datetime.utcnow()
        if self.checkFields():
            ansi = Ansi("csr")
            ansi.run(self.request)
            self.request.json['domain_ssl_details']['csr'] = self.openCsr(
                    domain=self.request.json['domain_name']
                    )
            return self.mc.create(self.request, created)
        else:
            abort(500)

    def openFile(self, filepath):
        try:
            with open(filepath, 'r') as f:
                data = f.read()
                return data
        except Exception, e:
            print 'file does not exist '+filepath

    def openVhost(self, protocol, domain):
        path  = '/var/www/vhosts/{0}/conf/{1}.{0}.conf'.format(domain, protocol)
        return self.openFile(path)

    def openPhp(self, domain):
        path  = '/var/www/vhosts/{0}/etc/php.ini'.format(domain)
        return self.openFile(path)

    def openCsr(self, domain):
        path  = '/var/www/vhosts/{0}/ssl/{0}.csr'.format(domain)
        return self.openFile(path)

    def saveFile(self, file, data):
        if data:
            with open(file, 'w') as f:
                f.write(data)

    def writeVhost(self, domain, protocol, data):
        path = '/var/www/vhosts/{0}/conf/{1}.{0}.conf'.format(domain, protocol)
        self.saveFile(path, data)
