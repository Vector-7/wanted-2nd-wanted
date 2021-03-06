from typing import Optional

from access.utils.managers.backend_managers import (
    SignUpAuthenticationManager,
    LoginManager,
    FindingPasswordAuthenticateManager
)
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
    AdminPermissionChecker as AdminOnly, USER_LEVEL_MAP,
)
from user.models import User


class AuthenticationRemoteManager(BaseManager,
                                  FrontendManagerLayer):
    signup_manager = SignUpAuthenticationManager()

    def _request_email_auth_code_for_signup(self, email: Optional[str]):
        if not email:
            raise TypeError('data is not exists')
        if UserQuery().read(email=email):
            raise ValueError('user already exists')
        SignUpAuthenticationManager().request_code(email)

    def _request_email_auth_code_for_finding_password(self, email: Optional[str]):
        if not email:
            raise TypeError('data not exists')
        if not UserQuery().read(email=email):
            raise ValueError('user not exists')
        FindingPasswordAuthenticateManager().request_code(email)

    def request_auth_code(self, email: Optional[str], issue: Optional[str]):
        if not issue:
            raise PermissionError('issue failed')
        if issue == 'sign-up':
            self._request_email_auth_code_for_signup(email)
        elif issue == 'finding-password':
            self._request_email_auth_code_for_finding_password(email)
        else:
            raise PermissionError('issue failed')

    def _request_token_for_sign_up(self, email, code):

        try:
            is_matched = SignUpAuthenticationManager() \
                .match_code(code, email)
        except ValueError:
            raise TokenExpiredError('token expired')
        except Exception as e:
            # View ???????????? ??????
            raise e
        if not is_matched:
            return ValueError('token not matched')

        return SignUpAuthenticationManager().auth(email)

    def _request_token_for_finding_password(self, email, code):

        try:
            is_matched = FindingPasswordAuthenticateManager() \
                .match_code(code, email)
        except ValueError:
            raise TokenExpiredError('token expired')
        except Exception as e:
            raise e
        if not is_matched:
            return ValueError('token not matched')

        return FindingPasswordAuthenticateManager().auth(email)

    def request_token_for_certaion_issue(self, email, code, issue):
        if issue == 'sign-up':
            # ?????????
            return self._request_token_for_sign_up(email, code)
        elif issue == 'finding-password':
            # ???????????? ??????
            return self._request_token_for_finding_password(email, code)
        else:
            raise PermissionError()

    def request_sign_up(self, nickname, email, password, level, access_token):

        """
        ?????? ??????

        ????????? ??????: jwt.exceptions.DecodeError
        ????????? ??????: PermissionError
        ?????? ?????? ??????: exception
        ?????? ?????? ??????: sereializers.ValidationError
        """

        # ?????? ????????? ??????
        issue, current_email = read_jwt(access_token, 'wanted-company-searcher')
        user_level: Optional[str] = None
        try:
            user = User.objects.get(email=current_email)
            user_level = USER_LEVEL_MAP[user.level]
        except Exception:
            pass

        """
        ?????? ??????
        
        1.?????? ?????? ?????? ????????? ??????
            1.1. ?????? ?????? ?????? ??????
                and
            1.2. ????????? ???????????? ?????? ??????
        2. ??? Admin??? ?????? ????????? ????????? ???????????????
            ?????? ?????? ???????????? ?????? ?????? ??????
        """
        is_allowed = (SignUpOnly(issue) & SameEmailOnly(current_email, email)) | \
                     (AdminOnly(user_level) & LoginOnly(issue))
        if not bool(is_allowed):
            raise PermissionError('Permission Failed')

        # ?????? ?????? ??? ?????????
        return UserQuery().create(nickname=nickname,
                                  email=email,
                                  password=password,
                                  level=level)

    def request_login(self, email, password):
        token = LoginManager().auth(email, email, password)
        return token
