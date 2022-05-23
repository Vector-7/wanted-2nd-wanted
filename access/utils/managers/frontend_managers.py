from typing import Optional

from access.utils.managers.backend_managers import SignUpAuthenticationManager, LoginManager
from access.utils.permissions import SignUpPermissionChecker
from core.miniframework_on_django.exc import TokenExpiredError
from core.miniframework_on_django.manager_layer.manager import BaseManager
from core.miniframework_on_django.manager_layer.manager_layer import FrontendManagerLayer
from core.miniframework_on_django.query_layer.access_query.permission import PermissionList, PermissionSameUserChecker
from core.miniframework_on_django.system_layer.jwt.jwt import read_jwt
from user.utils.data_queries.user import UserQuery


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
        Permission Check

        디코딩 실패: jwt.exceptions.DecodeError
        권한이 안됨: PermissionError
        알수 없는 에러: exception
        유저 생성 실패: sereializers.ValidationError
        """

        # 권한 체크
        PermissionList(
            req_permissions=[
                SignUpPermissionChecker(),
                PermissionSameUserChecker(target_user=email),
            ],
            decode_token_func=read_jwt,
            app_name='wanted-company-searcher',
        )(access_token)

        # 유저 생성 및 보내기
        return UserQuery().create(nickname=nickname,
                                  email=email,
                                  password=password,
                                  level=level)

    def request_login(self, email, password):

        token = LoginManager().auth(email, email, password)

        # 토큰 발행
        return token
