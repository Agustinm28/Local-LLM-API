from flask import Blueprint, jsonify, request, Response
from website.load_model import load_model, get_models, set_model
from website.authentication import *
import copy
import asyncio
from flask_sse import sse
import time

views = Blueprint('views', __name__)

@views.route('/')
@require_api_key
def home():
    return "<h1>Local LLM improved API</h1><p>Use /model to get answer, /stream to stream answer, /models to see available models, /setModel to set a model</p>"

@views.route('/model', methods=['POST'])
@require_api_key
def answer():
    start_time = time.time()
    try:
        llm = load_model()
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500 
    
    request_data = request.get_json()
    question = request_data.get("question")

    if not question:
        return jsonify({"error": "Question not provided in the request"}), 400

    stream = llm(
        f"Question: {question} Answer:",
        max_tokens=10000,
        stop=["Q:"],
        echo=True,
    )
    
    result = copy.deepcopy(stream)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time in seconds: {execution_time}")
    
    return jsonify({"result": result})

@views.route("/stream", methods=['POST'])
@require_api_key
def stream():
    start_time = time.time()
    try:
        llm = load_model()
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500 
    
    request_data = request.get_json()
    question = request_data.get("question")

    if not question:
        return jsonify({"error": "Question not provided in the request"}), 400

    stream = llm(
        f"Question: {question} Answer:",
        max_tokens=10000,
        stop=["Q:"],
        stream=True,
    )

    def event_stream():
        for item in stream:
            result = copy.deepcopy(item)
            text = result["choices"][0]["text"]
            yield f"data: {text}\n\n"

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time in seconds: {execution_time}")

    return Response(event_stream(), mimetype="text/event-stream")

@views.route('/models', methods=['POST', 'GET'])
@require_api_key
def models():
    start_time = time.time()
    try:
        models = get_models()
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500 
    
    print(models)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time in seconds: {execution_time}")
    
    return jsonify({"models": models})

@views.route('/setModel', methods=['POST', 'GET'])
@require_api_key
def req_models():
    start_time = time.time()
    request_data = request.get_json()
    model = request_data.get("model")
    
    try:
        model_request = set_model(model)
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500 

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time in seconds: {execution_time}")
    
    return jsonify({"model_status": model_request})

@views.route('/auth', methods=['POST', 'GET'])
@require_api_key
def auth():
    return jsonify({"auth": True})

@views.route('/getKey', methods=['POST', 'GET'])
@require_master_key
def key():
    
    try:
        key_request = generate_api_key()
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500 

    return jsonify({"key_status": key_request})