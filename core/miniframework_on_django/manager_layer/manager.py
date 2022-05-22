from abc import ABCMeta
from collections.abc import Callable

from core.miniframework_on_django.manager_layer.manager_layer import BackendManagerLayer
from core.miniframework_on_django.query_layer.access_query.authenticator import AuthenticateTokenGenerator


class BaseManager(metaclass=ABCMeta):
    pass


class AuthenticationManager(BaseManager,
                            BackendManagerLayer,
                            metaclass=ABCMeta):
    """
    인증 매니저

    데이터 검증 후, 검증이 완료되면 토큰을 전송한다.
    """

    token_generator: AuthenticateTokenGenerator
    check_auth: Callable

    def auth(self, info_for_token, *args, **kwargs):
        """
        인증 토큰을 전송하기 전, 제대로 된 사용자가 맞는 지 검토한다.
        """
        if self.check_auth(*args, **kwargs):
            return self.token_generator.generate(info_for_token)
        else:
            return None
