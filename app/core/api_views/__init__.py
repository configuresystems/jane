from app.modules.users.views import mod as users
from flask import make_response, jsonify
from app import app

app.register_blueprint(users)

@app.route('/')
def index():
    return "hello world"

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error':'Bad Request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not Found'}), 404)

@app.errorhandler(409)
def conflict(error):
    return make_response(jsonify({'error':'Entity Exists'}), 409)

@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error':'Internal Server Error'}), 500)

