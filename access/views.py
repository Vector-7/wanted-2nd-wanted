from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from access.utils.managers import SignUpAuthenticationManager

from ast import literal_eval


class CertificateView(APIView):
    """
    이메일 인증 관련 API

    (GET)   /api/auth/certificate   이메일 인증 요청
    (POST)  /api/auth/certificate   이메일 인증 번호 매칭 및 토큰 발행
    """

    def get(self, request: Request):
        """
        GET-param: email
        """

        # get param에서 이메일 데이터 가져오기
        email = request.GET.get('email', None)
        if not email:
            return Response({'error': 'email data not found'})
        # TODO 해당 이메일이 이미 등록 되어 있는 지 확인하기
        # 인증 코드 보내기
        SignUpAuthenticationManager().request_code('napalosense@gmail.com')
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        """
        post-param
        {
            "email": <str:email>,
            "code": <str:code>
        }
        """

        # POST 데이터 파싱
        req_data = literal_eval(request.body.decode('utf-8'))
        code, email = req_data['code'], req_data['email']
        # 인증코드 매칭 확인
        try:
            is_matched = SignUpAuthenticationManager() \
                .match_code(code, email)
        except ValueError:
            return Response({'error': '인증 코드가 만료되었습니다.'},
                            status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not is_matched:
            return Response({'error': '잘못된 인증 코드 입력 입니다.'},
                            status.HTTP_400_BAD_REQUEST)
        # 토큰 생성
        # 이때 토큰 만료 시간은 5분이다.
        token = SignUpAuthenticationManager().auth(info_for_token=email)
        return Response({'token': token}, status.HTTP_200_OK)


class LoginView(APIView):
    """
    (POST)   /api/auth/login     로그인
    """

    def post(self, request):
        return Response({'hello': 'world'}, status=status.HTTP_200_OK)
