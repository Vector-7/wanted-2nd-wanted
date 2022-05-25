from ast import literal_eval

# Create your views here.
import jwt.exceptions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from access.utils.managers.frontend_managers import (
    AuthenticationRemoteManager,
)
from user.utils.managers.frontend_manager import UserManager, PasswordMatchFailedError
from user.models import User


class UserCreateView(APIView):
    """
    (POST)      /api/users  회원 가입
    (GET)       /api/users  회원 정보 가져오기
    (PATCH)     /api/users  회원 정보 수정
    (DELETE)    /api/usrs   회원 정보 삭제
    """

    def post(self, request):
        req_data = literal_eval(request.body.decode('utf-8'))
        try:
            res = AuthenticationRemoteManager() \
                .request_sign_up(**req_data, access_token=request.headers['Access'])
        except KeyError:
            return Response({'error': '접근할 수 없는 API 입니다.'},
                            status.HTTP_403_FORBIDDEN)
        except (PermissionError, jwt.exceptions.DecodeError):
            return Response({'error': '유효한 token이 아닙니다'},
                            status.HTTP_403_FORBIDDEN)
        except serializers.ValidationError as e:
            return Response(str(e),
                            status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(res, status.HTTP_201_CREATED)

    def delete(self, request):
        """
        input json data
        { "password": <확인 패스워드> }
        """
        try:
            req_data = literal_eval(request.body.decode('utf-8'))
            UserManager().signout(**req_data, access_token=request.headers['Access'])
        except KeyError:
            return Response({'error': '접근할 수 없는 API 입니다.'},
                            status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({'error': '없는 계정 입니다.'},
                            status.HTTP_404_NOT_FOUND)
        except (PermissionError, jwt.exceptions.DecodeError):
            return Response({'error': '유호한 토큰이 아닙니다.'},
                            status.HTTP_403_FORBIDDEN)
        except PasswordMatchFailedError:
            return Response({'error': '패스워드가 일치하지 않습니다.'},
                            status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request):
        """
        input form = {
            "nickname": "<new nickname>".
            "password": "<password>",
            "issue": "change-info",
            "
        }
        """
        try:
            req_data = literal_eval(request.body.decode('utf-8'))
            res = UserManager().update_user(**req_data,
                                            access_token=request.headers['Access'])
        except KeyError:
            return Response({'error': '접근할 수 없는 API 입니다.'},
                            status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({'error': '알 수 없는 접근 입니다.'},
                            status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': '없는 계정 입니다.'},
                            status.HTTP_404_NOT_FOUND)
        except (PermissionError, jwt.exceptions.DecodeError):
            return Response({'error': '유호한 토큰이 아닙니다.'},
                            status.HTTP_403_FORBIDDEN)
        except PasswordMatchFailedError:
            return Response({'error': '패스워드가 일치하지 않습니다.'},
                            status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(res, status=status.HTTP_200_OK)


class UserView(APIView):
    """
    (GET)   /api/users/:name    다른 유저의 정보 가져오기
    """

    def get(self, request, name):
        raise NotImplemented()
