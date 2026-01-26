import typing, abc

class CustomIpcThreadPoolBase(abc.ABC):
    pass


class IpcTaskScheduling(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    GlobalConcurrent : IpcTaskScheduling # 0
    LocalOneByOne : IpcTaskScheduling # 1

