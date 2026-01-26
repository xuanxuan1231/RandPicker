import typing, clr, abc
from dotnetCampus.Ipc import IIpcProvider, IPeerProxy, IIpcRequestHandler
from dotnetCampus.Ipc.Context import IIpcRequestContext
from System.Threading.Tasks import Task_1
from dotnetCampus.Ipc.Messages import IIpcResponseMessage

class Garm_GenericClasses(abc.ABCMeta):
    Generic_Garm_GenericClasses_Garm_1_T = typing.TypeVar('Generic_Garm_GenericClasses_Garm_1_T')
    def __getitem__(self, types : typing.Type[Generic_Garm_GenericClasses_Garm_1_T]) -> typing.Type[Garm_1[Generic_Garm_GenericClasses_Garm_1_T]]: ...

Garm : Garm_GenericClasses

Garm_1_T = typing.TypeVar('Garm_1_T')
class Garm_1(typing.Generic[Garm_1_T], IGarmObject):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, value: Garm_1_T) -> None: ...
    @typing.overload
    def __init__(self, value: Garm_1_T, ipcType: typing.Type[typing.Any]) -> None: ...
    @property
    def Value(self) -> Garm_1_T: ...
    # Operator not supported op_Implicit(value: T)


class GeneratedIpcFactory(abc.ABC):
    # Skipped CreateIpcJoint due to it being static, abstract and generic.

    CreateIpcJoint : CreateIpcJoint_MethodGroup
    class CreateIpcJoint_MethodGroup:
        def __getitem__(self, t:typing.Type[CreateIpcJoint_1_T1]) -> CreateIpcJoint_1[CreateIpcJoint_1_T1]: ...

        CreateIpcJoint_1_T1 = typing.TypeVar('CreateIpcJoint_1_T1')
        class CreateIpcJoint_1(typing.Generic[CreateIpcJoint_1_T1]):
            CreateIpcJoint_1_TContract = GeneratedIpcFactory.CreateIpcJoint_MethodGroup.CreateIpcJoint_1_T1
            def __call__(self, ipcProvider: IIpcProvider, realInstance: CreateIpcJoint_1_TContract, ipcObjectId: str = ...) -> CreateIpcJoint_1_TContract:...


    # Skipped CreateIpcProxy due to it being static, abstract and generic.

    CreateIpcProxy : CreateIpcProxy_MethodGroup
    class CreateIpcProxy_MethodGroup:
        @typing.overload
        def __getitem__(self, t:typing.Type[CreateIpcProxy_1_T1]) -> CreateIpcProxy_1[CreateIpcProxy_1_T1]: ...

        CreateIpcProxy_1_T1 = typing.TypeVar('CreateIpcProxy_1_T1')
        class CreateIpcProxy_1(typing.Generic[CreateIpcProxy_1_T1]):
            CreateIpcProxy_1_TContract = GeneratedIpcFactory.CreateIpcProxy_MethodGroup.CreateIpcProxy_1_T1
            @typing.overload
            def __call__(self, ipcProvider: IIpcProvider, peer: IPeerProxy, ipcObjectId: str = ...) -> CreateIpcProxy_1_TContract:...
            @typing.overload
            def __call__(self, ipcProvider: IIpcProvider, peer: IPeerProxy, ipcProxyConfigs: IpcProxyConfigs, ipcObjectId: str = ...) -> CreateIpcProxy_1_TContract:...

        @typing.overload
        def __getitem__(self, t:typing.Tuple[typing.Type[CreateIpcProxy_2_T1], typing.Type[CreateIpcProxy_2_T2]]) -> CreateIpcProxy_2[CreateIpcProxy_2_T1, CreateIpcProxy_2_T2]: ...

        CreateIpcProxy_2_T1 = typing.TypeVar('CreateIpcProxy_2_T1')
        CreateIpcProxy_2_T2 = typing.TypeVar('CreateIpcProxy_2_T2')
        class CreateIpcProxy_2(typing.Generic[CreateIpcProxy_2_T1, CreateIpcProxy_2_T2]):
            CreateIpcProxy_2_TContract = GeneratedIpcFactory.CreateIpcProxy_MethodGroup.CreateIpcProxy_2_T1
            CreateIpcProxy_2_TShape = GeneratedIpcFactory.CreateIpcProxy_MethodGroup.CreateIpcProxy_2_T2
            def __call__(self, ipcProvider: IIpcProvider, peer: IPeerProxy, ipcObjectId: str = ...) -> CreateIpcProxy_2_TContract:...




class GeneratedIpcJoint_GenericClasses(abc.ABCMeta):
    Generic_GeneratedIpcJoint_GenericClasses_GeneratedIpcJoint_1_TContract = typing.TypeVar('Generic_GeneratedIpcJoint_GenericClasses_GeneratedIpcJoint_1_TContract')
    def __getitem__(self, types : typing.Type[Generic_GeneratedIpcJoint_GenericClasses_GeneratedIpcJoint_1_TContract]) -> typing.Type[GeneratedIpcJoint_1[Generic_GeneratedIpcJoint_GenericClasses_GeneratedIpcJoint_1_TContract]]: ...

