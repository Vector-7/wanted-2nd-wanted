from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Optional, Iterable


class PermissionChecker(metaclass=ABCMeta):
    @abstractmethod
    def check(self, user) -> bool:
        pass


class PermissionSameUserChecker(PermissionChecker, metaclass=ABCMeta):
    target_user: str

    def check(self, user):
        return user == self.target_user


class PermissionLevelChecker(PermissionChecker, metaclass=ABCMeta):
    level: Any

    def check(self, level: Any) -> bool:
        return level == self.level


class PermissionIssueChecker(PermissionChecker, metaclass=ABCMeta):
    issue: Any

    def check(self, issue: Any) -> bool:
        return issue == self.issue


class PermissionAllAllowed(PermissionChecker):

    def check(self, _) -> bool:
        return True


class PermissionList:
    required_permissions: Iterable[PermissionChecker]
    decode_token: Callable
    get_user_level: Optional[Callable]
    app_name: str

    def __init__(self, req_permissions, decode_token_func, app_name, get_user_level_func=None):
        self.required_permissions = req_permissions
        self.decode_token = decode_token_func
        self.get_user_level = get_user_level_func
        self.app_name = app_name

    def __call__(self, token):
        issue, user = self.decode_token(token, self.app_name)

        user_level = self.get_user_level(user) if self.get_user_level \
            else None

        for permission in self.required_permissions:
            checked_val = None
            if issubclass(type(permission), PermissionLevelChecker):
                checked_val = user_level
            elif issubclass(type(permission), PermissionIssueChecker):
                checked_val = issue
            else:
                checked_val = user
            if not permission.check(checked_val):
                raise PermissionError('User Permission Failed')
