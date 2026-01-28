import typing, abc

class ICommand(typing.Protocol):
    @abc.abstractmethod
    def CanExecute(self, parameter: typing.Any) -> bool: ...
    @abc.abstractmethod
    def Execute(self, parameter: typing.Any) -> None: ...

