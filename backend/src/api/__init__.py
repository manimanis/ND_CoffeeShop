import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from ..auth.auth import AuthError, requires_auth
from ..database.models import drinks_list_short, drinks_list_complete, Drink, \
    setup_db


def create_app():
    app = Flask(__name__)
    db = setup_db(app)
    CORS(app)

    # '''
    # @TODO uncomment the following line to initialize the datbase
    # !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    # !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    # '''
    # db_drop_and_create_all()

    # ROUTES ------------------------------------------------------------------
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # '''
    # @TODO implement endpoint
    #     GET /drinks
    #         it should be a public endpoint
    #         it should contain only the drink.short() data representation
    #     returns status code 200 and json {"success": True, "drinks": drinks}
    #     where drinks is the list of drinks or appropriate status code
    #     indicating reason for failure
    # '''
    @app.route('/drinks')
    def get_drinks_short():
        drinks = drinks_list_short(Drink.query.all())
        return jsonify({
            "success": True,
            "drinks": drinks
        })

    # '''
    # @TODO implement endpoint
    #     GET /drinks-detail
    #         it should require the 'get:drinks-detail' permission
    #         it should contain the drink.long() data representation
    #     returns status code 200 and json {"success": True, "drinks": drinks}
    #     where drinks is the list of drinks
    #         or appropriate status code indicating reason for failure
    # '''
    @app.route('/drinks-detail')
    @requires_auth('get:drinks-detail')
    def get_drinks_complete(payload):
        drinks = drinks_list_complete(Drink.query.all())
        return jsonify({
            'success': True,
            'drinks': drinks
        })

    # '''
    # @TODO implement endpoint
    #     POST /drinks
    #         it should create a new row in the drinks table
    #         it should require the 'post:drinks' permission
    #         it should contain the drink.long() data representation
    #     returns status code 200 and json {"success": True, "drinks": drink}
    #     where drink an array containing only the newly created drink
    #         or appropriate status code indicating reason for failure
    # '''
    @app.route('/drinks', methods=['POST'])
    @requires_auth('post:drinks')
    def insert_drink(payload):
        data = request.get_json()
        fields = ['title', 'recipe']
        # check all the fields for the new drink are there
        if not all(field in data for field in fields):
            abort(422)
        else:
            data = {field: data[field] for field in fields}
        old_drink = (Drink
                     .query
                     .filter(db.func.lower(Drink.title) ==
                             data['title'].lower())
                     .first())
        if old_drink is not None:
            abort(422)
        # The data recipe must be a list of dictionaries
        if type(data['recipe']) == dict:
            data['recipe'] = [data['recipe']]
        data['recipe'] = json.dumps(data['recipe'])
        drink = Drink(**data)
        try:
            drink.insert()
            return jsonify({
                'success': True,
                'drinks': [drink.long()]
            })
        except Exception as e:
            print(e)
            abort(400)

    # '''
    # @TODO implement endpoint
    #     PATCH /drinks/<id>
    #         where <id> is the existing model id
    #         it should respond with a 404 error if <id> is not found
    #         it should update the corresponding row for <id>
    #         it should require the 'patch:drinks' permission
    #         it should contain the drink.long() data representation
    #     returns status code 200 and json {"success": True, "drinks": drink}
    #     where drink an array containing only the updated drink
    #         or appropriate status code indicating reason for failure
    # '''
    @app.route('/drinks/<int:drink_id>', methods=['PATCH'])
    @requires_auth('patch:drinks')
    def update_drink(payload, drink_id):
        old_drink = Drink.query.get(drink_id)
        if old_drink is None:
            abort(404)
        data = request.get_json()
        fields = ['title', 'recipe']
        # check all the fields for the updated drink are there
        if not any(field in data for field in fields):
            abort(422)
        if 'title' in data:
            old_drink.title = data['title']
        if 'recipe' in data:
            # The data recipe must be a list of dictionaries
            if type(data['recipe']) == dict:
                data['recipe'] = [data['recipe']]
            old_drink.recipe = json.dumps(data['recipe'])
        try:
            old_drink.update()
            return jsonify({
                'success': True,
                'drinks': [old_drink.long()]
            })
        except Exception:
            abort(400)

    # '''
    # @TODO implement endpoint
    #     DELETE /drinks/<id>
    #         where <id> is the existing model id
    #         it should respond with a 404 error if <id> is not found
    #         it should delete the corresponding row for <id>
    #         it should require the 'delete:drinks' permission
    #     returns status code 200 and json {"success": True, "delete": id}
    #     where id is the id of the deleted record
    #         or appropriate status code indicating reason for failure
    # '''
    @app.route('/drinks/<int:drink_id>', methods=['DELETE'])
    @requires_auth('delete:drinks')
    def delete_drink(payload, drink_id):
        old_drink = Drink.query.get(drink_id)
        if old_drink is None:
            abort(404)
        try:
            old_drink.delete()
            return jsonify({
                'success': True,
                'delete': old_drink.id
            })
        except Exception:
            abort(400)

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        """
        Example error handling for unprocessable entity
        """
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    # '''
    # @TODO implement error handlers using the @app.errorhandler(error)
    #  decorator
    #     each error handler should return (with approprate messages):
    #              jsonify({
    #                     "success": False,
    #                     "error": 404,
    #                     "message": "resource not found"
    #                     }), 404
    # @TODO implement error handler for 400
    #     error handler should conform to general task above
    # @TODO implement error handler for AuthError
    #     error handler should conform to general task above
    # '''
    @app.errorhandler(404)
    def unprocessable(error):
        """
        Example error handling for resource not found entity
        """
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        """
        Example error handling for resource not found entity
        """
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        """
        Example error handling for resource not found entity
        """
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        """
        Example error handling for resource not found entity
        """
        return jsonify({
            "success": False,
            "error": 403,
            "message": "access forbidden"
        }), 403

    return app
