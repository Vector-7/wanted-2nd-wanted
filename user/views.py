from ast import literal_eval

# Create your views here.
import jwt.exceptions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from access.utils.managers.frontend_managers import AuthenticationRemoteManager


class UserCreateView(APIView):
    """
    (POST) /api/users   회원 가입
    """
    def post(self, request: Request):
        req_data = literal_eval(request.body.decode('utf-8'))
        try:
            res = AuthenticationRemoteManager() \
                .request_sign_up(**req_data, access_token=request.headers['Access'])
        except KeyError:
            # header에 access token 못찾음
            return Response({'error': '접근할 수 없는 API 입니다.'}, status.HTTP_403_FORBIDDEN)
        except (PermissionError, jwt.exceptions.DecodeError):
            # 디코딩 실패 또는 Permission Failed
            return Response({'error': '유효한 token이 아닙니다'}, status.HTTP_403_FORBIDDEN)
        except serializers.ValidationError as e:
            # 유저 데이터를 생성하는 데 규칙에 맞지 않음
            return Response(str(e), status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # 기타 일 수 없는 에러
            return Response({'error': 'server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(res, status.HTTP_201_CREATED)
