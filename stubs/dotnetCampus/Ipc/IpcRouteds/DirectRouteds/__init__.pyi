import typing, clr, abc
from dotnetCampus.Ipc.Pipes import IpcProvider, PeerProxy
from System.Threading.Tasks import Task_1, Task
from System import Exception, Func_2, Func_3, Action_1, Action_2, Func_1, Action, Span_1
from dotnetCampus.Ipc.Context import IpcConfiguration
from dotnetCampus.Ipc import IPeerProxy
from dotnetCampus.Ipc.Messages import IpcMessageBody, IpcMessage

class IpcDirectRoutedClientProxyBase(abc.ABC):
    pass


class IpcDirectRoutedProviderBase(abc.ABC):
    @property
    def IpcProvider(self) -> IpcProvider: ...
    def StartServer(self) -> None: ...


class JsonIpcDirectRoutedClientProxy(IpcDirectRoutedClientProxyBase):
    def __init__(self, peerProxy: PeerProxy) -> None: ...
    # Skipped GetResponseAsync due to it being static, abstract and generic.

    GetResponseAsync : GetResponseAsync_MethodGroup
    class GetResponseAsync_MethodGroup:
        def __getitem__(self, t:typing.Type[GetResponseAsync_1_T1]) -> GetResponseAsync_1[GetResponseAsync_1_T1]: ...

        GetResponseAsync_1_T1 = typing.TypeVar('GetResponseAsync_1_T1')
        class GetResponseAsync_1(typing.Generic[GetResponseAsync_1_T1]):
            GetResponseAsync_1_TResponse = JsonIpcDirectRoutedClientProxy.GetResponseAsync_MethodGroup.GetResponseAsync_1_T1
            @typing.overload
            def __call__(self, routedPath: str) -> Task_1[GetResponseAsync_1_TResponse]:...
            @typing.overload
            def __call__(self, routedPath: str, obj: typing.Any) -> Task_1[GetResponseAsync_1_TResponse]:...


    # Skipped NotifyAsync due to it being static, abstract and generic.

    NotifyAsync : NotifyAsync_MethodGroup
    class NotifyAsync_MethodGroup:
        def __getitem__(self, t:typing.Type[NotifyAsync_1_T1]) -> NotifyAsync_1[NotifyAsync_1_T1]: ...

        NotifyAsync_1_T1 = typing.TypeVar('NotifyAsync_1_T1')
        class NotifyAsync_1(typing.Generic[NotifyAsync_1_T1]):
            NotifyAsync_1_T = JsonIpcDirectRoutedClientProxy.NotifyAsync_MethodGroup.NotifyAsync_1_T1
            def __call__(self, routedPath: str, obj: NotifyAsync_1_T) -> Task:...

        def __call__(self, routedPath: str) -> Task:...



class JsonIpcDirectRoutedContext:
    def __init__(self, peerName: str) -> None: ...
    @property
    def PeerName(self) -> str: ...


class JsonIpcDirectRoutedLogStateMessageType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ReceiveNotify : JsonIpcDirectRoutedLogStateMessageType # 0
    ReceiveRequest : JsonIpcDirectRoutedLogStateMessageType # 1
    SendResponse : JsonIpcDirectRoutedLogStateMessageType # 2
    SendNotify : JsonIpcDirectRoutedLogStateMessageType # 3
    SendRequest : JsonIpcDirectRoutedLogStateMessageType # 4
    ReceiveResponse : JsonIpcDirectRoutedLogStateMessageType # 5


class JsonIpcDirectRoutedMessageLogState:
    @property
    def LocalPeerName(self) -> str: ...
    @property
    def MessageType(self) -> JsonIpcDirectRoutedLogStateMessageType: ...
    @property
    def RemotePeerName(self) -> str: ...
    @property
    def RoutedPath(self) -> str: ...
    @staticmethod
    def Format(state: JsonIpcDirectRoutedMessageLogState, exception: Exception) -> str: ...
    def GetJsonText(self) -> str: ...


