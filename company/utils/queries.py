from typing import Dict, Optional, List

from django.db import transaction
from django.db.models import Q

from company.models import Company, CompanyName, CompanyTag, CompanyTagItem
from company.serializers import CompanyNameSerializer, CompanyTagItemSerializer
from core.miniframework_on_django.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework_on_django.query_layer.data_query.query_methods import (
    QueryReader,
    QueryCreator,
    QuerySearcher,
    QueryDestroyer, QueryUpdator
)
from access.utils.permissions import (
    CompanyClientPermissionChecker as CompanyOnly,
    AdminPermissionChecker as AdminOnly,
)
from core.miniframework_on_django.query_layer.access_query.permission import \
    PermissionSameUserChecker as SameUserOnly
from user.models import User


# noinspection PyUnresolvedReferences
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
        tag_ids = [tag.id for tag in CompanyTag.objects.filter(company__id=company['company'])]
        tags = CompanyTagItem.objects.filter(tag__in=tag_ids).filter(language=lang).values('name')
        res['tags'] = [tag['name'] for tag in tags]
        return res


class CompanyQueryUpdator(QueryUpdator):

    @transaction.atomic()
    def __call__(self,
                 modified_company_names,
                 modified_company_tags,
                 lang,
                 target_company_name):

        # 회사 검색
        global res
        q = Q(name=target_company_name) & Q(language=lang)
        try:
            company = CompanyName.objects.get(q).company
            company_id = company.id
        except CompanyName.DoesNotExist:
            raise ValueError('No Compnay searched')
        # 이름 변경
        company_names: List[CompanyName] = CompanyName.objects.filter(company=company_id)
        lang_map: Dict[str, CompanyName] = {cn.language: cn for cn in company_names}

        for k, name in modified_company_names.items():
            # 이름 수정
            if k in lang_map:
                if lang_map[k].name != name:
                    # 이름이 다르면 수정
                    lang_map[k].name = name
                    lang_map[k].save()
                    # 결과 데이터 적기
                del lang_map[k]
            else:
                # 없음 -> 새로 생성
                new_company_name = \
                    CompanyName(company=company, name=name, language=k)
                new_company_name.save()

        # lang_map에 남아있는 데이터는 전부 삭제 대상이다.
        if len(deleted := list(lang_map.keys())) > 0:
            CompanyName.objects.filter(language__in=deleted).delete()

        # 태그 데이터 수정
        tag_ids = CompanyTag.objects.filter(company=company)
        visited = {tag.id: tag for tag in tag_ids}

        for tag in modified_company_tags:
            tag_id = tag['id']
            tag_names = tag['tag_name']

            if tag_id == -1:
                # 추가
                new_tag = CompanyTag(company=company)
                new_tag.save()
                tag_id = new_tag.id
                for k, item in tag_names.items():
                    new_tag_item = CompanyTagItem(
                        tag=new_tag,
                        name=item,
                        language=k
                    )
                    new_tag_item.save()
            else:
                # 데이터 수정
                if tag_id not in visited:
                    raise ValueError()
                # 태그 내 데이터 순회
                current_tag_lang_map = \
                    {item.language: item for item in CompanyTagItem.objects.filter(tag__id=tag_id)}

                for k, new_name in tag_names.items():
                    if k not in current_tag_lang_map:
                        # 새로 언어를 추가한다.
                        new_tag_item = CompanyTagItem(tag=CompanyTag.objects.get(id=tag_id), language=k, name=new_name)
                        new_tag_item.save()
                    else:
                        if current_tag_lang_map[k].name != new_name:
                            current_tag_lang_map[k].name = new_name
                            current_tag_lang_map[k].save()
                        del current_tag_lang_map[k]

                # 남아있는 데이터는 전부 삭제 대상이다.
                if len(deleted := list(current_tag_lang_map.keys())) > 0:
                    CompanyTagItem.objects.filter(tag__id=tag_id).filter(language__in=deleted).delete()

            # 작업 후 Company Tag에 대한 TagItem이 하나도 없는 경우
            cnt = CompanyTagItem.objects.filter(tag__id=tag_id).count()
            if cnt == 0:
                CompanyTag.objects.get(id=tag_id).delete()

        # 수정된 데이터 수집

        res = {
            'company_name': CompanyName.objects.filter(company__id=company.id).get(language=lang).name,
            'tags': [
                item.name for item in
                CompanyTagItem.objects.filter(
                    tag__in=CompanyTag.objects.filter(company=company)
                ).filter(language=lang)
            ],
        }

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

                # 태그 생성
                tag = CompanyTag(company=company)
                tag.save()

                for l, t in tag_shield['tag_name'].items():
                    req = {
                        'tag': tag.id,
                        'name': t,
                        'language': l,
                    }
                    cts = CompanyTagItemSerializer(data=req)
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

        """
        Admin은 다른 사람의 회사를 삭제할 수 있지만
        CompanyClient는 자신이 만든 회사만 삭제할 수 있다.
        """
        is_available = \
            AdminOnly(user_level) | \
            (CompanyOnly(user_level) & SameUserOnly(user_email, company_user_email))

        if not bool(is_available):
            raise PermissionError('You Cannot remove this company')

        # 회사 삭제
        Company.objects.get(id=company.id)


class CompanyQuery(QueryCRUDS):
    reader = CompanyQueryReader()
    creator = CompanyQueryCreator()
    searcher = CompanyQuerySearcher()
    updator = CompanyQueryUpdator()
    destroyer = CompanyQueryDestoryer()