class GeneratedIpcJoint(GeneratedIpcJoint_0, metaclass =GeneratedIpcJoint_GenericClasses): ...

class GeneratedIpcJoint_0(abc.ABC):
    pass


GeneratedIpcJoint_1_TContract = typing.TypeVar('GeneratedIpcJoint_1_TContract')
class GeneratedIpcJoint_1(typing.Generic[GeneratedIpcJoint_1_TContract], GeneratedIpcJoint_0):
    pass


class GeneratedIpcProxy_GenericClasses(abc.ABCMeta):
    Generic_GeneratedIpcProxy_GenericClasses_GeneratedIpcProxy_1_TContract = typing.TypeVar('Generic_GeneratedIpcProxy_GenericClasses_GeneratedIpcProxy_1_TContract')
    def __getitem__(self, types : typing.Type[Generic_GeneratedIpcProxy_GenericClasses_GeneratedIpcProxy_1_TContract]) -> typing.Type[GeneratedIpcProxy_1[Generic_GeneratedIpcProxy_GenericClasses_GeneratedIpcProxy_1_TContract]]: ...

class GeneratedIpcProxy(GeneratedIpcProxy_0, metaclass =GeneratedIpcProxy_GenericClasses): ...

class GeneratedIpcProxy_0(abc.ABC):
    @property
    def Context(self) -> GeneratedProxyJointIpcContext: ...
    @Context.setter
    def Context(self, value: GeneratedProxyJointIpcContext) -> GeneratedProxyJointIpcContext: ...
    @property
    def ObjectId(self) -> str: ...
    @ObjectId.setter
    def ObjectId(self, value: str) -> str: ...
    @property
    def PeerProxy(self) -> IPeerProxy: ...
    @PeerProxy.setter
    def PeerProxy(self, value: IPeerProxy) -> IPeerProxy: ...
    @property
    def TypeName(self) -> str: ...
    @TypeName.setter
    def TypeName(self, value: str) -> str: ...


GeneratedIpcProxy_1_TContract = typing.TypeVar('GeneratedIpcProxy_1_TContract')
class GeneratedIpcProxy_1(typing.Generic[GeneratedIpcProxy_1_TContract], GeneratedIpcProxy_0):
    @property
    def Context(self) -> GeneratedProxyJointIpcContext: ...
    @Context.setter
    def Context(self, value: GeneratedProxyJointIpcContext) -> GeneratedProxyJointIpcContext: ...
    @property
    def ObjectId(self) -> str: ...
    @ObjectId.setter
    def ObjectId(self, value: str) -> str: ...
    @property
    def PeerProxy(self) -> IPeerProxy: ...
    @PeerProxy.setter
    def PeerProxy(self, value: IPeerProxy) -> IPeerProxy: ...
    @property
    def TypeName(self) -> str: ...
    @TypeName.setter
    def TypeName(self, value: str) -> str: ...


class GeneratedProxyJointIpcContext:
    @property
    def RequestHandler(self) -> IIpcRequestHandler: ...


class IGarmObject(typing.Protocol):
    @property
    def IpcType(self) -> typing.Type[typing.Any]: ...
    @property
    def Value(self) -> typing.Any: ...
    @property
    def ValueType(self) -> typing.Type[typing.Any]: ...


class IpcProxyConfigs:
    def __init__(self) -> None: ...
    @property
    def IgnoresIpcException(self) -> bool: ...
    @IgnoresIpcException.setter
    def IgnoresIpcException(self, value: bool) -> bool: ...
    @property
    def Timeout(self) -> int: ...
    @Timeout.setter
    def Timeout(self, value: int) -> int: ...


class PublicIpcJointManager:
    def TryJoint(self, request: IIpcRequestContext, responseTask: clr.Reference[Task_1[IIpcResponseMessage]]) -> bool: ...
    # Skipped AddPublicIpcObject due to it being static, abstract and generic.

    AddPublicIpcObject : AddPublicIpcObject_MethodGroup
    class AddPublicIpcObject_MethodGroup:
        def __getitem__(self, t:typing.Type[AddPublicIpcObject_1_T1]) -> AddPublicIpcObject_1[AddPublicIpcObject_1_T1]: ...

        AddPublicIpcObject_1_T1 = typing.TypeVar('AddPublicIpcObject_1_T1')
        class AddPublicIpcObject_1(typing.Generic[AddPublicIpcObject_1_T1]):
            AddPublicIpcObject_1_TContract = PublicIpcJointManager.AddPublicIpcObject_MethodGroup.AddPublicIpcObject_1_T1
            def __call__(self, joint: GeneratedIpcJoint_1[AddPublicIpcObject_1_TContract], ipcObjectId: str = ...) -> None:...

        def __call__(self, contractType: typing.Type[typing.Any], joint: GeneratedIpcJoint, ipcObjectId: str = ...) -> None:...


