from app.core.logging import Logging
from app.core.ansible import Ansi
from app.modules.domains.models import Domains, DomainDetails
from app.modules.users.inc import DatabaseModel
from app.core.common import ModuleController
from flask import Blueprint, jsonify, make_response, url_for, abort, request
from app import app, db
import datetime
import json


def dump_datetime(value):
    """ Deserialize datetime object into string form for JSON processing. """
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

mod = Blueprint('domains', __name__, url_prefix='/api')
def make_public_domain(domain):
    new_domain = {}
    for field in domain:
        if field == 'domain_name':
            new_user['uri'] = url_for(
                    'domains.get_domain',
                    domain_name=domain['domain_name'],
                    _external=True
                    )
        else:
            new_domain[field] = domain[field]
    return new_domain

@mod.route('/domains', methods=['GET'])
@mod.route('/domains/<int:page>', methods=['GET'])
def get_domains(page=1):
    """ Get a list of all the users that have been added """
    from app.core.api_views import Api
    api = Api()
    return api.getList(
            db_name=Domains,
            page=page,
            key='domains'
            )

@mod.route('/domains/<domain_name>', methods=['GET'])
@mod.route('/domains/<domain_name>/<int:page>', methods=['GET'])
def get_domain(domain_name, page=1):
    """ Get a specific user from the database """
    from app.core.api_views import Api
    api = Api()
    return api.getByFields(
            db_name=Domains,
            page=page,
            key='domain',
            kwargs={'domain_name':domain_name}
            )

@mod.route('/domains', methods=['POST'])
def create_domain():
    #ansi = Ansi("domain")
    """ Create a new domain """
    if not request.json or not 'domain_name' in request.json:
        abort(404)
    # Grab a user and check if it exists.  If it does, kick to 409 response
    mc = ModuleController(
            main_db=Domains,
            details_db=DomainDetails,
            relationship='domain_name',
            key='domain',
            name=request.json['domain_name']
            )
    created = datetime.datetime.utcnow()
    domain = mc.create(request, created)
    Ansi("domain").run({'domain':domain})
    return mc.dataAsJson(
            key='domain',
            dictionary=domain
            )

#@mod.route('/users/<username>', methods=['PUT'])
#def update_task(username):
#    """ update User information """
#    dm = DatabaseModel(username=username)
#    #user = dm.appendUserDetails(request)
#    return  dm.dataAsJson(
#            key='user',
#            dictionary=user
#            )

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

