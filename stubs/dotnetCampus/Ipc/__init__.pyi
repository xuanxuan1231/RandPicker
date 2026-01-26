import typing, abc
from dotnetCampus.Ipc.Context import IpcContext, IIpcRequestContext
from System.Threading.Tasks import Task_1, Task
from dotnetCampus.Ipc.Messages import IIpcResponseMessage, IpcMessage
from System import Array_1

class IIpcProvider(typing.Protocol):
    @property
    def IpcContext(self) -> IpcContext: ...


class IIpcRequestHandler(typing.Protocol):
    @abc.abstractmethod
    def HandleRequest(self, requestContext: IIpcRequestContext) -> Task_1[IIpcResponseMessage]: ...


class IpcMessageWriter(IRawMessageWriter):
    def __init__(self, messageWriter: IRawMessageWriter) -> None: ...
    # Skipped WriteMessageAsync due to it being static, abstract and generic.

    WriteMessageAsync : WriteMessageAsync_MethodGroup
    class WriteMessageAsync_MethodGroup:
        @typing.overload
        def __call__(self, message: IpcMessage) -> Task:...
        @typing.overload
        def __call__(self, message: str, tag: str = ...) -> Task:...
        @typing.overload
        def __call__(self, buffer: Array_1[int], offset: int, count: int, tag: str = ...) -> Task:...



class IPeerProxy(typing.Protocol):
    @property
    def PeerName(self) -> str: ...
    @abc.abstractmethod
    def GetResponseAsync(self, request: IpcMessage) -> Task_1[IpcMessage]: ...
    @abc.abstractmethod
    def NotifyAsync(self, request: IpcMessage) -> Task: ...


class IRawMessageWriter(typing.Protocol):
    @abc.abstractmethod
    def WriteMessageAsync(self, data: Array_1[int], offset: int, length: int, tag: str = ...) -> Task: ...

