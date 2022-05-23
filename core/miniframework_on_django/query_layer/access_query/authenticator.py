import time
from abc import ABCMeta, abstractmethod

from core.miniframework_on_django.system_layer.jwt.jwt import write_jwt


class AuthenticateCodeChecker(metaclass=ABCMeta):
    """
    인증 코드가 정확한 지 검사하는 클래스
    """

    @abstractmethod
    def match(self, *args, **kwargs) -> bool:
        """
        검토를 위한 input_code가 들어간다.

        :return: (bool) 맞으면 True, 틀리면 False
        """
        pass


class AuthenticateCodeSender(metaclass=ABCMeta):
    """
    인증 코드를 요청하는 클래스
    이때 리턴값이 아닌 다른 수단을 이용(SMS, Email 등)을 이용해
    인증한다.

    :variable ttl: 인증코드 제한 시간 (분단위)

    :function generate_code: 인증코드 생성 함수
    :function send_code: 인증코드 발송
    """
    ttl: int

    def get_ttl_second(self):
        return self.ttl * 60

    @abstractmethod
    def generate_code(self, *args, **kwargs) -> str:
        """
        인증코드 생성
        """
        pass

    @abstractmethod
    def save_code(self, email, auth_code):
        """
        특정 DB에 저장
        """
        pass

    @abstractmethod
    def send_code(self, email, auth_code):
        """
        인증 코드를 발송한다.
        """
        pass


class AuthenticateTokenGenerator(metaclass=ABCMeta):
    """
    JWT 토큰을 생성하는 클래스
    """

    app_name: str
    issue: str
    expire_len: int     # minue

    def generate(self, audience) -> str:
        return write_jwt(
            app_name=self.app_name,
            issue=self.issue,
            audience=audience,
            expire_len=self.expire_len
        )
