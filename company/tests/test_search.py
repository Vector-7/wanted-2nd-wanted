import json
import csv
import os

from rest_framework import status
from rest_framework.test import APITestCase

from access.utils.managers.backend_managers import LoginManager
from user.utils.queries import UserQuery
from company.utils.queries import CompanyQuery
from user.models import User

user = None
access_token = None
user_req = {
    'nickname': 'recoma',
    'email': 'seokbong60@gmail.com',
    'level': 'company_client',
    'password': 'password0812'
}


class TestCompnayRead(APITestCase):

    @classmethod
    def setUpTestData(cls):
        global user
        global access_token
        UserQuery().create(**user_req)
        user = User.objects.get(email=user_req['email'])

        access_token = LoginManager().auth(user_req['email'],
                                           user_req['email'],
                                           user_req['password'])

        # csv data import
        with open('company/tests/data.csv', 'rt', encoding='utf-8') as f:
            reader = csv.reader(f)
            for idx, (ck, ce, cj, tk, te, tj) in enumerate(reader):
                if idx == 0:
                    continue
                company_names = {}
                tags = []

                if ck:
                    company_names['ko'] = ck
                if ce:
                    company_names['en'] = ce
                if cj:
                    company_names['ja'] = cj

                availables = {}
                tag_len = 0
                if tk:
                    availables['ko'] = tk.split('|')
                    if tag_len == 0:
                        tag_len = len(availables['ko'])
                if te:
                    availables['en'] = te.split('|')
                    if tag_len == 0:
                        tag_len = len(availables['en'])
                if tj:
                    availables['ja'] = tj.split('|')
                    if tag_len == 0:
                        tag_len = len(availables['en'])

                for i in range(tag_len):
                    tag = {}
                    for k, arr in availables.items():
                        tag[k] = arr[i]
                    tags.append({'tag_name': tag})

                CompanyQuery().create(
                    user=user,
                    company_names=company_names,
                    lang='ko',
                    tags=tags,
                )

    def test_search_by_only_contain_word(self):
        self.client.get('/api/search/companies', data={'query': '링크'},
                        **{'HTTP_x-wanted-language': 'ko'})
