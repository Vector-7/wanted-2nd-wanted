from core.miniframework_on_django.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework_on_django.query_layer.data_query.query_methods import QueryReader, QueryCreator
from user.models import User
from user.serializers import UserSerializer


class UserQueryReader(QueryReader):

    def __call__(self, email: str):
        try:
            obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        return UserSerializer(obj).data


class UserQueryCreator(QueryCreator):

    def __call__(self, email: str, password: str, level: str, nickname: str):
        req = {
            'nickname': nickname,
            'password': password,
            'level': level,
            'email': email
        }
        user_serializer = UserSerializer(data=req)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return user_serializer.data


class UserQuery(QueryCRUDS):
    reader = UserQueryReader()
    creator = UserQueryCreator()
