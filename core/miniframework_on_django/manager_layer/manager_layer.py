from abc import ABCMeta


class BaseManagerLayer(metaclass=ABCMeta):
    pass


class FrontendManagerLayer(BaseManagerLayer, metaclass=ABCMeta):
    """
    Frontend 계열의 Manager를 선언할 때 사용한다.

    Frontend로 선언된 Manager들은 어디든지 사용할 수 있다.
    즉, View  단위에서도 사용할 수 있고 같은 Frontend Manager단에서도 사용할 수 있다.

    (Not Implemented) 최상단에서 반응하며 상태 무결성을 위해 Singletone Pattern이 적용될 예정이다.
    """
    pass


class BackendManagerLayer(BaseManagerLayer, metaclass=ABCMeta):
    """
    Backend 계열의 Manager를 선언할 때 사용한다.

    FrontEnd Manager의 기능을 뒤에서 지원할 때 사용되며
    Frontend Manager 단에서만 사용할 수 있고 View단에서는 사용할 수 없다.

    (Not Implemented) FrontEnd와는 달리 FrontendManager가 당장 쓰고 버리는 용도의 Manager로
    Singletone Pattern를 적용하지 않는다. 단, 대용량 트래픽 시, 지나친 Instance 갯수를 줄이기 위해
    인스턴스 생성에 제한을 둘 예정이며 Memory Pool을 자체 구현하여 관리할 예정. 일정 갯수 이상을 전부 쓰게 되면
    다음 클라이언트는 일부 Manager가 할당 해제될 때 까지 기다리게 된다.
    """
    pass
