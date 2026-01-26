import typing, abc
from System import IObservable_1, MulticastDelegate, IAsyncResult, AsyncCallback
from System.Reflection import MethodInfo

class IMessenger(typing.Protocol):
    @abc.abstractmethod
    def Cleanup(self) -> None: ...
    @abc.abstractmethod
    def Reset(self) -> None: ...
    # Skipped IsRegistered due to it being static, abstract and generic.

    IsRegistered : IsRegistered_MethodGroup
    class IsRegistered_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[IsRegistered_2_T1], typing.Type[IsRegistered_2_T2]]) -> IsRegistered_2[IsRegistered_2_T1, IsRegistered_2_T2]: ...

        IsRegistered_2_T1 = typing.TypeVar('IsRegistered_2_T1')
        IsRegistered_2_T2 = typing.TypeVar('IsRegistered_2_T2')
        class IsRegistered_2(typing.Generic[IsRegistered_2_T1, IsRegistered_2_T2]):
            IsRegistered_2_TMessage = IMessenger.IsRegistered_MethodGroup.IsRegistered_2_T1
            IsRegistered_2_TToken = IMessenger.IsRegistered_MethodGroup.IsRegistered_2_T2
            def __call__(self, recipient: typing.Any, token: IsRegistered_2_TToken) -> bool:...


    # Skipped Register due to it being static, abstract and generic.

    Register : Register_MethodGroup
    class Register_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[Register_3_T1], typing.Type[Register_3_T2], typing.Type[Register_3_T3]]) -> Register_3[Register_3_T1, Register_3_T2, Register_3_T3]: ...

        Register_3_T1 = typing.TypeVar('Register_3_T1')
        Register_3_T2 = typing.TypeVar('Register_3_T2')
        Register_3_T3 = typing.TypeVar('Register_3_T3')
        class Register_3(typing.Generic[Register_3_T1, Register_3_T2, Register_3_T3]):
            Register_3_TRecipient = IMessenger.Register_MethodGroup.Register_3_T1
            Register_3_TMessage = IMessenger.Register_MethodGroup.Register_3_T2
            Register_3_TToken = IMessenger.Register_MethodGroup.Register_3_T3
            def __call__(self, recipient: Register_3_TRecipient, token: Register_3_TToken, handler: MessageHandler_2[Register_3_TRecipient, Register_3_TMessage]) -> None:...


    # Skipped Send due to it being static, abstract and generic.

    Send : Send_MethodGroup
    class Send_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[Send_2_T1], typing.Type[Send_2_T2]]) -> Send_2[Send_2_T1, Send_2_T2]: ...

        Send_2_T1 = typing.TypeVar('Send_2_T1')
        Send_2_T2 = typing.TypeVar('Send_2_T2')
        class Send_2(typing.Generic[Send_2_T1, Send_2_T2]):
            Send_2_TMessage = IMessenger.Send_MethodGroup.Send_2_T1
            Send_2_TToken = IMessenger.Send_MethodGroup.Send_2_T2
            def __call__(self, message: Send_2_TMessage, token: Send_2_TToken) -> Send_2_TMessage:...


    # Skipped Unregister due to it being static, abstract and generic.

    Unregister : Unregister_MethodGroup
    class Unregister_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[Unregister_2_T1], typing.Type[Unregister_2_T2]]) -> Unregister_2[Unregister_2_T1, Unregister_2_T2]: ...

        Unregister_2_T1 = typing.TypeVar('Unregister_2_T1')
        Unregister_2_T2 = typing.TypeVar('Unregister_2_T2')
        class Unregister_2(typing.Generic[Unregister_2_T1, Unregister_2_T2]):
            Unregister_2_TMessage = IMessenger.Unregister_MethodGroup.Unregister_2_T1
            Unregister_2_TToken = IMessenger.Unregister_MethodGroup.Unregister_2_T2
            def __call__(self, recipient: typing.Any, token: Unregister_2_TToken) -> None:...


    # Skipped UnregisterAll due to it being static, abstract and generic.

    UnregisterAll : UnregisterAll_MethodGroup
    class UnregisterAll_MethodGroup:
        def __getitem__(self, t:typing.Type[UnregisterAll_1_T1]) -> UnregisterAll_1[UnregisterAll_1_T1]: ...

        UnregisterAll_1_T1 = typing.TypeVar('UnregisterAll_1_T1')
        class UnregisterAll_1(typing.Generic[UnregisterAll_1_T1]):
            UnregisterAll_1_TToken = IMessenger.UnregisterAll_MethodGroup.UnregisterAll_1_T1
            def __call__(self, recipient: typing.Any, token: UnregisterAll_1_TToken) -> None:...

        def __call__(self, recipient: typing.Any) -> None:...



