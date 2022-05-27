from user.models import User

from core.miniframework_on_django.manager_layer.manager import CRUDManager
from user.utils.queries import UserQuery
from access.utils.permissions import (
    LoginPermissionChecker as LoginOnly,
    FindingPasswordPermissionChecker as ForFindingPswdOnly,
)
from core.miniframework_on_django.system_layer.jwt.jwt import read_jwt
from core.miniframework_on_django.tools.password import match_password


class PasswordMatchFailedError(Exception):
    # 패스워드 매칭 실패 에러
    pass


class UserManager(CRUDManager):
    cruds_query = UserQuery()

    def signout(self, password, access_token):
        """
        회원 탈퇴 (유저 삭제)
        
        :param password: 확인 패스워드
        :param access_token: 탈퇴하고자 하는 유저에 대한 정보가 들어있는 토큰
        """

        # 토큰 데이터 추출
        issue, email = read_jwt(access_token, 'wanted-company-searcher')

        # 로그인 되어 있어야 한다.
        login_permission = LoginOnly(issue)
        login_permission.check()
        if not bool(login_permission):
            raise PermissionError('Permisson Failed')

        # 유저 정보 갖고오기 없으면 User.DoesNotExist 호출
        user: User = User.objects.get(email=email)

        # 패스워드 비교
        if not match_password(password, user.password):
            raise PasswordMatchFailedError()

        # 유저 삭제
        self._destroy(email=email)

    def _update_user(self, access_token, nickname=None, password=None):
        """
        사용자 업데이트
        """

        # 토큰 데이터 추출
        issue, email = read_jwt(access_token, 'wanted-company-searcher')

        # 로그인 상태여야 한다.
        is_available = LoginOnly(issue)
        is_available.check()
        if not bool(is_available):
            raise PermissionError('Permission Error')
        
        # 업데이트
        return self._update(target_email=email,
                            password=password,
                            nickname=nickname)

    def _fiding_password(self, password, access_token):
        """
        패스워드 찾기 및 재설정

        :param password: 재설정 하기 위한 패스워드
        :param access_token: 토큰
        """

        # 토큰 데이터 추출
        issue, email = read_jwt(access_token, 'wanted-company-searcher')

        # 목적이 패스워드를 잊었을 경우만 해당 기능을 사용할 수 있다.
        is_available = ForFindingPswdOnly(issue)
        is_available.check()
        if not bool(is_available):
            raise PermissionError('Permission Error')
        
        # 패스워드 업데이트
        return self._update(target_email=email,
                            password=password)

    def update_user(self, issue, access_token, nickname=None, password=None):
        """
        User 업데이트에는 두 가지의 경우가 있다.
            1. 일반적인 유저 정보 변경
            2. 패스워드 찾기
        """
        if issue == 'change':
            return self._update_user(access_token, nickname, password)
        elif issue == 'finding-password':
            return self._fiding_password(password, access_token)
        else:
            raise ValueError()
