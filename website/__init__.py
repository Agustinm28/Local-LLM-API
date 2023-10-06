from flask import Flask
from flask_restx import Api
from services.answer_services import answer
from services.auth_services import Auth
from services.model_services import LLMmodels

def create_app(config):

    # Initialize flask app
    app = Flask(__name__)
    app.config.from_object(config)
    api = Api(app, doc='/docs')

    # Register Namespaces
    api.add_namespace(answer)
    api.add_namespace(Auth)
    api.add_namespace(LLMmodels)

    return app