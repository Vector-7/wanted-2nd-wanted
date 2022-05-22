from django.core.mail import EmailMessage
from django.core.cache import cache
import random

from core.miniframework_on_django.query_layer.access_query.authenticator import AuthenticateCodeSender, \
    AuthenticateCodeChecker, AuthenticateTokenGenerator


class SignUpAuthenticateCodeSender(AuthenticateCodeSender):
    """
    회원 가입용 인증코드 발송
    """
    ttl = 3

    def generate_code(self, *args, **kwargs) -> str:
        return str(random.randint(100000, 999999))

    def save_code(self, email, auth_code):
        key = f'email_certificate:{email}'
        value = {
            'code': auth_code
        }
        cache.set(key, value, self.get_ttl_second())

    def send_code(self, email, auth_code):
        """
        이메일로 코드 코드 전송
        """
        email = EmailMessage(
            'Company Searcher 인증 코드 입니다.',
            f'Code: {auth_code}',
            to=[email]
        )
        email.send()


class SignUpAuthenticateCodeChecker(AuthenticateCodeChecker):
    """
    회원 가입 인증 체크
    """
    def match(self, code: str, email: str) -> bool:
        key = f'email_certificate:{email}'

        # 데이터 가져오기
        auth_data = cache.get(key)

        if not auth_data:
            # 데이터 없음
            raise ValueError('Code Expired')

        # 매칭
        return code == auth_data['code']


class SignUpAuthenticateTokenGenerator(AuthenticateTokenGenerator):
    """
    회원 가입 시, 유저 생성을 위해 필요한 토큰 생성기
    """
    app_name = 'wanted-company-searcher'
    issue = 'sign-up'
    expire_len = 5
