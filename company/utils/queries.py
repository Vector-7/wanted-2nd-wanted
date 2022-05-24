from core.miniframework_on_django.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework_on_django.query_layer.data_query.query_methods import QueryReader, QueryCreator


class UserQueryReader(QueryReader):
    def __call__(self, company_name, x_wanted_language, tags=None):
        pass


class UserQueryCreator(QueryCreator):
    def __call__(self, company_name, x_wanted_language, tags=None):
        pass


class CompanyQuery(QueryCRUDS):
    reader = UserQueryReader()
    creator = UserQueryCreator()