class IMessengerExtensions(abc.ABC):
    # Skipped CreateObservable due to it being static, abstract and generic.

    CreateObservable : CreateObservable_MethodGroup
    class CreateObservable_MethodGroup:
        @typing.overload
        def __getitem__(self, t:typing.Type[CreateObservable_1_T1]) -> CreateObservable_1[CreateObservable_1_T1]: ...

        CreateObservable_1_T1 = typing.TypeVar('CreateObservable_1_T1')
        class CreateObservable_1(typing.Generic[CreateObservable_1_T1]):
            CreateObservable_1_TMessage = IMessengerExtensions.CreateObservable_MethodGroup.CreateObservable_1_T1
            def __call__(self, messenger: IMessenger) -> IObservable_1[CreateObservable_1_TMessage]:...

        @typing.overload
        def __getitem__(self, t:typing.Tuple[typing.Type[CreateObservable_2_T1], typing.Type[CreateObservable_2_T2]]) -> CreateObservable_2[CreateObservable_2_T1, CreateObservable_2_T2]: ...

        CreateObservable_2_T1 = typing.TypeVar('CreateObservable_2_T1')
        CreateObservable_2_T2 = typing.TypeVar('CreateObservable_2_T2')
        class CreateObservable_2(typing.Generic[CreateObservable_2_T1, CreateObservable_2_T2]):
            CreateObservable_2_TMessage = IMessengerExtensions.CreateObservable_MethodGroup.CreateObservable_2_T1
            CreateObservable_2_TToken = IMessengerExtensions.CreateObservable_MethodGroup.CreateObservable_2_T2
            def __call__(self, messenger: IMessenger, token: CreateObservable_2_TToken) -> IObservable_1[CreateObservable_2_TMessage]:...


    # Skipped IsRegistered due to it being static, abstract and generic.

    IsRegistered : IsRegistered_MethodGroup
    class IsRegistered_MethodGroup:
        def __getitem__(self, t:typing.Type[IsRegistered_1_T1]) -> IsRegistered_1[IsRegistered_1_T1]: ...

        IsRegistered_1_T1 = typing.TypeVar('IsRegistered_1_T1')
        class IsRegistered_1(typing.Generic[IsRegistered_1_T1]):
            IsRegistered_1_TMessage = IMessengerExtensions.IsRegistered_MethodGroup.IsRegistered_1_T1
            def __call__(self, messenger: IMessenger, recipient: typing.Any) -> bool:...


    # Skipped Register due to it being static, abstract and generic.

    Register : Register_MethodGroup
    class Register_MethodGroup:
        @typing.overload
        def __getitem__(self, t:typing.Type[Register_1_T1]) -> Register_1[Register_1_T1]: ...

        Register_1_T1 = typing.TypeVar('Register_1_T1')
        class Register_1(typing.Generic[Register_1_T1]):
            Register_1_TMessage = IMessengerExtensions.Register_MethodGroup.Register_1_T1
            @typing.overload
            def __call__(self, messenger: IMessenger, recipient: IRecipient_1[Register_1_TMessage]) -> None:...
            @typing.overload
            def __call__(self, messenger: IMessenger, recipient: typing.Any, handler: MessageHandler_2[typing.Any, Register_1_TMessage]) -> None:...

        @typing.overload
        def __getitem__(self, t:typing.Tuple[typing.Type[Register_2_T1], typing.Type[Register_2_T2]]) -> Register_2[Register_2_T1, Register_2_T2]: ...

        Register_2_T1 = typing.TypeVar('Register_2_T1')
        Register_2_T2 = typing.TypeVar('Register_2_T2')
        class Register_2(typing.Generic[Register_2_T1, Register_2_T2]):
            Register_2_TRecipient = IMessengerExtensions.Register_MethodGroup.Register_2_T1
            Register_2_TMessage = IMessengerExtensions.Register_MethodGroup.Register_2_T1
            Register_2_TMessage = IMessengerExtensions.Register_MethodGroup.Register_2_T2
            Register_2_TToken = IMessengerExtensions.Register_MethodGroup.Register_2_T2
            @typing.overload
            def __call__(self, messenger: IMessenger, recipient: Register_2_TRecipient, handler: MessageHandler_2[Register_2_TRecipient, Register_2_TMessage]) -> None:...
            @typing.overload
            def __call__(self, messenger: IMessenger, recipient: IRecipient_1[Register_2_TMessage], token: Register_2_TToken) -> None:...
            @typing.overload
            def __call__(self, messenger: IMessenger, recipient: typing.Any, token: Register_2_TToken, handler: MessageHandler_2[typing.Any, Register_2_TMessage]) -> None:...


    # Skipped RegisterAll due to it being static, abstract and generic.

    RegisterAll : RegisterAll_MethodGroup
    class RegisterAll_MethodGroup:
        def __getitem__(self, t:typing.Type[RegisterAll_1_T1]) -> RegisterAll_1[RegisterAll_1_T1]: ...

        RegisterAll_1_T1 = typing.TypeVar('RegisterAll_1_T1')
        class RegisterAll_1(typing.Generic[RegisterAll_1_T1]):
            RegisterAll_1_TToken = IMessengerExtensions.RegisterAll_MethodGroup.RegisterAll_1_T1
            def __call__(self, messenger: IMessenger, recipient: typing.Any, token: RegisterAll_1_TToken) -> None:...

        def __call__(self, messenger: IMessenger, recipient: typing.Any) -> None:...

    # Skipped Send due to it being static, abstract and generic.

    Send : Send_MethodGroup
    class Send_MethodGroup:
        @typing.overload
        def __getitem__(self, t:typing.Type[Send_1_T1]) -> Send_1[Send_1_T1]: ...

        Send_1_T1 = typing.TypeVar('Send_1_T1')
        class Send_1(typing.Generic[Send_1_T1]):
            Send_1_TMessage = IMessengerExtensions.Send_MethodGroup.Send_1_T1
            @typing.overload
            def __call__(self, messenger: IMessenger) -> Send_1_TMessage:...
            @typing.overload
            def __call__(self, messenger: IMessenger, message: Send_1_TMessage) -> Send_1_TMessage:...

        @typing.overload
        def __getitem__(self, t:typing.Tuple[typing.Type[Send_2_T1], typing.Type[Send_2_T2]]) -> Send_2[Send_2_T1, Send_2_T2]: ...

        Send_2_T1 = typing.TypeVar('Send_2_T1')
        Send_2_T2 = typing.TypeVar('Send_2_T2')
        class Send_2(typing.Generic[Send_2_T1, Send_2_T2]):
            Send_2_TMessage = IMessengerExtensions.Send_MethodGroup.Send_2_T1
            Send_2_TToken = IMessengerExtensions.Send_MethodGroup.Send_2_T2
            def __call__(self, messenger: IMessenger, token: Send_2_TToken) -> Send_2_TMessage:...


    # Skipped Unregister due to it being static, abstract and generic.

    Unregister : Unregister_MethodGroup
    class Unregister_MethodGroup:
        def __getitem__(self, t:typing.Type[Unregister_1_T1]) -> Unregister_1[Unregister_1_T1]: ...

        Unregister_1_T1 = typing.TypeVar('Unregister_1_T1')
        class Unregister_1(typing.Generic[Unregister_1_T1]):
            Unregister_1_TMessage = IMessengerExtensions.Unregister_MethodGroup.Unregister_1_T1
            def __call__(self, messenger: IMessenger, recipient: typing.Any) -> None:...




