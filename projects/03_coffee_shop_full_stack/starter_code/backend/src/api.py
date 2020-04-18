import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
db_drop_and_create_all()


@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()

    response = {
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    }
    return jsonify(response)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.all()

    response = {
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    }
    return jsonify(response)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    data = request.get_json()

    try:
        drink = Drink(
            title=data['title'],
            recipe=json.dumps(data['recipe'])
        )
        drink.insert()
        response = {
            'success': True,
            'drinks': [drink.long()]
        }
        return jsonify(response)
    except:
        abort(400)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if not drink:
        abort(404)

    data = request.get_json()

    try:
        if 'title' in data:
            drink.title = data['title']
        if 'recipe' in data:
            drink.recipe = json.dumps(data['recipe'])

        response = {
            'success': True,
            'drinks': [drink.long()]
        }
        return jsonify(response)
    except:
        abort(400)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if not drink:
        abort(404)

    drink.delete()
    response = {
        'success': True,
        'delete': drink_id
    }
    return jsonify(response)


'''
Error handling
'''


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable entity"
    }), 422
