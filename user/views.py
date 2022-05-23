from ast import literal_eval

# Create your views here.
import jwt.exceptions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from access.utils.permissions import SignUpPermissionChecker
from core.miniframework_on_django.query_layer.access_query.permission import PermissionList, PermissionSameUserChecker
from core.miniframework_on_django.system_layer.jwt.jwt import read_jwt
from user.utils.data_queries.user import UserQuery


class UserCreateView(APIView):
    """
    (POST) /api/users   회원 가입
    """

    def post(self, request: Request):

        # body JSON 데이터 꺼내오기
        req_data = literal_eval(request.body.decode('utf-8'))
        nickname, email, password, level = \
            req_data['nickname'], req_data['email'], \
            req_data['password'], req_data['level']

        try:
            # token 갖고오기
            token = request.headers['Access']
        except KeyError:
            return Response({'error': '접근할 수 없는 API 입니다.'},
                            status.HTTP_403_FORBIDDEN)
        # Permission Check
        try:
            PermissionList(
                req_permissions=[
                    SignUpPermissionChecker(),
                    PermissionSameUserChecker(target_user=email)
                ],
                decode_token_func=read_jwt,
                app_name='wanted-company-searcher'
            )(token)
        except (PermissionError, jwt.exceptions.DecodeError) as e:
            return Response({'error': '접근할 수 없는 API 입니다.'},
                            status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            res = UserQuery().create(nickname=nickname,
                                     email=email,
                                     password=password,
                                     level=level)
        except serializers.ValidationError as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)
        return Response(res, status.HTTP_201_CREATED)
