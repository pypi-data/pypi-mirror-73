import sys
sys.path.append('.')

from tests.common import post


headers = {
    'X-Token': ''
}

# result = post(
#     url='http://localhost:8000/api/user/register',
#     json_data={
#         'username': 'admin',
#         'password': '111111'
#     },
#     headers=headers
# )


result = post(
    url='http://localhost:58000/api/user/login',
    json_data={
        'username': 'abcd',
        'password': '1234'
    },
    headers=headers
)

print('login: ', result)
headers['X-Token'] = result['token']

result = post(
    url='http://localhost:58000/api/user/logout',
    json_data={},
    headers=headers
)

print('logout: ', result)
