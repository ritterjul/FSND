from flask import Flask, jsonify
from models import setup_db, Plant # predefined database
from flask_cors import CORS

def create_app(test_conig=None):
    app = Flask(__name__)
    setup_db(app)

    # initialize CORS with default options
    CORS(app)
    # initialize CORS with resource-specific usage
    #cors = CORS(app, resources={r'*/api/*': {'origins': '*'}})

    # attach CORS headers to response
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    @cross_origin() # enable CORS specifically for route
    def hello():
        return jsonify({'message': 'HELLO WORLD'})

    @app.route('/smiley')
    def smiley():
        return ':)'   

    return app



