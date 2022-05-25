from ast import literal_eval

import django.db.utils
import jwt.exceptions
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from company.utils.managers import CompanyManager
from core.miniframework_on_django.exc import TokenExpiredError


# noinspection PyMethodMayBeStatic,PyBroadException,SpellCheckingInspection
class CompanyCreateView(APIView):
    """
    (POST)  /api/company    회사 생성
    """

    def post(self, request):
        req_data = literal_eval(request.body.decode('utf-8'))
        try:
            res = CompanyManager() \
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
        except Exception:
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(res, status.HTTP_201_CREATED)


# noinspection PyMethodMayBeStatic,SpellCheckingInspection,PyBroadException
class CompanyView(APIView):
    """
    (GET)   /api/companies/<company_name:str>   회사 검색
    (POST)  /api/companies/<company_name:str>   회사 정보 업데이트
    (DELETE)/api/companies/<company_name:str>   회사 삭제
    """

    def get(self, request, company_name):
        try:
            res = CompanyManager() \
                .get_company_info(company_name=company_name,
                                  lang=request.headers['X-Wanted-Language'])
        except KeyError:
            return Response({'error': '언어가 설정되지 않았습니다.'},
                            status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not res:
            return Response({'error': '해당 회사를 찾을 수 없습니다.'},
                            status.HTTP_404_NOT_FOUND)
        return Response(res, status.HTTP_200_OK)

    def patch(self, request, company_name):
        try:
            req_data = literal_eval(request.body.decode('utf-8'))
            res = CompanyManager() \
                .update_company(**req_data,
                                target_company=company_name,
                                lang=request.headers['X-Wanted-Language'],
                                access_token=request.headers['Access'])
        except KeyError:
            return Response({'error': '접근할 수 없는 API 입니다.'},
                            status.HTTP_403_FORBIDDEN)
        except TokenExpiredError:
            return Response({'error': '토큰이 만료되었습니다.'},
                            status.HTTP_403_FORBIDDEN)
        except (PermissionError, jwt.exceptions.DecodeError):
            return Response({'error': '유효한 토큰이 아닙니다.'}, status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            print(e)
            return Response({'error': '수정하고자 하는 회사가 없습니다.'},
                            status.HTTP_404_NOT_FOUND)
        except (serializers.ValidationError, django.db.utils.IntegrityError) as e:
            return Response(str(e),
                            status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(res, status.HTTP_200_OK)

    def delete(self, request, company_name):
        try:
            CompanyManager() \
                .remove_company(company_name=company_name,
                                lang=request.headers['X-Wanted-Language'],
                                access_token=request.headers['Access'])
        except KeyError:
            return Response({'error': '접근할 수 없는 API 입니다.'},
                            status.HTTP_403_FORBIDDEN)
        except TokenExpiredError:
            return Response({'error': '토큰이 만료되었습니다.'},
                            status.HTTP_403_FORBIDDEN)
        except (PermissionError, jwt.exceptions.DecodeError):
            return Response({'error': '유효한 토큰이 아닙니다.'}, status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({'error': '삭제하고자 하는 회사가 없습니다.'},
                            status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)


# noinspection PyMethodMayBeStatic,PyBroadException,SpellCheckingInspection
class CompanySearchView(APIView):
    """
    (GET)   /api/search/companies   검색
    """

    def get(self, request):
        query = {
            'word': request.GET.get('query', None),
            'tags': request.GET.get('tags', ''),
        }
        try:
            res = CompanyManager() \
                .search_company_by_contain_word(
                word=query['word'],
                lang=request.headers['X-Wanted-Language'])
        except KeyError:
            return Response({'error': '언어가 설정되지 않았습니다.'},
                            status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(res, status.HTTP_200_OK)
