
class Config:

    HOST = 'http://127.0.0.1:8000'

    DEFAULT_APP_URL = '%s/api' % HOST
    DEFAULT_APP_ACCESS_KEY_ID = 'abcdefg'
    DEFAULT_APP_ACCESS_KEY_SECRET = '1111111'

    @staticmethod
    def init_app(app):
        pass


config = {
    'dev': Config,
}
