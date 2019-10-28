import json
from restdemo.tests.base import TestBase


class TestLogin(TestBase):

    def test_login(self):
        # create test user first
        url = '/user/{}'.format(self.user_data['username'])
        self.client().post(
            url,
            data=self.user_data
        )
        # check access token
        url = '/auth/login'
        res = self.client().post(
            url,
            data=json.dumps({'username': 'test', 'password': 'test123'}),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertIn('access_token', res_data)

    def test_login_failed(self):
        # create test user first
        url = '/user/{}'.format(self.user_data['username'])
        self.client().post(
            url,
            data=self.user_data
        )
        # check access token
        url = '/auth/login'
        res = self.client().post(
            url,
            data=json.dumps({'username': 'test', 'password': 'wrong_password'}),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(res.status_code, 401)
        res_data = json.loads(res.get_data(as_text=True))
        data = {
            "description": "Invalid credentials",
            "error": "Bad Request",
            "status_code": 401
        }
        self.assertEqual(res_data, data)
