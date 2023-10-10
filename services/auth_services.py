from flask_restx import Namespace, Resource
from flask import request
import time
from auth.authentication import *

Auth = Namespace('auth', description='Auth related operations')

@Auth.route('/')
class Authentication(Resource):
    @require_api_key
    def get(self):
        '''
        Method to check if the API key is valid.
            - Requires an API key in the request header.
        '''
        return {"auth": True}
    
@Auth.route('/key')
class Key(Resource):
    @require_master_key
    def get(self):
        '''
        Method to generate a new API key.
            - Requires a master API key in the request header. The master API key is the first API key generated, with key 0.
        '''
        try:
            key_request = generate_api_key()
        except Exception as e:
            error_message = str(e)
            return Auth.abort(500, error_message)

        return {"key": key_request}
from flask_restx import Namespace, Resource
from flask import request
import time
from auth.authentication import *

Auth = Namespace('auth', description='Auth related operations')

@Auth.route('/')
class Authentication(Resource):
    @require_api_key
    def get(self):
        '''
        Method to check if the API key is valid.
            - Requires an API key in the request header.
        '''
        return {"auth": True}
    
@Auth.route('/key')
class Key(Resource):
    @require_master_key
    def get(self):
        '''
        Method to generate a new API key.
            - Requires a master API key in the request header. The master API key is the first API key generated, with key 0.
        '''
        try:
            key_request = generate_api_key()
        except Exception as e:
            error_message = str(e)
            return Auth.abort(500, error_message)

        return {"key": key_request}