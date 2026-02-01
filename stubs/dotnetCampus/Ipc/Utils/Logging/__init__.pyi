import typing

class IpcLogger:
    def __init__(self, name: str) -> None: ...
    @property
    def MinLogLevel(self) -> LogLevel: ...
    @MinLogLevel.setter
    def MinLogLevel(self, value: LogLevel) -> LogLevel: ...
    def ToString(self) -> str: ...


class LogLevel(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Trace : LogLevel # 0
    Debug : LogLevel # 1
    Information : LogLevel # 2
    Warning : LogLevel # 3
    Error : LogLevel # 4
    Critical : LogLevel # 5
    None_ : LogLevel # 6

