from flask import Blueprint, jsonify, request, Response
from website.load_model import load_model, get_models, set_model, see_models, download_model
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
    prompt = request_data.get("prompt")

    if not prompt:
        return jsonify({"error": "Question not provided in the request"}), 400

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

    return jsonify({"result": result})


@views.route("/stream", methods=['POST'])
@require_api_key
def stream():
    '''
    Method to stream the answer from the model (like GTP model).
        - Requires a json with the question in the request.
        - Requires an API key in the request header.
    '''
    start_time = time.time()
    try:
        llm = load_model()
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500

    request_data = request.get_json()
    prompt = request_data.get("prompt")

    if not prompt:
        return jsonify({"error": "Question not provided in the request"}), 400

    # Response structure compatible with llama-2 and vicuna
    stream = llm(
        f"Instruction: {prompt}\nResponse:",
        max_tokens=10000,
        # stop=["\n","Q:"], # Stops the generation when prompt finds a Q: or a \n
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
    '''
    Method to get the models available in the models folder.
        - Requires an API key in the request header.
    '''
    start_time = time.time()
    try:
        models = get_models()
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time in seconds: {execution_time}")

    return jsonify({"models": models})


@views.route('/downloadModels', methods=['POST', 'GET'])
@require_api_key
def download_models():
    '''
    Method to get the models available for download in the models.json file.
        - Requires an API key in the request header.
    '''
    start_time = time.time()
    try:
        models = see_models()
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time in seconds: {execution_time}")

    return jsonify({"models": models})


@views.route('/downloadModel', methods=['POST', 'GET'])
@require_api_key
def obtain_model():
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
        return jsonify({"error": error_message}), 500

    def download_stream():
        for bar in model:
            if isinstance(bar, str):
                yield bar.encode('utf-8')
            elif isinstance(bar, bytes):
                yield bar
            else:
                #print(f"Skipping unsupported data: {bar}")
                continue

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time in seconds: {execution_time}")

    return Response(download_stream(), mimetype="text/download-stream")



@views.route('/setModel', methods=['POST', 'GET'])
@require_api_key
def req_models():
    '''
    Method to set the model.
        - Requires a json with the model name in the request.
        - Requires an API key in the request header.
    '''
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
    '''
    Method to check if the API key is valid.
        - Requires an API key in the request header.
    '''
    return jsonify({"auth": True})


@views.route('/getKey', methods=['POST', 'GET'])
@require_master_key
def key():
    '''
    Method to generate a new API key.
        - Requires a master API key in the request header. The master API key is the first API key generated, with key 0.
    '''
    try:
        key_request = generate_api_key()
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500

    return jsonify({"key_status": key_request})
