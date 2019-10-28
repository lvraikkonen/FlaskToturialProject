import json

from restdemo.tests.base import TestBase


class TestUser(TestBase):

    def test_user_create(self):
        # first create a test user
        url = '/user/{}'.format(self.user_data['username'])
        res = self.client().post(
            url,
            data=self.user_data
        )
        self.assertEqual(res.status_code, 201)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data['username'], self.user_data['username'])
        self.assertEqual(res_data['email'], self.user_data['email'])

        # duplicate user
        res = self.client().post(
            url,
            data=self.user_data
        )
        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data.get('message'), f"user {self.user_data['username']} already exist.")

    def test_user_get(self):
        # create a test user first
        url = '/user/{}'.format(self.user_data['username'])
        res = self.client().post(
            url,
            data=self.user_data
        )
        res = self.client().get(url)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data.get('username'), self.user_data['username'])
        self.assertEqual(res_data.get('email'), self.user_data['email'])

    def test_user_get_not_exist(self):
        url = '/user/{}'.format(self.user_data['username'])
        res = self.client().get(url)
        res_data = res.get_data(as_text=True)
        res_data = json.loads(res_data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data, {'message': f"user {self.user_data['username']} not found"})

    def test_user_delete(self):
        url = '/user/{}'.format(self.user_data['username'])
        self.client().post(
            url,
            data=self.user_data
        )
        res = self.client().delete(url)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, {'message': f"user {self.user_data['username']} deleted."})

    def test_user_delete_not_exist(self):
        url = '/user/{}'.format(self.user_data['username'])
        res = self.client().delete(url)
        res_data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 204)

    def test_user_update(self):
        url = '/user/{}'.format(self.user_data['username'])
        self.client().post(
            url,
            data=self.user_data
        )
        res = self.client().put(
            url,
            data={
                'password': 'newpassword',
                'email': 'newemail@new.com'
            }
        )
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['email'], 'newemail@new.com')
