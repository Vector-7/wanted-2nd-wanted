import json
from rest_framework import status
from rest_framework.test import APITestCase

from access.utils.managers.backend_managers import LoginManager
from user.utils.queries import UserQuery
from user.models import User

user1 = None
access_token1 = None
user_req1 = {
    'nickname': 'recoma',
    'email': 'seokbong60@gmail.com',
    'level': 'company_client',
    'password': 'password0812'
}

user2 = None
access_token2 = None
user_req2 = {
    'nickname': 'jeonghyun',
    'email': 'napalosense@gmail.com',
    'level': 'company_client',
    'password': 'password0812'
}

user1_company_info = {
    'company_name': {
        'ko': '컴퍼니', 'en': 'Company', 'ja': 'CPY'
    },
    'tags': [],
}
user2_company_info = {
    'company_name': {
        'ko': '컴퍼니2', 'en': 'Company2', 'ja': 'Company'
    },
    'tags': [],
}


class TestCompanyDelete(APITestCase):

    @classmethod
    def setUpTestData(cls):
        global user1, access_token1
        global user2, access_token2

        UserQuery().create(**user_req1)
        user1 = User.objects.get(email=user_req1['email'])

        access_token1 = LoginManager().auth(user_req1['email'],
                                            user_req1['email'],
                                            user_req1['password'])

        UserQuery().create(**user_req2)
        user2 = User.objects.get(email=user_req2['email'])

        access_token2 = LoginManager().auth(user_req2['email'],
                                            user_req2['email'],
                                            user_req2['password'])

    def test_success_remove(self):
        # 생성
        res = self.client.post('/api/companies',
                               data=json.dumps(user1_company_info),
                               content_type='application/json',
                               **{'HTTP_x-wanted-language': 'ko', 'HTTP_access': access_token1})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # 삭제
        res = self.client.delete('/api/companies/컴퍼니',
                                 **{'HTTP_x-wanted-language': 'ko', 'HTTP_access': access_token1})
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_remove_no_existed_company(self):
        res = self.client.delete('/api/companies/컴퍼니',
                                 **{'HTTP_x-wanted-language': 'ko', 'HTTP_access': access_token1})
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_remove_other_company(self):
        # user 1 데이터 생성
        res = self.client.post('/api/companies',
                               data=json.dumps(user1_company_info),
                               content_type='application/json',
                               **{'HTTP_x-wanted-language': 'ko', 'HTTP_access': access_token1})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # user 2 데이터 생성
        res = self.client.post('/api/companies',
                               data=json.dumps(user2_company_info),
                               content_type='application/json',
                               **{'HTTP_x-wanted-language': 'ko', 'HTTP_access': access_token2})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # user1이 user2의 회사를 삭제할 수 없다
        res = self.client.delete('/api/companies/Company',
                                 **{'HTTP_x-wanted-language': 'ja', 'HTTP_access': access_token1})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
