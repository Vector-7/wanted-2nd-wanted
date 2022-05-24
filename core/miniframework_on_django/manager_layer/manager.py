from abc import ABCMeta
from collections.abc import Callable
from typing import Dict, Any

from core.miniframework_on_django.manager_layer.manager_layer import BackendManagerLayer, FrontendManagerLayer
from core.miniframework_on_django.query_layer.access_query.authenticator import AuthenticateTokenGenerator
from core.miniframework_on_django.query_layer.data_query.query_cruds import QueryCRUDS


class BaseManager(metaclass=ABCMeta):
    """
    모든 Manager의 최상위 객체
    현재는 상징적 추상 클래스 이지만
    상황에 따라 모든 Manager에게 필요한 기능을 구현해야 할 경우
    여기에 구현할 것
    """
    pass


class AuthenticationManager(BaseManager,
                            BackendManagerLayer,
                            metaclass=ABCMeta):
    """
    인증 Manager

    데이터 검증 후, 검증이 완료되면 토큰을 전송한다.
    BackendManager 타입으로 View단위에서가 아닌 FrontendManager단에서 사용할 것

    :variable token_generator <AuthenticateTokenGenerator>: 토큰 생성기
    :variable check_auth <Function[Any] -> bool>: 토큰을 생성하기 전 유효한 사용자 인지 검수를 한다.
    """

    token_generator: AuthenticateTokenGenerator
    check_auth: Callable

    def auth(self, info_for_token: Any, *args, **kwargs) -> str:
        """
        토큰 발행

        :param info_for_token: 토큰을 만들기 위한 정보들
        :param args, kwargs: info_for_token을 제외한 나머지 parameter로 사용자 검토를 할 때 사용된다.

        :return: 문자열 형태의 토큰을 발행

        :exception PermissionError: 유효하지 않은 사용자일 경우
        """
        if self.check_auth(*args, **kwargs):
            return self.token_generator.generate(info_for_token)
        else:
            raise PermissionError('Auth Failed')


class CRUDManager(BaseManager,
                  FrontendManagerLayer,
                  metaclass=ABCMeta):
    """
    데이터베이스를 접속하기 위한 Manager

    상황에 따라 내장 함수들(_create, _update, _read ...)를 이용하여 별개의 쿼리를 함수 단위로 작성 가능
    내장 함수들의 작동은 QueryCRUDS의 함수들을 사용한다.

    :variable cruds_query: 기초 쿼리 함수 제공하는 클래스
    """
    cruds_query: QueryCRUDS

    def _create(self, *args, **kwargs):
        return self.cruds_query.create(*args, **kwargs)

    def _update(self, *args, **kwargs):
        return self.cruds_query.update(*args, **kwargs)

    def _read(self, *args, **kwargs):
        return self.cruds_query.read(*args, **kwargs)

    def _destroy(self, *args, **kwargs):
        return self.cruds_query.destroy(*args, **kwargs)

    def _search(self, *args, **kwargs):
        return self.cruds_query.search(*args, **kwargs)