class JsonIpcDirectRoutedProvider(IpcDirectRoutedProviderBase):
    @typing.overload
    def __init__(self, ipcProvider: IpcProvider) -> None: ...
    @typing.overload
    def __init__(self, pipeName: str = ..., ipcConfiguration: IpcConfiguration = ...) -> None: ...
    @property
    def IpcProvider(self) -> IpcProvider: ...
    def GetAndConnectClientAsync(self, serverPeerName: str) -> Task_1[JsonIpcDirectRoutedClientProxy]: ...
    # Skipped AddNotifyHandler due to it being static, abstract and generic.

    AddNotifyHandler : AddNotifyHandler_MethodGroup
    class AddNotifyHandler_MethodGroup:
        def __getitem__(self, t:typing.Type[AddNotifyHandler_1_T1]) -> AddNotifyHandler_1[AddNotifyHandler_1_T1]: ...

        AddNotifyHandler_1_T1 = typing.TypeVar('AddNotifyHandler_1_T1')
        class AddNotifyHandler_1(typing.Generic[AddNotifyHandler_1_T1]):
            AddNotifyHandler_1_T = JsonIpcDirectRoutedProvider.AddNotifyHandler_MethodGroup.AddNotifyHandler_1_T1
            @typing.overload
            def __call__(self, routedPath: str, handler: Func_2[AddNotifyHandler_1_T, Task]) -> None:...
            @typing.overload
            def __call__(self, routedPath: str, handler: Func_3[AddNotifyHandler_1_T, JsonIpcDirectRoutedContext, Task]) -> None:...
            @typing.overload
            def __call__(self, routedPath: str, handler: Action_1[AddNotifyHandler_1_T]) -> None:...
            @typing.overload
            def __call__(self, routedPath: str, handler: Action_2[AddNotifyHandler_1_T, JsonIpcDirectRoutedContext]) -> None:...

        @typing.overload
        def __call__(self, routedPath: str, handler: Func_1[Task]) -> None:...
        @typing.overload
        def __call__(self, routedPath: str, handler: Action) -> None:...

    # Skipped AddRequestHandler due to it being static, abstract and generic.

    AddRequestHandler : AddRequestHandler_MethodGroup
    class AddRequestHandler_MethodGroup:
        @typing.overload
        def __getitem__(self, t:typing.Type[AddRequestHandler_1_T1]) -> AddRequestHandler_1[AddRequestHandler_1_T1]: ...

        AddRequestHandler_1_T1 = typing.TypeVar('AddRequestHandler_1_T1')
        class AddRequestHandler_1(typing.Generic[AddRequestHandler_1_T1]):
            AddRequestHandler_1_TResponse = JsonIpcDirectRoutedProvider.AddRequestHandler_MethodGroup.AddRequestHandler_1_T1
            @typing.overload
            def __call__(self, routedPath: str, handler: Func_1[Task_1[AddRequestHandler_1_TResponse]]) -> None:...
            @typing.overload
            def __call__(self, routedPath: str, handler: Func_1[AddRequestHandler_1_TResponse]) -> None:...

        @typing.overload
        def __getitem__(self, t:typing.Tuple[typing.Type[AddRequestHandler_2_T1], typing.Type[AddRequestHandler_2_T2]]) -> AddRequestHandler_2[AddRequestHandler_2_T1, AddRequestHandler_2_T2]: ...

        AddRequestHandler_2_T1 = typing.TypeVar('AddRequestHandler_2_T1')
        AddRequestHandler_2_T2 = typing.TypeVar('AddRequestHandler_2_T2')
        class AddRequestHandler_2(typing.Generic[AddRequestHandler_2_T1, AddRequestHandler_2_T2]):
            AddRequestHandler_2_TRequest = JsonIpcDirectRoutedProvider.AddRequestHandler_MethodGroup.AddRequestHandler_2_T1
            AddRequestHandler_2_TResponse = JsonIpcDirectRoutedProvider.AddRequestHandler_MethodGroup.AddRequestHandler_2_T2
            @typing.overload
            def __call__(self, routedPath: str, handler: Func_2[AddRequestHandler_2_TRequest, Task_1[AddRequestHandler_2_TResponse]]) -> None:...
            @typing.overload
            def __call__(self, routedPath: str, handler: Func_3[AddRequestHandler_2_TRequest, JsonIpcDirectRoutedContext, Task_1[AddRequestHandler_2_TResponse]]) -> None:...
            @typing.overload
            def __call__(self, routedPath: str, handler: Func_2[AddRequestHandler_2_TRequest, AddRequestHandler_2_TResponse]) -> None:...
            @typing.overload
            def __call__(self, routedPath: str, handler: Func_3[AddRequestHandler_2_TRequest, JsonIpcDirectRoutedContext, AddRequestHandler_2_TResponse]) -> None:...




class RawByteIpcDirectRoutedClientProxy(IpcDirectRoutedClientProxyBase):
    def __init__(self, peerProxy: IPeerProxy) -> None: ...
    def GetResponseAsync(self, routedPath: str, ipcMessageBody: IpcMessageBody) -> Task_1[IpcMessageBody]: ...
    # Skipped NotfiyAsync due to it being static, abstract and generic.

    NotfiyAsync : NotfiyAsync_MethodGroup
    class NotfiyAsync_MethodGroup:
        @typing.overload
        def __call__(self, routedPath: str, data: Span_1[int]) -> Task:...
        @typing.overload
        def __call__(self, routedPath: str, data: clr.Reference[IpcMessageBody]) -> Task:...



class RawByteIpcDirectRoutedProvider(IpcDirectRoutedProviderBase):
    @typing.overload
    def __init__(self, ipcProvider: IpcProvider) -> None: ...
    @typing.overload
    def __init__(self, pipeName: str = ..., ipcConfiguration: IpcConfiguration = ...) -> None: ...
    @property
    def IpcProvider(self) -> IpcProvider: ...
    # Skipped AddNotifyHandler due to it being static, abstract and generic.

    AddNotifyHandler : AddNotifyHandler_MethodGroup
    class AddNotifyHandler_MethodGroup:
        @typing.overload
        def __call__(self, routedPath: str, handler: Func_2[IpcMessageBody, Task]) -> None:...
        @typing.overload
        def __call__(self, routedPath: str, handler: Func_3[IpcMessageBody, JsonIpcDirectRoutedContext, Task]) -> None:...
        @typing.overload
        def __call__(self, routedPath: str, handler: Action_1[IpcMessageBody]) -> None:...
        @typing.overload
        def __call__(self, routedPath: str, handler: Action_2[IpcMessageBody, JsonIpcDirectRoutedContext]) -> None:...

    # Skipped AddRequestHandler due to it being static, abstract and generic.

    AddRequestHandler : AddRequestHandler_MethodGroup
    class AddRequestHandler_MethodGroup:
        @typing.overload
        def __call__(self, routedPath: str, handler: Func_2[IpcMessageBody, IpcMessage]) -> None:...
        @typing.overload
        def __call__(self, routedPath: str, handler: Func_3[IpcMessageBody, JsonIpcDirectRoutedContext, IpcMessage]) -> None:...
        @typing.overload
        def __call__(self, routedPath: str, handler: Func_2[IpcMessageBody, Task_1[IpcMessage]]) -> None:...
        @typing.overload
        def __call__(self, routedPath: str, handler: Func_3[IpcMessageBody, JsonIpcDirectRoutedContext, Task_1[IpcMessage]]) -> None:...


