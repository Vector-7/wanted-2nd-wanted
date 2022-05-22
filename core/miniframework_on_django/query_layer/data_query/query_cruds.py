from typing import Optional

from core.miniframework_on_django.query_layer.data_query.query_methods import *


class QueryCRUD(metaclass=ABCMeta):
    creator: Optional[QueryCreator] = None
    reader: Optional[QueryReader] = None
    updator: Optional[QueryUpdator] = None
    destroyer: Optional[QueryDestroyer] = None

    def _run_query(self, method: Optional[QueryMethod], *args, **kwargs):
        if not method:
            raise PermissionError('method not allowed')
        return method(*args, **kwargs)

    def create(self, *args, **kwargs):
        return self._run_query(self.creator, *args, **kwargs)

    def read(self, *args, **kwargs):
        return self._run_query(self.reader, *args, **kwargs)

    def update(self, *args, **kwargs):
        return self._run_query(self.updator, *args, **kwargs)

    def destroy(self, *args, **kwargs):
        return self._run_query(self.destroyer, *args, **kwargs)


class QueryCRUDS(QueryCRUD):
    searcher: Optional[QuerySearcher] = None

    def search(self, *args, **kwargs):
        return self._run_query(self.searcher, *args, **kwargs)
