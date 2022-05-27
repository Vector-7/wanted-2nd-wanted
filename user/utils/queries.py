from typing import Optional

from core.miniframework_on_django.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework_on_django.query_layer.data_query.query_methods import (
    QueryReader,
    QueryCreator,
    QueryDestroyer,
    QueryUpdator
)
from user.models import User
from user.serializers import UserSerializer


class UserQueryReader(QueryReader):
    """
    유저 정보 읽기
    """

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
    """
    유저 생성
    """

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


class UserQueryDestroyer(QueryDestroyer):
    """
    유저 삭제
    """
    def __call__(self,
                 user_name: Optional[str] = None,
                 email: Optional[str] = None):
        if user_name:
            User.objects.get(name=user_name).delete()
        elif email:
            User.objects.get(email=email).delete()
        else:
            raise ValueError('No Data Selected')


class UserQueryUpdator(QueryUpdator):
    """
    유저 정보 변경
    
    패스워드/닉네임만 변경 가능
    """
    def __call__(self,
                 target_email: Optional[str] = None,
                 target_nickname: Optional[str] = None,

                 password: Optional[str] = None,
                 nickname: Optional[str] = None):
        user: User = None
        if target_email:
            user = User.objects.get(email=target_email)
        elif target_nickname:
            user = User.objects.get(nickname=target_nickname)
        else:
            raise ValueError('target user data is nothing')
        req = dict()
        if password:
            req['password'] = password
        if nickname:
            req['nickname'] = nickname
        user_serializer = UserSerializer(user, data=req, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return {'result': 'ok'}


class UserQuery(QueryCRUDS):
    reader = UserQueryReader()
    creator = UserQueryCreator()
    destroyer = UserQueryDestroyer()
    updator = UserQueryUpdator()