class IRecipient_GenericClasses(abc.ABCMeta):
    Generic_IRecipient_GenericClasses_IRecipient_1_TMessage = typing.TypeVar('Generic_IRecipient_GenericClasses_IRecipient_1_TMessage')
    def __getitem__(self, types : typing.Type[Generic_IRecipient_GenericClasses_IRecipient_1_TMessage]) -> typing.Type[IRecipient_1[Generic_IRecipient_GenericClasses_IRecipient_1_TMessage]]: ...

IRecipient : IRecipient_GenericClasses

IRecipient_1_TMessage = typing.TypeVar('IRecipient_1_TMessage', contravariant=True)
class IRecipient_1(typing.Generic[IRecipient_1_TMessage], typing.Protocol):
    @abc.abstractmethod
    def Receive(self, message: IRecipient_1_TMessage) -> None: ...


class MessageHandler_GenericClasses(abc.ABCMeta):
    Generic_MessageHandler_GenericClasses_MessageHandler_2_TRecipient = typing.TypeVar('Generic_MessageHandler_GenericClasses_MessageHandler_2_TRecipient')
    Generic_MessageHandler_GenericClasses_MessageHandler_2_TMessage = typing.TypeVar('Generic_MessageHandler_GenericClasses_MessageHandler_2_TMessage')
    def __getitem__(self, types : typing.Tuple[typing.Type[Generic_MessageHandler_GenericClasses_MessageHandler_2_TRecipient], typing.Type[Generic_MessageHandler_GenericClasses_MessageHandler_2_TMessage]]) -> typing.Type[MessageHandler_2[Generic_MessageHandler_GenericClasses_MessageHandler_2_TRecipient, Generic_MessageHandler_GenericClasses_MessageHandler_2_TMessage]]: ...

