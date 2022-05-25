from ast import literal_eval

import django.db.utils
import jwt.exceptions
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from company.utils.managers import CompanyManager
from core.miniframework_on_django.exc import TokenExpiredError


class CompanyCreateView(APIView):
    """
    (POST)  /api/company    회사 생성
    """

    def post(self, request):
        req_data = literal_eval(request.body.decode('utf-8'))
        try:
            res = CompanyManager()  \
                .create_company(**req_data,
                                lang=request.headers['X-Wanted-Language'],
                                access_token=request.headers['Access'])
        except KeyError:
            return Response({'error': '접근할 수 없는 API 입니다.'},
                            status.HTTP_403_FORBIDDEN)
        except TokenExpiredError:
            return Response({'error': '토큰이 만료되었습니다.'},
                            status.HTTP_403_FORBIDDEN)
        except (PermissionError, jwt.exceptions.DecodeError):
            return Response({'error': '유효한 토큰이 아닙니다.'},
                            status.HTTP_403_FORBIDDEN)
        except (serializers.ValidationError, django.db.utils.IntegrityError) as e:
            return Response(str(e),
                            status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(res, status.HTTP_201_CREATED)


class CompanyView(APIView):
    """
    (GET)   /api/companies/<company_name:str>   회사 검색
    (POST)  /api/companies/<company_name:str>   회사 정보 업데이트 (Not Implemented)
    (DELETE)/api/companies/<company_name:str>   회사 삭제 (Not Implemented)
    """
    def get(self, request, company_name):
        try:
            res = CompanyManager()  \
                .get_company_info(company_name=company_name,
                                  lang=request.headers['X-Wanted-Language'])
        except KeyError:
            return Response({'error': '언어가 설정되지 않았습니다.'},
                            status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not res:
            return Response({'error': '해당 회사를 찾을 수 없습니다.'},
                            status.HTTP_404_NOT_FOUND)
        return Response(res, status.HTTP_200_OK)


class CompanySearchView(APIView):
    """
    (GET)   /api/companies/search   검색
    """
    def get(self, request):
        """
        아직 완성 X
        """
        query = {
            'word': request.GET.get('query', None),
            'tags': request.GET.get('tags', ''),
        }
        try:
            res = CompanyManager()\
                .search_company(**query,
                                lang=request.headers['X-Wanted-Language'])
        except KeyError:
            return Response({'error': '언어가 설정되지 않았습니다.'},
                            status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(res, status.HTTP_201_CREATED)

