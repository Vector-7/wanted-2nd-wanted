from typing import Dict, Optional, List

from django.db import transaction
from django.db.models import Q

from company.models import Company, CompanyName, CompanyTag
from company.serializers import CompanyNameSerializer, CompanyTagSerializer
from core.miniframework_on_django.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework_on_django.query_layer.data_query.query_methods import (
    QueryReader,
    QueryCreator,
    QuerySearcher,
    QueryDestroyer
)
from user.models import User


class CompanyQueryReader(QueryReader):
    # 회사 정보 읽기

    def __call__(self,
                 company_name,
                 lang=None):

        companies = CompanyName.objects.filter(name=company_name).values('company')

        if len(companies) == 0:
            return None
        if not lang:
            # 언어 고려 X
            # 맨 첫번 째 부분만 출력한다.
            company = companies[0].company
        else:
            # 언어를 고려한 출력

            # 해당 언어로 검색도된 회사들의 company id, langauge로 다시 검색
            company_ids = [company['company'] for company in companies]
            companies = CompanyName.objects \
                .filter(company__id__in=company_ids) \
                .filter(language=lang).values('company', 'name')

            # 정보 없음
            if len(companies) == 0:
                return None
            # 가장 맨 위에 있는 데이터를 선택
            company = companies[0]

        # 검색 대상 회사를 이용해 태그 검색
        res = {'company_name': company['name'], 'tags': []}
        tags = CompanyTag.objects \
            .filter(company__id=company['company']) \
            .filter(language=lang).values('name')
        res['tags'] = [tag['name'] for tag in tags]
        return res


class CompanyQueryCreator(QueryCreator):
    # 회사 생성

    @transaction.atomic()  # 트랜잭션 적용
    def __call__(self,
                 user: User,
                 company_names: Dict[str, str],
                 lang: str,
                 tags: Optional[
                     List[
                         Dict[str, Dict[str, str]]
                     ]
                 ]):
        """
        :param user: 회사 데이터를 생성 할 User
        :param company_names: 회사 이름들
        :param lang: 언어
        :param tags: 테그 데이터들

        :return: 생성 결과(언어에 따른 출력)
        """

        """
        Input Formats
        compnay_names = {
            "<lang>": "<name>",
            "<lang>": "<name>",
            ...
        }
        tags = [
            {
                "tag_name": {
                    "<lang>": "<name>",
                    "<lang>": "<name>",
                    ...
                }
            }
        ]
        ...
        
        Output Format
        lang에 따라야 함 
        {
            "company_name": "<name>",
            "tags": ["<tag1>", "<tag2>", ...]
        }
        """

        res = {
            'company_name': None,
            'tags': [],
        }

        """ Company 생성 """
        company: Company = Company(user=user)
        company.save()

        """
        Company Name 생성
        l -> 언어
        n -> 이름
        """
        for l, n in company_names.items():
            req = {
                'company': company.id,
                'name': n,
                'language': l,
            }
            cns = CompanyNameSerializer(data=req)
            cns.is_valid(raise_exception=True)
            cns.save()
            if req['language'] == lang:
                res['company_name'] = req['name']

        """
        company tag 생성
        l -> 언어
        t -> 태그 이름
        """
        if tags:
            # 태그가 존재하는 경우만 추가한다.
            for tag_shield in tags:
                if 'tag_name' not in tag_shield:
                    continue
                for l, t in tag_shield['tag_name'].items():
                    req = {
                        'company': company.id,
                        'name': t,
                        'language': l,
                    }
                    cts = CompanyTagSerializer(data=req)
                    cts.is_valid(raise_exception=True)
                    cts.save()
                    if req['language'] == lang:
                        res['tags'].append(req['name'])
        return res


class CompanyQuerySearcher(QuerySearcher):
    # 회사 검색
    def __call__(self, word, lang):
        company_names = CompanyName.objects.filter(name__contains=word) \
            .filter(language=lang).values('name')
        return [{'company_name': company_name['name']} for company_name in company_names]


class CompanyQueryDestoryer(QueryDestroyer):
    def __call__(self,
                 user_email,
                 user_level,
                 removed_company,
                 lang):

        """
        삭제할 회사 검색
        이름 and 언어로 검색한다.
        이러면 단 한개의 회사만 검색된다.
        """
        q = Q(name=removed_company) & Q(language=lang)
        try:
            company = CompanyName.objects.get(q).company
            company_user_email = company.user.email
        except CompanyName.DoesNotExist:
            raise ValueError('No Compnay searched')

        # 자신이 만든 회사여야 한다
        if user_email != company_user_email:
            raise PermissionError('You Cannot remove this company')

        # 회사 삭제
        Company.objects.get(id=company.id)


class CompanyQuery(QueryCRUDS):
    reader = CompanyQueryReader()
    creator = CompanyQueryCreator()
    searcher = CompanyQuerySearcher()
    destroyer = CompanyQueryDestoryer()
