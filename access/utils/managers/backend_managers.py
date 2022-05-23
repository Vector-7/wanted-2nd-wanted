from access.utils.authenticates.login import LoginTokenGenerator, check_login
from access.utils.authenticates.signup import SignUpAuthenticateCodeSender, SignUpAuthenticateCodeChecker, \
    SignUpAuthenticateTokenGenerator
from core.miniframework_on_django.manager_layer.manager import AuthenticationManager
from core.miniframework_on_django.manager_layer.plugins import AuthenticateCodePlugin


def _pass(*args, **kwargs):
    return True


class SignUpAuthenticationManager(AuthenticationManager,
                                  AuthenticateCodePlugin):
    sender = SignUpAuthenticateCodeSender()
    checker = SignUpAuthenticateCodeChecker()
    check_auth = _pass
    token_generator = SignUpAuthenticateTokenGenerator()


class LoginManager(AuthenticationManager):
    check_auth = check_login
    token_generator = LoginTokenGenerator()
