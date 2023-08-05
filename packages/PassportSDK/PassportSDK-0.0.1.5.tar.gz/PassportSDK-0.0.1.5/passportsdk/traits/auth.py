from passportsdk.client import AppClient


class AuthTrait:

    @staticmethod
    def get_access_token(app_client: AppClient):
        """
        获取access_token
        :return:
        """
        from passportsdk.common import post

        if not app_client.access_token:
            json_data = {
                'access_key_id': app_client.access_key_id,
                'access_key_secret': app_client.access_key_secret
            }
            res = post(
                url='%s/user/access/token' % app_client.passport_service_url,
                json_data=json_data,
                headers=None
            )
            if res and 'data' in res and 'access_token' in res['data']:
                # print('[[get_access_token: ', res['data']['access_token'])
                app_client.access_token = res['data']['access_token']
                return app_client.access_token
            return None
        return app_client.access_token

    @staticmethod
    def user_register(app_client, username, password):
        """
        用户注册
        :param username:
        :param password:
        :return:
        """
        json_data = {
            'username': username,
            'password': password
        }
        res = app_client.post(
            url='/user/register',
            json_data=json_data
        )
        return res

    @staticmethod
    def user_login(app_client, username, password):
        """
        用户登录
        :param username:
        :param password:
        :return:
        """
        json_data = {
            'username': username,
            'password': password
        }
        res = app_client.post(
            url='/user/login',
            json_data=json_data
        )
        print(res)
        return res

    @staticmethod
    def user_logout(app_client, user_token):
        """
        用户登出
        :param user_token:
        :return:
        """
        json_data = {
            'token': user_token,
        }
        res = app_client.post(
            url='/user/logout',
            json_data=json_data
        )
        return res

    @staticmethod
    def user_info(app_client, user_token):
        """
        用户信息
        :param user_token:
        :return:
        """
        json_data = {
            'token': user_token,
        }
        res = app_client.post(
            url='/user/info',
            json_data=json_data
        )
        return res
