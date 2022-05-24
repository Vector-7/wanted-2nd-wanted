from core.miniframework_on_django.manager_layer.manager import CRUDManager
from user.utils.queries import UserQuery


class UserManager(CRUDManager):
    cruds_query = UserQuery()
