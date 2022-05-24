from typing import Optional, Iterable

from access.utils.permissions import (
    CompanyClientPermissionChecker as CompanyOnly,
    LoginPermissionChecker as LoginOnly,
    USER_LEVEL_MAP
)
from company.utils.queries import CompanyQuery
from core.miniframework_on_django.manager_layer.manager import CRUDManager
from core.miniframework_on_django.system_layer.jwt.jwt import read_jwt
from user.models import User


class CompanyManager(CRUDManager):
    cruds_query = CompanyQuery()

    def create_company(self, company_name, tags, lang, access_token):
        """
        회사 생성

        디코딩 실패: jwt.exceptions.DecodeError
        토큰 만료: TokenExpiredError
        권한이 안됨: PermissionError
        알수 없는 에러: exception
        유저 생성 실패: sereializers.V
        """

        # 토큰 데이터 추출
        issue, email = read_jwt(access_token, 'wanted-company-searcher')
        user: User = User.objects.get(email=email)
        user_lv = USER_LEVEL_MAP[user.level]

        # 회사를 만드려면 해당 유저는 CompanyClient에 로그인이 되어 있어야 한다
        if not bool(CompanyOnly(user_lv) & LoginOnly(issue)):
            raise PermissionError('Permission Failed')

        """
        생성
        해당 함수에 대한 쿼리 로직은 해당 경로에 있습니다.
        company/utils/queries.py
        """
        return self._create(
            company_names=company_name,
            tags=tags,
            user=user,
            lang=lang)

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
