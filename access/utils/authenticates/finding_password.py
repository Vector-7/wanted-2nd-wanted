from django.core.mail import EmailMessage
from django.core.cache import cache
import random

from core.miniframework_on_django.query_layer.access_query.authenticator import AuthenticateCodeSender, \
    AuthenticateCodeChecker, AuthenticateTokenGenerator


class FindingPasswordAuthenticateCodeSender(AuthenticateCodeSender):
    ttl = 3

    def generate_code(self, *args, **kwargs) -> str:
        return str(random.randint(100000, 999999))

    def save_code(self, audience, auth_code):
        key = f'email_certificate:finding_password:{audience}'
        value = {
            'code': auth_code
        }
        cache.set(key, value, self.get_ttl_second())

    def send_code(self, audience, auth_code):
        """
        이메일로 코드 코드 전송
        """
        email = EmailMessage(
            'Company Searcher 인증 코드 입니다.',
            f'Code: {auth_code}',
            to=[audience]
        )
        email.send()


class FindingPasswordAuthenticateCodeChecker(AuthenticateCodeChecker):
    """
    패스워드 찾기 관련 인증 체크
    """

    def match(self, code: str, email: str) -> bool:
        key = f'email_certificate:finding_password:{email}'

        # 데이터 가져오기
        auth_data = cache.get(key)

        if not auth_data:
            # 데이터 없음
            raise ValueError('Code Expired')

        # 매칭
        return code == auth_data['code']


class FindingPasswordAuthenticateTokenGenerator(AuthenticateTokenGenerator):
    """
    패스워드 찾기 시 토큰 생성
    """
    app_name = 'wanted-company-searcher'
    issue = 'finding-password'
    expire_len = 5
