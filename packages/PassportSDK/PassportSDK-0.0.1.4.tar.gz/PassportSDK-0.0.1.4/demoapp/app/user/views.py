from flask import request
from flask_restful import Api, Resource

from demoapp.app import app_client

api = Api()


def api_common(data={}, code=0, message='lang.success'):
    response = {
        'data': data,
        'code': code,
        'return_message': message
    }
    return response


@api.resource('/login')
class APIUserLogin(Resource):

    def post(self):
        request_data = request.get_json(silent=True)

        if app_client and app_client.get_access_token():
            return app_client.user_login(
                username=request_data['username'],
                password=request_data['password']
            )
        return api_common({})


@api.resource('/logout')
class APIUserLogout(Resource):

    def post(self):
        if 'X-Token' in request.headers:

            if app_client and app_client.get_access_token():
                # print('[APIUserLogout] X-Token : ', len(request.headers['X-Token']))
                return app_client.user_logout(request.headers['X-Token'])
        return api_common({})
