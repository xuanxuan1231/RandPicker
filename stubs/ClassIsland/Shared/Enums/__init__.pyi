import typing

class ActionSetStatus(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Normal : ActionSetStatus # 0
    Invoking : ActionSetStatus # 1
    IsOn : ActionSetStatus # 2
    Reverting : ActionSetStatus # 3


class TempClassPlanGroupType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Override : TempClassPlanGroupType # 0
    Inherit : TempClassPlanGroupType # 1


class TimeState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : TimeState # 0
    OnClass : TimeState # 1
    PrepareOnClass : TimeState # 2
    Breaking : TimeState # 3
    AfterSchool : TimeState # 4

