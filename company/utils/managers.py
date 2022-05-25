from access.utils.permissions import (
    CompanyClientPermissionChecker as CompanyOnly,
    LoginPermissionChecker as LoginOnly,
    AdminPermissionChecker as AdminOnly,
    USER_LEVEL_MAP
)
from company.utils.queries import CompanyQuery
from core.miniframework_on_django.manager_layer.manager import CRUDManager
from core.miniframework_on_django.system_layer.jwt.jwt import read_jwt
from user.models import User


# noinspection PyMethodMayBeStatic
class CompanyManager(CRUDManager):
    cruds_query = CompanyQuery()

    def create_company(self, company_name, tags, lang, access_token):
        """
        회사 생성

        디코딩 실패: jwt.exceptions.DecodeError
        토큰 만료: TokenExpiredError
        권한이 안됨: PermissionError
        알수 없는 에러: exception
        유저 생성 실패: serializers.ValidationError
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
        """
        """
        해당 함수에 대한 쿼리 로직은 해당 경로에 있습니다.
        company/utils/queries.py
        """
        return self._read(company_name=company_name, lang=lang)

    def search_company_by_contain_word(self, word, lang):
        """
        연관검색어를 이용한 검색

        Not Implemented
        """
        """
        해당 함수에 대한 쿼리 로직은 해당 경로에 있습니다.
        company/utils/queries.py
        """
        return self._search(word=word,
                            lang=lang)

    def remove_company(self, company_name, lang, access_token):
        """
        회사 삭제

        디코딩 실패: jwt.exceptions.DecodeError
        토큰 만료: TokenExpiredError
        권한이 안됨: PermissionError
            + 다른 사람의 회사를 삭제하는 경우도 포함
        없는 회사 삭제하려고 함: ValueError
        알수 없는 에러: exception
        """

        # 토큰 데이터 추출
        issue, email = read_jwt(access_token, 'wanted-company-searcher')
        user: User = User.objects.get(email=email)
        user_lv = USER_LEVEL_MAP[user.level]

        """
        회사를 삭제하려면 CompanyClient/Admin 정도의 레벨에
        로그인 상태여야 한다.
        
        또한 자신이 만든 회사만 삭제할 수 있어야 하는데 이 부분은 Query단계에서 처리한다.
        """
        is_available = (CompanyOnly(user_lv) | AdminOnly(user_lv)) & LoginOnly(issue)
        if not bool(is_available):
            raise PermissionError('Permission Failed')

        self._destroy(user_email=email,
                      user_level=user_lv,
                      removed_company=company_name,
                      lang=lang)

    def update_company(self, company_name, tags, lang, access_token, target_company):

        # 토큰 데이터 추출
        issue, email = read_jwt(access_token, 'wanted-company-searcher')
        user: User = User.objects.get(email=email)
        user_lv = USER_LEVEL_MAP[user.level]

        is_available = (CompanyOnly(user_lv) | AdminOnly(user_lv)) & LoginOnly(issue)
        if not bool(is_available):
            raise PermissionError('Permission Failed')

        return self._update(
            modified_company_names=company_name,
            modified_company_tags=tags,
            lang=lang,
            target_company_name=target_company,
        )