MessageHandler : MessageHandler_GenericClasses

MessageHandler_2_TRecipient = typing.TypeVar('MessageHandler_2_TRecipient', contravariant=True)
MessageHandler_2_TMessage = typing.TypeVar('MessageHandler_2_TMessage', contravariant=True)
class MessageHandler_2(typing.Generic[MessageHandler_2_TRecipient, MessageHandler_2_TMessage], MulticastDelegate):
    def __init__(self, object: typing.Any, method: int) -> None: ...
    @property
    def Method(self) -> MethodInfo: ...
    @property
    def Target(self) -> typing.Any: ...
    def BeginInvoke(self, recipient: MessageHandler_2_TRecipient, message: MessageHandler_2_TMessage, callback: AsyncCallback, object: typing.Any) -> IAsyncResult: ...
    def EndInvoke(self, result: IAsyncResult) -> None: ...
    def Invoke(self, recipient: MessageHandler_2_TRecipient, message: MessageHandler_2_TMessage) -> None: ...


class StrongReferenceMessenger(IMessenger):
    def __init__(self) -> None: ...
    @classmethod
    @property
    def Default(cls) -> StrongReferenceMessenger: ...
    def Reset(self) -> None: ...
    # Skipped IsRegistered due to it being static, abstract and generic.

    IsRegistered : IsRegistered_MethodGroup
    class IsRegistered_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[IsRegistered_2_T1], typing.Type[IsRegistered_2_T2]]) -> IsRegistered_2[IsRegistered_2_T1, IsRegistered_2_T2]: ...

        IsRegistered_2_T1 = typing.TypeVar('IsRegistered_2_T1')
        IsRegistered_2_T2 = typing.TypeVar('IsRegistered_2_T2')
        class IsRegistered_2(typing.Generic[IsRegistered_2_T1, IsRegistered_2_T2]):
            IsRegistered_2_TMessage = StrongReferenceMessenger.IsRegistered_MethodGroup.IsRegistered_2_T1
            IsRegistered_2_TToken = StrongReferenceMessenger.IsRegistered_MethodGroup.IsRegistered_2_T2
            def __call__(self, recipient: typing.Any, token: IsRegistered_2_TToken) -> bool:...


    # Skipped Register due to it being static, abstract and generic.

    Register : Register_MethodGroup
    class Register_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[Register_3_T1], typing.Type[Register_3_T2], typing.Type[Register_3_T3]]) -> Register_3[Register_3_T1, Register_3_T2, Register_3_T3]: ...

        Register_3_T1 = typing.TypeVar('Register_3_T1')
        Register_3_T2 = typing.TypeVar('Register_3_T2')
        Register_3_T3 = typing.TypeVar('Register_3_T3')
        class Register_3(typing.Generic[Register_3_T1, Register_3_T2, Register_3_T3]):
            Register_3_TRecipient = StrongReferenceMessenger.Register_MethodGroup.Register_3_T1
            Register_3_TMessage = StrongReferenceMessenger.Register_MethodGroup.Register_3_T2
            Register_3_TToken = StrongReferenceMessenger.Register_MethodGroup.Register_3_T3
            def __call__(self, recipient: Register_3_TRecipient, token: Register_3_TToken, handler: MessageHandler_2[Register_3_TRecipient, Register_3_TMessage]) -> None:...


    # Skipped Send due to it being static, abstract and generic.

    Send : Send_MethodGroup
    class Send_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[Send_2_T1], typing.Type[Send_2_T2]]) -> Send_2[Send_2_T1, Send_2_T2]: ...

        Send_2_T1 = typing.TypeVar('Send_2_T1')
        Send_2_T2 = typing.TypeVar('Send_2_T2')
        class Send_2(typing.Generic[Send_2_T1, Send_2_T2]):
            Send_2_TMessage = StrongReferenceMessenger.Send_MethodGroup.Send_2_T1
            Send_2_TToken = StrongReferenceMessenger.Send_MethodGroup.Send_2_T2
            def __call__(self, message: Send_2_TMessage, token: Send_2_TToken) -> Send_2_TMessage:...


    # Skipped Unregister due to it being static, abstract and generic.

    Unregister : Unregister_MethodGroup
    class Unregister_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[Unregister_2_T1], typing.Type[Unregister_2_T2]]) -> Unregister_2[Unregister_2_T1, Unregister_2_T2]: ...

        Unregister_2_T1 = typing.TypeVar('Unregister_2_T1')
        Unregister_2_T2 = typing.TypeVar('Unregister_2_T2')
        class Unregister_2(typing.Generic[Unregister_2_T1, Unregister_2_T2]):
            Unregister_2_TMessage = StrongReferenceMessenger.Unregister_MethodGroup.Unregister_2_T1
            Unregister_2_TToken = StrongReferenceMessenger.Unregister_MethodGroup.Unregister_2_T2
            def __call__(self, recipient: typing.Any, token: Unregister_2_TToken) -> None:...


    # Skipped UnregisterAll due to it being static, abstract and generic.

    UnregisterAll : UnregisterAll_MethodGroup
    class UnregisterAll_MethodGroup:
        def __getitem__(self, t:typing.Type[UnregisterAll_1_T1]) -> UnregisterAll_1[UnregisterAll_1_T1]: ...

        UnregisterAll_1_T1 = typing.TypeVar('UnregisterAll_1_T1')
        class UnregisterAll_1(typing.Generic[UnregisterAll_1_T1]):
            UnregisterAll_1_TToken = StrongReferenceMessenger.UnregisterAll_MethodGroup.UnregisterAll_1_T1
            def __call__(self, recipient: typing.Any, token: UnregisterAll_1_TToken) -> None:...

        def __call__(self, recipient: typing.Any) -> None:...



