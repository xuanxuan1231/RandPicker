import typing, abc
from RP4CI.Shared.Models import NotifyResult

class IRPService(typing.Protocol):
    @abc.abstractmethod
    def Notify(self, result: NotifyResult) -> None: ...
    @abc.abstractmethod
    def PingService(self) -> str: ...

