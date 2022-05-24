from typing import Optional

from core.miniframework_on_django.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework_on_django.query_layer.data_query.query_methods import QueryReader, QueryCreator
from user.models import User
from user.serializers import UserSerializer


class UserQueryReader(QueryReader):

    def __call__(self,
                 email: Optional[str] = None,
                 nickname: Optional[str] = None):
        obj = None
        try:
            if email:
                obj = User.objects.get(email=email)
            elif nickname:
                obj = User.objects.get(nickname=nickname)
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
        data = user_serializer.data

        # password 부분 삭제
        del data['password']

        return data


class UserQuery(QueryCRUDS):
    reader = UserQueryReader()
    creator = UserQueryCreator()