class WeakReferenceMessenger(IMessenger):
    def __init__(self) -> None: ...
    @classmethod
    @property
    def Default(cls) -> WeakReferenceMessenger: ...
    def Cleanup(self) -> None: ...
    def Reset(self) -> None: ...
    # Skipped IsRegistered due to it being static, abstract and generic.

    IsRegistered : IsRegistered_MethodGroup
    class IsRegistered_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[IsRegistered_2_T1], typing.Type[IsRegistered_2_T2]]) -> IsRegistered_2[IsRegistered_2_T1, IsRegistered_2_T2]: ...

        IsRegistered_2_T1 = typing.TypeVar('IsRegistered_2_T1')
        IsRegistered_2_T2 = typing.TypeVar('IsRegistered_2_T2')
        class IsRegistered_2(typing.Generic[IsRegistered_2_T1, IsRegistered_2_T2]):
            IsRegistered_2_TMessage = WeakReferenceMessenger.IsRegistered_MethodGroup.IsRegistered_2_T1
            IsRegistered_2_TToken = WeakReferenceMessenger.IsRegistered_MethodGroup.IsRegistered_2_T2
            def __call__(self, recipient: typing.Any, token: IsRegistered_2_TToken) -> bool:...


    # Skipped Register due to it being static, abstract and generic.

    Register : Register_MethodGroup
    class Register_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[Register_3_T1], typing.Type[Register_3_T2], typing.Type[Register_3_T3]]) -> Register_3[Register_3_T1, Register_3_T2, Register_3_T3]: ...

        Register_3_T1 = typing.TypeVar('Register_3_T1')
        Register_3_T2 = typing.TypeVar('Register_3_T2')
        Register_3_T3 = typing.TypeVar('Register_3_T3')
        class Register_3(typing.Generic[Register_3_T1, Register_3_T2, Register_3_T3]):
            Register_3_TRecipient = WeakReferenceMessenger.Register_MethodGroup.Register_3_T1
            Register_3_TMessage = WeakReferenceMessenger.Register_MethodGroup.Register_3_T2
            Register_3_TToken = WeakReferenceMessenger.Register_MethodGroup.Register_3_T3
            def __call__(self, recipient: Register_3_TRecipient, token: Register_3_TToken, handler: MessageHandler_2[Register_3_TRecipient, Register_3_TMessage]) -> None:...


    # Skipped Send due to it being static, abstract and generic.

    Send : Send_MethodGroup
    class Send_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[Send_2_T1], typing.Type[Send_2_T2]]) -> Send_2[Send_2_T1, Send_2_T2]: ...

        Send_2_T1 = typing.TypeVar('Send_2_T1')
        Send_2_T2 = typing.TypeVar('Send_2_T2')
        class Send_2(typing.Generic[Send_2_T1, Send_2_T2]):
            Send_2_TMessage = WeakReferenceMessenger.Send_MethodGroup.Send_2_T1
            Send_2_TToken = WeakReferenceMessenger.Send_MethodGroup.Send_2_T2
            def __call__(self, message: Send_2_TMessage, token: Send_2_TToken) -> Send_2_TMessage:...


    # Skipped Unregister due to it being static, abstract and generic.

    Unregister : Unregister_MethodGroup
    class Unregister_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[Unregister_2_T1], typing.Type[Unregister_2_T2]]) -> Unregister_2[Unregister_2_T1, Unregister_2_T2]: ...

        Unregister_2_T1 = typing.TypeVar('Unregister_2_T1')
        Unregister_2_T2 = typing.TypeVar('Unregister_2_T2')
        class Unregister_2(typing.Generic[Unregister_2_T1, Unregister_2_T2]):
            Unregister_2_TMessage = WeakReferenceMessenger.Unregister_MethodGroup.Unregister_2_T1
            Unregister_2_TToken = WeakReferenceMessenger.Unregister_MethodGroup.Unregister_2_T2
            def __call__(self, recipient: typing.Any, token: Unregister_2_TToken) -> None:...


    # Skipped UnregisterAll due to it being static, abstract and generic.

    UnregisterAll : UnregisterAll_MethodGroup
    class UnregisterAll_MethodGroup:
        def __getitem__(self, t:typing.Type[UnregisterAll_1_T1]) -> UnregisterAll_1[UnregisterAll_1_T1]: ...

        UnregisterAll_1_T1 = typing.TypeVar('UnregisterAll_1_T1')
        class UnregisterAll_1(typing.Generic[UnregisterAll_1_T1]):
            UnregisterAll_1_TToken = WeakReferenceMessenger.UnregisterAll_MethodGroup.UnregisterAll_1_T1
            def __call__(self, recipient: typing.Any, token: UnregisterAll_1_TToken) -> None:...

        def __call__(self, recipient: typing.Any) -> None:...


