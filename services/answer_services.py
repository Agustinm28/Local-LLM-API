from flask_restx import Namespace, Resource
from flask import request
from utils.load_model import load_model
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationEntityMemory
from langchain.memory.entity import SQLiteEntityStore
import time
import copy
from auth.authentication import *

answer = Namespace('answer', description='Answer related operations')

memory = None
llm = None
template = None

@answer.route('/')
class Answer(Resource):
    @require_api_key
    def post(self):
        '''
        Method to get the answer to a question.
            - Requires an API key in the request header.
            - Requires a question in the request body.
        '''
        start_time = time.time()
        
        global llm
        global template
        global memory
        entity_store = SQLiteEntityStore()

        if not llm:
            try:
                llm, template = load_model()
                memory = ConversationEntityMemory(llm=llm, entity_store=entity_store)
            except Exception as e:
                error_message = str(e)
                return answer.abort(500, error_message)

        request_data = request.get_json()
        question = request_data.get("prompt")

        if not question:
            return answer.abort(400, "Question not provided in the request")

        # Create prompt from template
        ## input_variables reads the variables from the template
        prompt = PromptTemplate(template=template, input_variables=["entities", "history", "input"])
        conversation_chain = ConversationChain(prompt=prompt, llm=llm, memory=memory)
        # Run the chain and get the stream
        stream = conversation_chain.run(question)

        result = copy.deepcopy(stream)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time in seconds: {execution_time}")

        return {"result": result}