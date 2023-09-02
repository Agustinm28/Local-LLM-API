from flask import Flask
from os import path
from .views import views

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234'

    app.register_blueprint(views, url_prefix='/')

    return app