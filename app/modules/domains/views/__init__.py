from app.core.logging import Logging
from app.core.ansible import Ansi
from app.modules.domains.models import Domains, DomainDetails, DomainSSLDetails
from app.modules.domains.inc import DomainController
from app.modules.users.inc import DatabaseModel
from app.modules.domains.forms import AddDomain, HttpVirtualHost, HttpsVirtualHost, AddSSLDetails
from app.core.common import ModuleController, AttrDict
from flask import Blueprint, jsonify, make_response, url_for, abort, request, render_template, redirect
from app import app, db
import datetime
import json


mod = Blueprint('domains', __name__, url_prefix='/api')
web = Blueprint('web_domains', __name__)

def dump_datetime(value):
    """ Deserialize datetime object into string form for JSON processing. """
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

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
    if request.json['domain_ssl_details']:
        ssl_details = request.json['domain_ssl_details']
        del request.json['domain_ssl_details']
        dc = DomainController(request)
        domain = dc.create()
        print 'inside create_domain'
        request.json['domain_ssl_details'] = ssl_details
        dc = DomainController(
                request=request,
                database=DomainSSLDetails,
                key='domain_ssl'
                )
        domain = dc.create_csr()
#        return dc.dataAsJson(
#                key='domain',
#                dictionary=domain
#                )
    else:
        dc = DomainController(request)
        domain = dc.create()

    #ansi = Ansi("domain")
    """ Create a new domain """
    # Grab a user and check if it exists.  If it does, kick to 409 response
    from app.core.api_views import Api
    api = Api()

    return api.getByFields(
            db_name=Domains,
            page=1,
            key='domain',
            kwargs={'domain_name':request.json['domain_name']}
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

@web.route('/domains', methods=['GET'])
@web.route('/domains/<int:page>', methods=['GET'])
def domains(page=1):
    """ Get a list of all the users that have been added """
    return render_template(
            'domain_list.html',
            title="Domains",
            )

@web.route('/domains/<domain>', methods=['GET','POST'])
def domain(domain):
    """ Get a list of all the users that have been added """
    dc = DomainController()
    form = AddDomain()
    ssl_form = AddSSLDetails()
    httpvh = HttpVirtualHost()
    httpsvh = HttpsVirtualHost()
    if httpvh.validate_on_submit:
        if httpvh.http.data:
            dc.writeVhost(domain, 'http', httpvh.http.data)
    if httpsvh.validate_on_submit:
        if httpsvh.https.data:
            dc.writeVhost(domain, 'https', httpsvh.https.data)
    if ssl_form.validate_on_submit:
        if ssl_form.country.data \
                and ssl_form.state.data \
                and ssl_form.city.data \
                and ssl_form.company.data \
                and ssl_form.department.data:
            request = AttrDict()
            request.json = {
                    "domain_name":domain,
                    'domain_ssl_details': {
                        'country':ssl_form.country.data,
                        'state':ssl_form.state.data,
                        'city':ssl_form.city.data,
                        'company':ssl_form.company.data,
                        'department':ssl_form.department.data,
                        }
                    }
            dc = DomainController(
                    request=request,
                    database=DomainSSLDetails,
                    key='domain_ssl'
                    )
            dc.create_csr()
    httpvh.http.data = dc.openVhost('http', domain)
    httpsvh.https.data = dc.openVhost('https', domain)
    csr = dc.openCsr(domain)
    return render_template(
            'domain_details.html',
            title=domain,
            form=form,
            domain=json.loads(get_domain(domain_name=domain).data),
            http=dc.openVhost('http', domain),
            https=dc.openVhost('https', domain),
            php=dc.openPhp(domain),
            httpvh=httpvh,
            httpsvh=httpsvh,
            ssl_form=ssl_form,
            csr=csr
            )

@web.route('/domains/add', methods=['GET','POST'])
def domain_add():
    """ Get a list of all the users that have been added """
    form = AddDomain()
    if form.validate_on_submit:
        if form.domain.data:
            request = AttrDict()
            request.json = {"domain_name":form.domain.data}
            dc = DomainController(request)
            dc.create()
            return redirect(url_for('web_domains.domain', domain=form.domain.data))
    return render_template(
            'domain_add.html',
            title="Add New Domain",
            form=form,
            )
