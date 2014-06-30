from app.core.logging import Logging
from flask import Blueprint, jsonify, make_response, url_for, abort, request
from app import app, db
import datetime
import json


mod = Blueprint('logging', __name__, url_prefix='/api')
@mod.route('/logging', methods=['GET'])
@mod.route('/logging/<int:page>', methods=['GET'])
@mod.route('/logging/<module>', methods=['GET'])
@mod.route('/logging/<module>/<type>', methods=['GET'])
def get_logs(page=1, module='', type=''):
    """
    /api/logging                   List all logs in paginated form
    /api/logging/<int:page>        List logs per page
    /api/logging/<module>          List all logs for <module>
    /api/logging/<module>/<type>   List all logs for <module> and <type>
    """

    from app.core.api_views import Api
    api = Api()
    if not module and not type:
        return api.getList(db_name=Logging, page=page, key='logs')
    elif module and not type:
        return api.getByFields(
                db_name=Logging,
                page=page,
                key='logs',
                kwargs={'module':module}
                )
    else:
        return api.getByFields(
                db_name=Logging,
                page=page,
                key='logs',
                kwargs={'module':module, 'type':type}
                )

