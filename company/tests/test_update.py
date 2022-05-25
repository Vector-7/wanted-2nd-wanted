import json

from rest_framework import status
from rest_framework.test import APITestCase

from access.utils.managers.backend_managers import LoginManager
from user.utils.queries import UserQuery

user = None
access_token = None
user_req = {
    'nickname': 'recoma',
    'email': 'seokbong60@gmail.com',
    'level': 'company_client',
    'password': 'password0812'
}


class TestCompanyCreate(APITestCase):

    @classmethod
    def setUpTestData(cls):
        global user
        global access_token
        user = UserQuery().create(**user_req)
        access_token = LoginManager().auth(user_req['email'],
                                           user_req['email'],
                                           user_req['password'])