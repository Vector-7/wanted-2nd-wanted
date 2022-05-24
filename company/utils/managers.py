from typing import Optional, Iterable

from access.utils.permissions import CompanyClientPermissionChecker
from company.utils.queries import CompanyQuery
from core.miniframework_on_django.manager_layer.manager import CRUDManager
from core.miniframework_on_django.query_layer.access_query.permission import PermissionList
from core.miniframework_on_django.system_layer.jwt.jwt import read_jwt


class CompanyManager(CRUDManager):
    cruds_query = CompanyQuery()

    def create_company(self, company_name, tags, lang, access_token):
        """
        회사 생성

        디코딩 실패: jwt.exceptions.DecodeError
        권한이 안됨: PermissionError
        알수 없는 에러: exception
        유저 생성 실패: sereializers.ValidationError
        """

        # 권한 체크
        PermissionList(
            req_permissions=[
                CompanyClientPermissionChecker(),
            ],
            decode_token_func=read_jwt,
            app_name='wanted-company-searcher'
        )
        return self._create(company_name, tags, lang)

    def get_company_info(self, company_name, lang):
        """
        회사 관련 내용 검색

        Not Implemented
        """
        return self._read(company_name=company_name,
                          lang=lang)

    def _search_company_by_contain_word(self, tags, lang):
        """
        연관검색어를 이용한 검색

        Not Implemented
        """
        return self._search(tags=tags,
                            lang=lang)

    def _search_company_by_tags(self, tags):
        raise NotImplemented()

    def search_company(self,
                       lang: str,
                       word: Optional[str],
                       tags: Optional[Iterable[str]]):
        raise NotImplemented()
