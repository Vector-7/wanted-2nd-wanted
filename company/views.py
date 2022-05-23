from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CompanyCreateView(APIView):
    """
    (POST)  /api/company    회사 생성
    """

    def post(self, request):
        return Response({'hello': 'world'}, status.HTTP_201_CREATED)


class CompanyView(APIView):
    """
    (GET)   /api/companies/<company_name:str>   회사 검색
    (POST)  /api/companies/<company_name:str>   회사 정보 업데이트 (Not Implemented)
    (DELETE)/api/companies/<company_name:str>   회사 삭제
    """
    pass


class CompanySearchView(APIView):
    """
    (GET)   /api/companies/search   검색
    """
    pass
