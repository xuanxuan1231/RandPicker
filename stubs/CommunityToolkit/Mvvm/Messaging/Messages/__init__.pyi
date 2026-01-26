import typing, abc
from System.Collections.Generic import IAsyncEnumerable_1, IAsyncEnumerator_1, IReadOnlyCollection_1, IEnumerable_1, IEnumerator_1
from System.Threading import CancellationToken
from System.Threading.Tasks import Task_1
from System import Func_2
from System.Runtime.CompilerServices import TaskAwaiter_1

class AsyncCollectionRequestMessage_GenericClasses(abc.ABCMeta):
    Generic_AsyncCollectionRequestMessage_GenericClasses_AsyncCollectionRequestMessage_1_T = typing.TypeVar('Generic_AsyncCollectionRequestMessage_GenericClasses_AsyncCollectionRequestMessage_1_T')
    def __getitem__(self, types : typing.Type[Generic_AsyncCollectionRequestMessage_GenericClasses_AsyncCollectionRequestMessage_1_T]) -> typing.Type[AsyncCollectionRequestMessage_1[Generic_AsyncCollectionRequestMessage_GenericClasses_AsyncCollectionRequestMessage_1_T]]: ...

AsyncCollectionRequestMessage : AsyncCollectionRequestMessage_GenericClasses

AsyncCollectionRequestMessage_1_T = typing.TypeVar('AsyncCollectionRequestMessage_1_T')
class AsyncCollectionRequestMessage_1(typing.Generic[AsyncCollectionRequestMessage_1_T], IAsyncEnumerable_1[AsyncCollectionRequestMessage_1_T]):
    def __init__(self) -> None: ...
    @property
    def CancellationToken(self) -> CancellationToken: ...
    def GetAsyncEnumerator(self, cancellationToken: CancellationToken = ...) -> IAsyncEnumerator_1[AsyncCollectionRequestMessage_1_T]: ...
    def GetResponsesAsync(self, cancellationToken: CancellationToken = ...) -> Task_1[IReadOnlyCollection_1[AsyncCollectionRequestMessage_1_T]]: ...
    # Skipped Reply due to it being static, abstract and generic.

    Reply : Reply_MethodGroup[AsyncCollectionRequestMessage_1_T]
    Reply_MethodGroup_AsyncCollectionRequestMessage_1_T = typing.TypeVar('Reply_MethodGroup_AsyncCollectionRequestMessage_1_T')
    class Reply_MethodGroup(typing.Generic[Reply_MethodGroup_AsyncCollectionRequestMessage_1_T]):
        Reply_MethodGroup_AsyncCollectionRequestMessage_1_T = AsyncCollectionRequestMessage_1.Reply_MethodGroup_AsyncCollectionRequestMessage_1_T
        @typing.overload
        def __call__(self, response: Func_2[CancellationToken, Task_1[Reply_MethodGroup_AsyncCollectionRequestMessage_1_T]]) -> None:...
        @typing.overload
        def __call__(self, response: Task_1[Reply_MethodGroup_AsyncCollectionRequestMessage_1_T]) -> None:...
        @typing.overload
        def __call__(self, response: Reply_MethodGroup_AsyncCollectionRequestMessage_1_T) -> None:...



class AsyncRequestMessage_GenericClasses(abc.ABCMeta):
    Generic_AsyncRequestMessage_GenericClasses_AsyncRequestMessage_1_T = typing.TypeVar('Generic_AsyncRequestMessage_GenericClasses_AsyncRequestMessage_1_T')
    def __getitem__(self, types : typing.Type[Generic_AsyncRequestMessage_GenericClasses_AsyncRequestMessage_1_T]) -> typing.Type[AsyncRequestMessage_1[Generic_AsyncRequestMessage_GenericClasses_AsyncRequestMessage_1_T]]: ...

AsyncRequestMessage : AsyncRequestMessage_GenericClasses

AsyncRequestMessage_1_T = typing.TypeVar('AsyncRequestMessage_1_T')
class AsyncRequestMessage_1(typing.Generic[AsyncRequestMessage_1_T]):
    def __init__(self) -> None: ...
    @property
    def HasReceivedResponse(self) -> bool: ...
    @HasReceivedResponse.setter
    def HasReceivedResponse(self, value: bool) -> bool: ...
    @property
    def Response(self) -> Task_1[AsyncRequestMessage_1_T]: ...
    def GetAwaiter(self) -> TaskAwaiter_1[AsyncRequestMessage_1_T]: ...
    # Skipped Reply due to it being static, abstract and generic.

    Reply : Reply_MethodGroup[AsyncRequestMessage_1_T]
    Reply_MethodGroup_AsyncRequestMessage_1_T = typing.TypeVar('Reply_MethodGroup_AsyncRequestMessage_1_T')
    class Reply_MethodGroup(typing.Generic[Reply_MethodGroup_AsyncRequestMessage_1_T]):
        Reply_MethodGroup_AsyncRequestMessage_1_T = AsyncRequestMessage_1.Reply_MethodGroup_AsyncRequestMessage_1_T
        @typing.overload
        def __call__(self, response: Task_1[Reply_MethodGroup_AsyncRequestMessage_1_T]) -> None:...
        @typing.overload
        def __call__(self, response: Reply_MethodGroup_AsyncRequestMessage_1_T) -> None:...



