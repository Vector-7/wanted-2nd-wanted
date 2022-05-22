from abc import ABCMeta
from typing import Any

from core.miniframework_on_django.query_layer.access_query.authenticator import AuthenticateCodeSender, \
    AuthenticateCodeChecker


class AuthenticateCodePlugin(metaclass=ABCMeta):
    """
    AuthenticationManager에 추가적으로 붙는 핸들러로
    인증을 위한 임시 코드 발송/확인 절차 추가
    """
    sender: AuthenticateCodeSender
    checker: AuthenticateCodeChecker

    def request_code(self, email, *args, **kwargs):
        auth_code = self.sender.generate_code(email, *args, **kwargs)
        self.sender.save_code(email, auth_code)
        self.sender.send_code(email, auth_code)

    def match_code(self, *args, **kwargs):
        return self.checker.match(*args, **kwargs)
