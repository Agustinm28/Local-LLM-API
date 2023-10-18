from flask_restx import Namespace, Resource
from flask import request
from utils.load_model import get_models, set_model
import time
from auth.authentication import *
from colorama import Fore as c

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
        print(f"\n[ {c.WHITE}MODEL{c.RESET} ] Execution time in seconds: {execution_time}\n")

        return {"models": models}
    
@LLMmodels.route('/model')
class Model(Resource):
    @require_api_key
    def post(self):
        '''
        Method to set the model to be used for predictions.
            - Requires an API key in the request header.
            - Requires a model name in the request body.
            - Requires a model config name in the request body. You can set the model config name in the config.json file in data.
        '''
        start_time = time.time()

        request_data = request.get_json()
        model_name = request_data.get("model")
        model_config_name = request_data.get("model_config")

        if not model_name:
            return LLMmodels.abort(400, "No model name provided")
        if not model_config_name:
            return LLMmodels.abort(400, "No model config name provided")

        try:
            model = set_model(
                model_config_name=model_config_name, 
                model_name=model_name
                )
        except Exception as e:
            error_message = str(e)
            return LLMmodels.abort(500, error_message)
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\n[ {c.WHITE}MODEL{c.RESET} ] Execution time in seconds: {execution_time}\n")

        return {"model_status": model}