class CollectionRequestMessage_GenericClasses(abc.ABCMeta):
    Generic_CollectionRequestMessage_GenericClasses_CollectionRequestMessage_1_T = typing.TypeVar('Generic_CollectionRequestMessage_GenericClasses_CollectionRequestMessage_1_T')
    def __getitem__(self, types : typing.Type[Generic_CollectionRequestMessage_GenericClasses_CollectionRequestMessage_1_T]) -> typing.Type[CollectionRequestMessage_1[Generic_CollectionRequestMessage_GenericClasses_CollectionRequestMessage_1_T]]: ...

CollectionRequestMessage : CollectionRequestMessage_GenericClasses

CollectionRequestMessage_1_T = typing.TypeVar('CollectionRequestMessage_1_T')
class CollectionRequestMessage_1(typing.Generic[CollectionRequestMessage_1_T], IEnumerable_1[CollectionRequestMessage_1_T]):
    def __init__(self) -> None: ...
    @property
    def Responses(self) -> IReadOnlyCollection_1[CollectionRequestMessage_1_T]: ...
    def GetEnumerator(self) -> IEnumerator_1[CollectionRequestMessage_1_T]: ...
    def Reply(self, response: CollectionRequestMessage_1_T) -> None: ...


class PropertyChangedMessage_GenericClasses(abc.ABCMeta):
    Generic_PropertyChangedMessage_GenericClasses_PropertyChangedMessage_1_T = typing.TypeVar('Generic_PropertyChangedMessage_GenericClasses_PropertyChangedMessage_1_T')
    def __getitem__(self, types : typing.Type[Generic_PropertyChangedMessage_GenericClasses_PropertyChangedMessage_1_T]) -> typing.Type[PropertyChangedMessage_1[Generic_PropertyChangedMessage_GenericClasses_PropertyChangedMessage_1_T]]: ...

PropertyChangedMessage : PropertyChangedMessage_GenericClasses

PropertyChangedMessage_1_T = typing.TypeVar('PropertyChangedMessage_1_T')
class PropertyChangedMessage_1(typing.Generic[PropertyChangedMessage_1_T]):
    def __init__(self, sender: typing.Any, propertyName: str, oldValue: PropertyChangedMessage_1_T, newValue: PropertyChangedMessage_1_T) -> None: ...
    @property
    def NewValue(self) -> PropertyChangedMessage_1_T: ...
    @property
    def OldValue(self) -> PropertyChangedMessage_1_T: ...
    @property
    def PropertyName(self) -> str: ...
    @property
    def Sender(self) -> typing.Any: ...


class RequestMessage_GenericClasses(abc.ABCMeta):
    Generic_RequestMessage_GenericClasses_RequestMessage_1_T = typing.TypeVar('Generic_RequestMessage_GenericClasses_RequestMessage_1_T')
    def __getitem__(self, types : typing.Type[Generic_RequestMessage_GenericClasses_RequestMessage_1_T]) -> typing.Type[RequestMessage_1[Generic_RequestMessage_GenericClasses_RequestMessage_1_T]]: ...

RequestMessage : RequestMessage_GenericClasses

RequestMessage_1_T = typing.TypeVar('RequestMessage_1_T')
class RequestMessage_1(typing.Generic[RequestMessage_1_T]):
    def __init__(self) -> None: ...
    @property
    def HasReceivedResponse(self) -> bool: ...
    @HasReceivedResponse.setter
    def HasReceivedResponse(self, value: bool) -> bool: ...
    @property
    def Response(self) -> RequestMessage_1_T: ...
    # Operator not supported op_Implicit(message: RequestMessage`1)
    def Reply(self, response: RequestMessage_1_T) -> None: ...


class ValueChangedMessage_GenericClasses(abc.ABCMeta):
    Generic_ValueChangedMessage_GenericClasses_ValueChangedMessage_1_T = typing.TypeVar('Generic_ValueChangedMessage_GenericClasses_ValueChangedMessage_1_T')
    def __getitem__(self, types : typing.Type[Generic_ValueChangedMessage_GenericClasses_ValueChangedMessage_1_T]) -> typing.Type[ValueChangedMessage_1[Generic_ValueChangedMessage_GenericClasses_ValueChangedMessage_1_T]]: ...

ValueChangedMessage : ValueChangedMessage_GenericClasses

ValueChangedMessage_1_T = typing.TypeVar('ValueChangedMessage_1_T')
class ValueChangedMessage_1(typing.Generic[ValueChangedMessage_1_T]):
    def __init__(self, value: ValueChangedMessage_1_T) -> None: ...
    @property
    def Value(self) -> ValueChangedMessage_1_T: ...

