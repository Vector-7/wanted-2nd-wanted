import json
from rest_framework import status
from rest_framework.test import APITestCase

from access.utils.managers.backend_managers import LoginManager
from user.utils.queries import UserQuery
from user.models import User
from company.models import CompanyTag, CompanyName

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
    'tags': [
        {
            'tag_name': {
                'ko': '태그1',
                'en': 'tag1',
                'ja': 'tag1',
            }
        },
        {
            'tag_name': {
                'ko': '태그2',
                'en': 'tag2',
                'ja': 'tag2',
            }
        }
    ],
}
user2_company_info = {
    'company_name': {
        'ko': '컴퍼니2', 'en': 'Company2', 'ja': 'Company'
    },
    'tags': [
        {
            'tag_name': {
                'ko': '태그1',
                'en': 'tag1',
                'ja': 'tag1',
            }
        },
        {
            'tag_name': {
                'ko': '태그2',
                'en': 'tag2',
                'ja': 'tag2',
            }
        }
    ],
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

    def test_change_success(self):
        res = self.client.post('/api/companies',
                               data=json.dumps(user1_company_info),
                               content_type='application/json',
                               **{'HTTP_x-wanted-language': 'ko', 'HTTP_access': access_token1})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        company_data = res.data

        # 데이터 수정
        req = {
            'company_name': {
                'ko': '회사', 'en': 'Company', 'ja': 'CPY'
            },
            'tags': [
                {
                    # 'id': <int>
                    'tag_name': {
                        'ko': '???',
                        'en': 'tag1',
                        'ja': 'tag1',
                    }
                },
                {
                    # 'id': <int>
                    'tag_name': {
                        'ko': '태극',
                        'en': 'tag2',
                        'ja': 'tag2',
                    }
                },
                {
                    'id': -1,  # 추가
                    'tag_name': {
                        'ko': '마지막',
                        'en': 'last',
                        'ja': 'last',
                    }
                }
            ],
        }
        company_name = CompanyName.objects.get(name=company_data['company_name'])
        company_tags = CompanyTag.objects.filter(company=company_name.company_id).values('id')
        for i in range(len(company_tags)):
            tag_id = company_tags[i]['id']
            req['tags'][i]['id'] = tag_id
        res = self.client.patch('/api/companies/컴퍼니',
                                data=json.dumps(req),
                                content_type='application/json',
                                **{'HTTP_x-wanted-language': 'ko', 'HTTP_access': access_token1})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        answer = {
            'company_name': '회사',
            "tags": [
                '???',
                "태극",
                "마지막",
            ]
        }
        self.assertCountEqual(res.data, answer)
        self.assertCountEqual(res.data['tags'], answer['tags'])
