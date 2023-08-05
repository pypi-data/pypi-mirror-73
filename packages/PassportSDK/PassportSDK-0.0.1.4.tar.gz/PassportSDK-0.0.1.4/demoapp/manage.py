import sys
sys.path.append('.')

from demoapp.app import create_app

app = create_app('dev')


if __name__ == '__main__':
    app.run(debug=True, port=58000)
