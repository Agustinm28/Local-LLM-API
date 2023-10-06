from flask_restx import Namespace, Resource
from flask import request
from utils.load_model import get_models, set_model, see_models, download_model
import time
from auth.authentication import *

LLMmodels = Namespace('models', description='Model related operations')

@LLMmodels.route('/')
class Models(Resource):
    @require_api_key
    def get(self):
        '''
        Method to get the models available in the models folder.
            - Requires an API key in the request header.
        '''
        start_time = time.time()
        try:
            models = get_models()
        except Exception as e:
            error_message = str(e)
            return LLMmodels.abort(500, error_message)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time in seconds: {execution_time}")

        return {"models": models}
    
@LLMmodels.route('/model')
class Model(Resource):
    @require_api_key
    def post(self):
        '''
        Method to set the model to be used for predictions.
            - Requires an API key in the request header.
        '''
        start_time = time.time()

        request_data = request.get_json()
        model_name = request_data.get("model")

        try:
            model = set_model(model_name)
        except Exception as e:
            error_message = str(e)
            return LLMmodels.abort(500, error_message)
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time in seconds: {execution_time}")

        return {"model_status": model}

@LLMmodels.route('/download')
class Downloads(Resource):
    @require_api_key
    def get(self):
        '''
        Method to get the models available for download in the models.json file.
            - Requires an API key in the request header.
        '''
        start_time = time.time()
        try:
            models = see_models()
        except Exception as e:
            error_message = str(e)
            return LLMmodels.abort(500, error_message)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time in seconds: {execution_time}")

        return {"models": models}
    
    @require_api_key
    def post(self):
        '''
        Method to download a model locally.
            - Requires an API key in the request header.
        '''
        start_time = time.time()

        request_data = request.get_json()
        model_name = request_data.get("model")

        try:
            model = download_model(model_name)
        except Exception as e:
            error_message = str(e)
            return LLMmodels.abort(500, error_message)
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time in seconds: {execution_time}")

        return {"model": model}