from flask import Flask
from flask_cors import CORS

from demoapp.config import config

app_client = None


def create_app(config_name):
    _app = Flask(__name__)
    CORS(_app,
         supports_credentials=True,
         origins=[
             'http://127.0.0.1:8000',
         ])
    _app.config.from_object(config[config_name])
    config[config_name].init_app(_app)

    global app_client

    from passportsdk.client import AppClient

    app_client = AppClient(_app)

    from demoapp.app.user import user_bp
    _app.register_blueprint(user_bp, url_prefix='/api/user')

    return _app
