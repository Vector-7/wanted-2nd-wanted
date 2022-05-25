from user.models import User

from core.miniframework_on_django.manager_layer.manager import CRUDManager
from user.utils.queries import UserQuery
from access.utils.permissions import (
    LoginPermissionChecker as LoginOnly,
)
from core.miniframework_on_django.system_layer.jwt.jwt import read_jwt
from core.miniframework_on_django.tools.password import match_password
from access.utils.permissions import USER_LEVEL_MAP


class PasswordMatchFailedError(ValueError):
    pass


class UserManager(CRUDManager):
    cruds_query = UserQuery()

    def signout(self, password, access_token):

        # 토큰 데이터 추출
        issue, email = read_jwt(access_token, 'wanted-company-searcher')

        # 로그인 되어 있어야 한다.
        login_permission = LoginOnly(issue)
        login_permission.check()
        if not bool(login_permission):
            raise PermissionError('Permisson Failed')

        # 유저 정보 갖고오기 없으면 User.DoesNotExist 호출
        user: User = User.objects.get(email=email)
        user_lv = USER_LEVEL_MAP[user.level]

        # 패스워드 비교
        if not match_password(password, user.password):
            raise PasswordMatchFailedError()

        # 유저 삭제
        self._destroy(email=email)
