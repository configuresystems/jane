from app.core.logging import Logging, LoggingDetails
from flask import Blueprint, jsonify, make_response, url_for, abort, request
from app import app, db
import datetime
import json


def make_public_log(self, item):
    new = {}
    for field in item:
        if field == 'module':
            new['uri'] = url_for(
                    'logging.get_log',
                    module=user['username'],
                    _external=True
                    )
        else:
            new[field] = item[field]
    return new

mod = Blueprint('logging', __name__, url_prefix='/api')
@mod.route('/logging', methods=['GET'])
@mod.route('/logging/<int:page>', methods=['GET'])
@mod.route('/logging/<status>', methods=['GET'])
@mod.route('/logging/<status>/<module>', methods=['GET'])
def get_logs(page=1, status='', module=''):
    """
    /api/logging                   List all logs in paginated form
    /api/logging/<int:page>        List logs per page
    /api/logging/<status>          List all logs for <module>
    /api/logging/<status>/<module>   List all logs for <module> and <type>
    """

    from app.core.api_views import Api
    api = Api()
    if not status and not module:
        return api.getList(db_name=Logging, page=page, key='logs')
    elif status and not module:
        return api.getByFields(
                db_name=Logging,
                page=page,
                key='logs',
                kwargs={'status':status}
                )
    else:
        return api.getByFields(
                db_name=Logging,
                page=page,
                key='logs',
                kwargs={'status':status, 'module':module}
                )
    abort(404)

@mod.route('/logging', methods=['POST'])
def create_log():
    """
    """
    from app.core.api_views import Api
    api = Api()
    request.json['logging_details']['timestamp'] = datetime.datetime.utcnow()
    request.json['logging_details']['status_code'] = request.json['status']
    create = api.create(db_name=Logging, db_join=LoggingDetails, relationship='status', key='logging', **request.json)
    request.json['logging_details']['timestamp'] = str(request.json['logging_details']['timestamp'])
    return jsonify({'logs':request.json})

