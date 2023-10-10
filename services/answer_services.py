from flask_restx import Namespace, Resource
from flask import request
from utils.load_model import load_model
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory.entity import SQLiteEntityStore
import time
import copy
from auth.authentication import *
from queue import Queue
from threading import Thread

answer = Namespace('answer', description='Answer related operations')

memory = None
llm = None
running_thread = None
queue = Queue()

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

        if not llm:
            try:
                llm, template = load_model()
                memory = ConversationBufferWindowMemory(k=1, memory_key="chat_history")
            except Exception as e:
                error_message = str(e)
                return answer.abort(500, error_message)

        request_data = request.get_json()
        question = request_data.get("prompt")

        if not question:
            return answer.abort(400, "Question not provided in the request")

        # Create prompt from template
        ## input_variables reads the variables from the template
        
        prompt = PromptTemplate(template=template, input_variables=["history", "input"])
        conversation_chain = LLMChain(prompt=prompt, llm=llm, memory=memory, verbose=True)

        # Run the chain and get the stream
        stream = conversation_chain.predict(input=question)

        result = copy.deepcopy(stream)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time in seconds: {execution_time}")

        return {"result": result}