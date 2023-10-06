from flask_restx import Namespace, Resource
from flask import request
from utils.load_model import load_model
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import time
import copy
from auth.authentication import *

answer = Namespace('answer', description='Answer related operations')
llm = None
template = None

@answer.route('/')
class Answer(Resource):
    @require_api_key
    def post(self):
        start_time = time.time()
        global llm
        global template

        if not llm:
            try:
                llm, template = load_model('Vicuna-13b')
            except Exception as e:
                error_message = str(e)
                return answer.abort(500, error_message)

        request_data = request.get_json()
        question = request_data.get("prompt")

        if not question:
            return answer.abort(400, "Question not provided in the request")

        # Create prompt from template
        ## input_variables reads the variables from the template
        prompt = PromptTemplate(template=template, input_variables=["prompt"])
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        # Run the chain and get the stream
        stream = llm_chain.run(question)

        result = copy.deepcopy(stream)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time in seconds: {execution_time}")

        return {"result": result}