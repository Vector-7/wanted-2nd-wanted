from abc import ABCMeta

from core.miniframework_on_django.query_layer.access_query.authenticator import AuthenticateCodeSender, \
    AuthenticateCodeChecker


class AuthenticateCodePlugin(metaclass=ABCMeta):
    """
    AuthenticationManager에 추가적으로 붙는 핸들러로
    인증을 위한 임시 코드 발송/확인 절차 추가

    :variable sender <AuthenticateCodeSender>: 임시 코드를 전송할 때 사용한다.
    :variable checker <AuthenticateCodeChecker>: 임시 코드가 맞는 지 매칭할 때 사용된다.
    """
    sender: AuthenticateCodeSender
    checker: AuthenticateCodeChecker

    def request_code(self, audience, *args, **kwargs):
        """
        임시 코드 발송 요청

        :param audience: 발송 요청자, 이메일이 될 수도 있고 문자 발송을 위한 전화번호도 될 수 있다.
        :param args, kwargs: 추가적으로 붙는 옵션
        """
        auth_code = self.sender.generate_code(audience, *args, **kwargs)
        self.sender.save_code(audience, auth_code)
        self.sender.send_code(audience, auth_code)

    def match_code(self, *args, **kwargs):
        """
        코드가 일치한 지 매칭
        """
        return self.checker.match(*args, **kwargs)
