from ast import literal_eval

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import serializers
from user.utils.data_queries.user import UserQuery


class UserCreateView(APIView):
    """
    (POST) /api/users
    """
    def post(self, request):
        req_data = literal_eval(request.body.decode('utf-8'))
        nickname, email, password, level = \
            req_data['nickname'], req_data['email'], \
            req_data['password'], req_data['level']
        try:
            res = UserQuery().create(nickname=nickname,
                                     email=email,
                                     password=password,
                                     level=level)
        except serializers.ValidationError as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)
        return Response(res, status.HTTP_201_CREATED)
