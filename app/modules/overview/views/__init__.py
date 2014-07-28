from app.core.logging import Logging
from app.core.ansible import Ansi
from app.modules.domains.models import Domains, DomainDetails
from app.core.logging import Logging, LoggingDetails
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

mod = Blueprint('overview', __name__, url_prefix='/api')

@mod.route('/overview/count', methods=['GET'])
def get_domains():
    """ Get a list of all the users that have been added """
    from app.core.api_views import Api
    api = Api()
    return api.getOverviewCount(
            db_name=LoggingDetails,
            field='success',
            key='logs',
            )
