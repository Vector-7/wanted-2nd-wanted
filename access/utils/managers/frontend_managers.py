from typing import Optional

from access.utils.managers.backend_managers import SignUpAuthenticationManager, LoginManager
from core.miniframework_on_django.exc import TokenExpiredError
from core.miniframework_on_django.manager_layer.manager import BaseManager
from core.miniframework_on_django.manager_layer.manager_layer import FrontendManagerLayer
from user.utils.queries import UserQuery
from core.miniframework_on_django.query_layer.access_query.permission \
    import PermissionSameUserChecker as SameEmailOnly
from core.miniframework_on_django.system_layer.jwt.jwt import read_jwt
from access.utils.permissions import (
    SignUpPermissionChecker as SignUpOnly,
    LoginPermissionChecker as LoginOnly,
    AdminPermissionChecker as AdminOnly,
)


class AuthenticationRemoteManager(BaseManager,
                                  FrontendManagerLayer):
    signup_manager = SignUpAuthenticationManager()

    def request_email_auth_code(self, email: Optional[str]):
        if not email:
            raise TypeError('data is not exists')

        if UserQuery().read(email=email):
            raise ValueError('user already exists')

        SignUpAuthenticationManager().request_code(email)

    def request_token_for_sign_up(self, req_data):
        code, email = req_data['code'], req_data['email']

        try:
            is_matched = SignUpAuthenticationManager() \
                .match_code(code, email)
        except ValueError:
            raise TokenExpiredError('token expired')
        except Exception as e:
            # View 단위에서 처리
            raise e
        if not is_matched:
            return ValueError('token not matched')

        return SignUpAuthenticationManager().auth(email)

    def request_sign_up(self, nickname, email, password, level, access_token):

        """
        회원 가입

        디코딩 실패: jwt.exceptions.DecodeError
        권한이 안됨: PermissionError
        알수 없는 에러: exception
        유저 생성 실패: sereializers.ValidationError
        """

        # 토큰 데이터 추출
        issue, current_email = read_jwt(access_token, 'wanted-company-searcher')
        user_level: Optional[str] = None
        try:
            user = User.objects.get(email=current_email)
            user_level = USER_LEVEL_MAP[user.level]
        except Exception:
            pass

        """
        권한 체크
        
        1.일반 유저 회원 가입일 경우
            1.1. 회원 가입 전용 토큰
                and
            1.2. 자신의 이메일로 회원 가입
        2. 단 Admin일 경우 로그인 상태의 토큰이라면
            다른 사람 계정으로 회원 가입 가능
        """
        is_allowed = (SignUpOnly(issue) & SameEmailOnly(current_email, email)) | \
                     (AdminOnly(user_level) & LoginOnly(issue))
        if not bool(is_allowed):
            raise PermissionError('Permission Failed')

        # 유저 생성 및 보내기
        return UserQuery().create(nickname=nickname,
                                  email=email,
                                  password=password,
                                  level=level)

    def request_login(self, email, password):
        token = LoginManager().auth(email, email, password)
        return token
