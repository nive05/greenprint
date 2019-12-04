"""
Accounts Service

Paths:
------
GET /accounts - Returns a list all of the accounts
GET /accounts/{id} - Returns the account with a given id number
POST /accounts - creates a new account record in the database
PUT /accounts/{id} - updates an account record in the database
DELETE /accounts/{id} - deletes an account record in the database
GET /accounts/{owner} - Returns the accounts with a given owner
GET /accounts/{account_id} - Returns the accounts with a given account id number
GET /accounts/{account_type} - Returns the accounts with a given account type
GET /accounts/{institution_id} - Returns the accounts with a given institution id number
GET /accounts/{balance} - Returns the accounts with a given balance
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import account, DataValidationError

# Import Flask application
from . import app

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)

@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_400_BAD_REQUEST,
                   error='Bad Request',
                   message=message), status.HTTP_400_BAD_REQUEST

@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_404_NOT_FOUND,
                   error='Not Found',
                   message=message), status.HTTP_404_NOT_FOUND

@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                   error='Method not Allowed',
                   message=message), status.HTTP_405_METHOD_NOT_ALLOWED

@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                   error='Unsupported media type',
                   message=message), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = str(error)
    app.logger.error(message)
    return jsonify(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   error='Internal Server Error',
                   message=message), status.HTTP_500_INTERNAL_SERVER_ERROR


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Root URL response """
    return jsonify(name='Account Demo REST API Service',
                   version='1.0',
                   paths=url_for('list_accounts', _external=True)
                  ), status.HTTP_200_OK

######################################################################
# LIST ALL PETS
######################################################################
@app.route('/accounts', methods=['GET'])
def list_pets():
    """ Returns all of the accounts """
    app.logger.info('Request for account list')
    accounts = []
    account_id = request.args.get('account_id')
    owner = request.args.get('owner')
    account_type = request.args.get('account_type')
    institution_id = request.args.get('institution_id')
    balance = request.args.get('balance')

    if account_id:
        accounts = account.find_by_account_id(account_id)
    elif owner:
        accounts = account.find_by_owner(owner)
    elif account_type:
        accounts = account.find_by_account_type(account_type)
    elif institution_id:
        accounts = account.find_by_institution_id(institution_id)
    elif balance:
        accounts = account.find_by_balance(balance)
    else:
        accounts = account.all()

    results = [account.serialize() for account in accounts]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE AN ACCOUNT BY ID
######################################################################
@app.route('/account/<int:accountid>', methods=['GET'])
def get_accounts(accountid):
    """
    Retrieve a single account

    This endpoint will return a account based on it's account id
    """
    app.logger.info('Request for account with id: %s', accountid)
    account = account.find(accountid)
    if not account:
        raise NotFound("Account with id '{}' was not found.".format(accountid))
    return make_response(jsonify(account.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW ACCOUNT
######################################################################
@app.route('/accounts', methods=['POST'])
def create_accounts():
    """
    Creates an account
    This endpoint will create an account based the data in the body that is posted
    """
    app.logger.info('Request to create an account')
    check_content_type('application/json')
    account = account()
    account.deserialize(request.get_json())
    account.save()
    message = account.serialize()
    location_url = url_for('get_accounts', accountid=account.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
                         })


######################################################################
# UPDATE AN EXISTING PET
######################################################################
@app.route('/accounts/<int:accountid>', methods=['PUT'])
def update_accounts(accountid):
    """
    Update an account

    This endpoint will update an account based the body that is posted
    """
    app.logger.info('Request to update account with id: %s', accountid)
    check_content_type('application/json')
    account = account.find(accountid)
    if not account:
        raise NotFound("Account with id '{}' was not found.".format(accountid))
    account.deserialize(request.get_json())
    account.id = accountid
    account.save()
    return make_response(jsonify(account.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A PET
######################################################################
@app.route('/account/<int:accountid>', methods=['DELETE'])
def delete_accounts(accountid):
    """
    Delete an Account

    This endpoint will delete an account based the id specified in the path
    """
    app.logger.info('Request to delete account with id: %s', accountid)
    account = account.find(accountid)
    if account:
        account.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    account.init_db(app)

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(415, 'Content-Type must be {}'.format(content_type))

def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print('Setting up logging...')
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.propagate = False
        app.logger.info('Logging handler established')

######################################################################
# RETRIEVE AN ORDER BASED ON OWNER
######################################################################

@app.route('/accounts/owner/<str:owner>', methods=['GET'])
def get_orders_owner(owner):
    """
    Retrieve an account
    This endpoint will return an account based on it's owner
    """
    print(owner)
    app.logger.info('Request for account list based on owner: %s', owner)
    accounts = account.find_by_owner(owner)
    if not accounts:
        raise NotFound("Account with owner '{}' was not found.".format(owner))
    else:
        results = [account.serialize() for account in accounts]
        return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE AN ORDER BASED ON ACCOUNT ID
######################################################################

@app.route('/accounts/account_id/<int:account_id>', methods=['GET'])
def get_orders_account_id(account_id):
    """
    Retrieve an account
    This endpoint will return an account based on it's account id
    """
    print(account_id)
    app.logger.info('Request for account list based on acccount id: %s', account_id)
    accounts = account.find_by_account_id(account_id)
    if not accounts:
        raise NotFound("Account with account id '{}' was not found.".format(account_id))
    else:
        results = [account.serialize() for account in accounts]
        return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE AN ORDER BASED ON ACCOUNT TYPE
######################################################################

@app.route('/accounts/account_type/<str:account_type>', methods=['GET'])
def get_orders_account_type(account_type):
    """
    Retrieve an account
    This endpoint will return an account based on it's account type
    """
    print(account_type)
    app.logger.info('Request for account list based on acccount type: %s', account_type)
    accounts = account.find_by_account_type(account_type)
    if not accounts:
        raise NotFound("Account with account type '{}' was not found.".format(account_type))
    else:
        results = [account.serialize() for account in accounts]
        return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE AN ORDER BASED ON INSTITUTION ID
######################################################################

@app.route('/accounts/account_id/<int:institution_id>', methods=['GET'])
def get_orders_institution_id(institution_id):
    """
    Retrieve an account
    This endpoint will return an account based on it's institution id
    """
    print(institution_id)
    app.logger.info('Request for account list based on institution id: %s', institution_id)
    accounts = account.find_by_institution_id(institution_id)
    if not accounts:
        raise NotFound("Account with institution id '{}' was not found.".format(institution_id))
    else:
        results = [account.serialize() for account in accounts]
        return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE AN ORDER BASED ON BALANCE
######################################################################

@app.route('/accounts/balance/<str:balance>', methods=['GET'])
def get_orders_balance(balance):
    """
    Retrieve an account
    This endpoint will return an account based on it's balance
    """
    print(balance)
    app.logger.info('Request for account list based on balance: %s', balance)
    accounts = account.find_by_balance(balance)
    if not accounts:
        raise NotFound("Account with balance '{}' was not found.".format(balance))
    else:
        results = [account.serialize() for account in accounts]
        return make_response(jsonify(results), status.HTTP_200_OK)
