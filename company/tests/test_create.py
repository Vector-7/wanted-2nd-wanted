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

    def test_create_success(self):
        """
        새로운 회사 추가
        """
        res = self.client.post(
            '/api/companies',
            data=json.dumps({
                "company_name": {"ko": "라인 프레쉬", "tw": "LINE FRESH", "en": "LINE FRESH", },
                "tags": [
                    {"tag_name": {"ko": "태그_1", "tw": "tag_1", "en": "tag_1"}},
                    {"tag_name": {"ko": "태그_8", "tw": "tag_8", "en": "tag_8"}},
                    {"tag_name": {"ko": "태그_15", "tw": "tag_15", "en": "tag_15"}}
                ]
            }),
            content_type='application/json',
            **{'HTTP_x-wanted-language': 'tw', 'HTTP_access': access_token}
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertCountEqual(res.data, {
            "company_name": "LINE FRESH",
            "tags": [
                "tag_1",
                "tag_8",
                "tag_15",
            ],
        })

    def test_create_with_no_tag(self):
        """
        태그 없어도 됨
        """
        res = self.client.post(
            '/api/companies',
            data=json.dumps({
                "company_name": {"ko": "라인 프레쉬", "tw": "LINE FRESH", "en": "LINE FRESH", },
                "tags": []
            }),
            content_type='application/json',
            **{'HTTP_x-wanted-language': 'ko', 'HTTP_access': access_token}
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertCountEqual(res.data, {
            "company_name": "라인 프레쉬",
            "tags": [
            ],
        })

    def test_create_no_same_lang(self):
        res = self.client.post(
            '/api/companies',
            data=json.dumps({
                "company_name": {"ko": "라인 프레쉬", "tw": "LINE FRESH", "en": "LINE FRESH", },
                "tags": []
            }),
            content_type='application/json',
            **{'HTTP_x-wanted-language': 'ko', 'HTTP_access': access_token}
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.post(
            '/api/companies',
            data=json.dumps({
                "company_name": {"ko": "라인 프레쉬", "tw": "LLLLIIINNNEEEFFFRREESSSSHHH", "en": "LINE FRESH", },
                "tags": [
                    {"tag_name": {"ko": "태그_1", "tw": "tag_1", "en": "tag_1"}},
                    {"tag_name": {"ko": "태그_8", "tw": "tag_8", "en": "tag_8"}},
                    {"tag_name": {"ko": "태그_15", "tw": "tag_15", "en": "tag_15"}}
                ]
            }),
            content_type='application/json',
            **{'HTTP_x-wanted-language': 'ko', 'HTTP_access': access_token}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_client_restict(self):
        # 클라이언트 접근 불가
        client_req = {
            'nickname': 'recoma2',
            'email': 'seokbong602@gmail.com',
            'level': 'client',
            'password': 'password0812'
        }
        UserQuery().create(**client_req)
        client_token = LoginManager().auth(client_req['email'],
                                           client_req['email'],
                                           client_req['password'])

        res = self.client.post(
            '/api/companies',
            data=json.dumps({
                "company_name": {"ko": "라인 프레쉬", "tw": "LINE FRESH", "en": "LINE FRESH", },
                "tags": [
                    {"tag_name": {"ko": "태그_1", "tw": "tag_1", "en": "tag_1"}},
                    {"tag_name": {"ko": "태그_8", "tw": "tag_8", "en": "tag_8"}},
                    {"tag_name": {"ko": "태그_15", "tw": "tag_15", "en": "tag_15"}}
                ]
            }),
            content_type='application/json',
            **{'HTTP_x-wanted-language': 'ko', 'HTTP_access': client_token}
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
