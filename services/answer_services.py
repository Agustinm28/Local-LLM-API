from flask_restx import Namespace, Resource
from flask import request
from utils.load_model import load_model, generate_gpu_text
import time
import copy
from auth.authentication import *

answer = Namespace('answer', description='Answer related operations')

@answer.route('/')
class Answer(Resource):
    @require_api_key
    def post(self):
        '''
        Method to get an answer from the model throug CPU with llama_cpp.
            - Requires an API key in the request header.
        '''
        start_time = time.time()
        try:
            llm = load_model()
        except Exception as e:
            error_message = str(e)
            return answer.abort(500, error_message)

        request_data = request.get_json()
        prompt = request_data.get("prompt")

        if not prompt:
            return answer.abort(400, "Question not provided in the request")

        # Response structure compatible with llama-2 and vicuna
        stream = llm(
            f"Instruction: {prompt}\nResponse:",
            max_tokens=10000,
            # stop=["\n","Q:"], # Stops the generation when prompt finds a Q: or a \n
            echo=True,
        )

        result = copy.deepcopy(stream)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time in seconds: {execution_time}")

        return {"result": result}
    
@answer.route('/gpu')
class GPUAnswer(Resource):
    @require_api_key
    def post(self):
        '''
        Method to get an answer from the model throug GPU with transformers.
            - Requires an API key in the request header.
            - Requires a valid GPTQ model.
        '''
        start_time = time.time()
        
        request_data = request.get_json()
        prompt = request_data.get("prompt")

        if not prompt:
            return answer.abort(400, "Question not provided in the request")
        
        try:
            answer = generate_gpu_text(
                prompt=prompt,
                temperature=0.7,
                max_length=2000,
                do_sample=True
            )
        except Exception as e:
            error_message = str(e)
            return answer.abort(500, error_message)
        
        result = copy.deepcopy(answer)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time in seconds: {execution_time}")

        return {"result": result}