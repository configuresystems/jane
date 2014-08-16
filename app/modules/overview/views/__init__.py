from app.core.logging import Logging
from app.core.ansible import Ansi
from app.modules.domains.models import Domains, DomainDetails
from app.core.logging import Logging, LoggingDetails
from app.modules.users.inc import DatabaseModel
from app.core.common import ModuleController
from flask import Blueprint, jsonify, make_response, url_for, abort, request, render_template
from app import app, db
import datetime
import json


def dump_datetime(value):
    """ Deserialize datetime object into string form for JSON processing. """
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

mod = Blueprint('overview', __name__, url_prefix='/api')
web = Blueprint('web_overview', __name__)

@mod.route('/overview/count', methods=['GET'])
def get_count_overview():
    """ Get a list of all the users that have been added """
    from app.core.api_views import Api
    api = Api()
    return api.getOverviewCount(
            db_name=LoggingDetails,
            field='success',
            key='logs',
            )

@web.route('/', methods=['GET'])
@web.route('/overview', methods=['GET'])
def get_overview():
    """ Get a list of all the users that have been added """
    from app.core.api_views import Api
    from app.modules.overview import inc
    sar = inc.main()
    api = Api()
    return render_template("index.html",
            sar=sar,
            )
