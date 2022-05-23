from core.miniframework_on_django.query_layer.access_query.authenticator import AuthenticateTokenGenerator
from core.miniframework_on_django.tools.password import match_password
from user.utils.data_queries.user import UserQuery


def check_login(_, email, password):

    # User Query를 사용하여 데이터 구하기
    user = UserQuery().read(email=email)
    if not user:
        return False
    user_password = user['password']
    return match_password(password, user_password)


class LoginTokenGenerator(AuthenticateTokenGenerator):
    app_name = 'wanted-company-searcher'
    issue = 'login'
    # 30일
    expire_len = 60 * 24 * 30
