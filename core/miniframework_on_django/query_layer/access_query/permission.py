from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Optional, Iterable


class PermissionChecker(metaclass=ABCMeta):
    """
    사용자 권한을 체크하는 데 사용된다.
    """
    @abstractmethod
    def check(self, user) -> bool:
        """
        사용자 권한 체크
        
        :param user: 검수 대상 클라이언트
        """
        pass


class PermissionSameUserChecker(PermissionChecker):
    """
    해당 유저가 같은 유저인 지 확인한다.

    예를 들어 회사를 삭제할 경우 해당 회사를 만든 사람만이 삭제할 수 있어야 한다.
    """
    target_user: str

    def __init__(self, target_user):
        self.target_user = target_user

    def check(self, user):
        return user == self.target_user


class PermissionLevelChecker(PermissionChecker, metaclass=ABCMeta):
    """
    사용자의 수준(Admin, Client 등...)을 체크한다.
    """
    level: Any

    def check(self, level: Any) -> bool:
        return level == self.level


class PermissionIssueChecker(PermissionChecker, metaclass=ABCMeta):
    """
    사용자의 목표를 체크한다.

    예를 들어 패스워드 변경이나, 회원 가입이 이에 포함된다.
    """
    issue: Any

    def check(self, issue: Any) -> bool:
        return issue == self.issue


class PermissionAllAllowed(PermissionChecker):
    """
    모든 조건 허용
    """

    def check(self, _) -> bool:
        return True


class PermissionList:
    """
    다수의 Permission 조건을 처리한느데 사용된다.

    해당 클래스는 컴포지션을 목적으로 한 클래스로 상속 보다는 변수로 사용하는 것을 권장한다.
    
    (Not Implemented) 해당 클래스는 Permission에 대흔 OR연산만 되고 AND 연산이 안되는 상황이다.
    클래스를 분할 하거나, PermssionManager를 따로 만들 예정

    :variable required_permissions: Permission 모음
    :variable decode_token: token을 디코딩 할 때 사용하는 함수
    :variable get_user_level: User의 수준을 확인할 때 사용되는 함수
    :variable app_name: jwt 토큰에 사용
    """
    required_permissions: Iterable[PermissionChecker]
    decode_token: Callable
    get_user_level: Optional[Callable]
    app_name: str

    def __init__(self,
                 req_permissions,
                 decode_token_func,
                 app_name,
                 get_user_level_func=None):
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
