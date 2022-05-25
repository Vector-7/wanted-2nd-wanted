from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ast import literal_eval

from access.utils.managers.frontend_managers import AuthenticationRemoteManager
from core.miniframework_on_django.exc import TokenExpiredError


class CertificateView(APIView):
    """
    이메일 인증 관련 API

    (GET)   /api/auth/certificate   이메일 인증 요청
    (POST)  /api/auth/certificate   이메일 인증 번호 매칭 및 토큰 발행
    """
    def get(self, request: Request):
        """
        GET-param: email
        GET-param: issue (sign-up, finding-password)
        """
        try:
            AuthenticationRemoteManager() \
                .request_auth_code(email=request.GET.get('email', None),
                                   issue=request.GET.get('issue', None))
        except TypeError:
            return Response({'error': '이메일을 입력하세요'},
                            status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': '이미 계정이 있는 이메일 입니다.'},
                            status.HTTP_400_BAD_REQUEST)
        except PermissionError:
            return Response({'error': '접근할 수 없는 API 입니다.'},
                            status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        """
        토큰 발행 (회원 가입, 패스워드 찾기)

        post-param
        {
            "email": <str:email>,
            "code": <str:code>,
            "issue": "sign-up" or "finding-password"
        }
        """
        # POST 데이터 파싱
        req_data = literal_eval(request.body.decode('utf-8'))
        # 인증코드 매칭 확인
        try:
            token = AuthenticationRemoteManager()   \
                .request_token_for_certaion_issue(**req_data)
        except TokenExpiredError:
            return Response({'error': '인증 코드가 만료되었습니다.'},
                            status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': '잘못된 인증 코드 입력 입니다.'},
                            status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'token': token}, status.HTTP_200_OK)


class LoginView(APIView):
    """
    (POST)   /api/auth/login     로그인
    """
    def post(self, request):
        """
        post-param
        {
            "email": <str:email>,
            "password": <str:password>
        }
        """
        # 데이터 추출
        req_data = literal_eval(request.body.decode('utf-8'))
        # 토큰 리턴
        try:
            token = AuthenticationRemoteManager()   \
                .request_login(**req_data)
        except PermissionError:
            # 로그인 실패
            return Response({'error': '로그인 실패'},
                            status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            # 잘못된 데이터
            return Response({'error': '잘못된 접근'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'server error'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'token': token}, status=status.HTTP_200_OK)
