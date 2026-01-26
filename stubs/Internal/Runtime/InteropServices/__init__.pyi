import typing, clr, abc
from System import Guid, MulticastDelegate, IAsyncResult, AsyncCallback
from System.Reflection import MethodInfo

class ComActivationContext:
    AssemblyName : str
    AssemblyPath : str
    ClassId : Guid
    InterfaceId : Guid
    TypeName : str
    @staticmethod
    def Create(cxtInt: clr.Reference[ComActivationContextInternal]) -> ComActivationContext: ...


class ComActivationContextInternal:
    AssemblyNameBuffer : clr.Reference[str]
    AssemblyPathBuffer : clr.Reference[str]
    ClassFactoryDest : int
    ClassId : Guid
    InterfaceId : Guid
    TypeNameBuffer : clr.Reference[str]


class ComActivator(abc.ABC):
    @staticmethod
    def ClassRegistrationScenarioForType(cxt: ComActivationContext, register: bool) -> None: ...
    @staticmethod
    def GetClassFactoryForType(cxt: ComActivationContext) -> typing.Any: ...
    @staticmethod
    def GetClassFactoryForTypeInternal(pCxtInt: clr.Reference[ComActivationContextInternal]) -> int: ...
    @staticmethod
    def RegisterClassForTypeInternal(pCxtInt: clr.Reference[ComActivationContextInternal]) -> int: ...
    @staticmethod
    def UnregisterClassForTypeInternal(pCxtInt: clr.Reference[ComActivationContextInternal]) -> int: ...


class ComponentActivator(abc.ABC):
    @staticmethod
    def GetFunctionPointer(typeNameNative: int, methodNameNative: int, delegateTypeNative: int, loadContext: int, reserved: int, functionHandle: int) -> int: ...
    @staticmethod
    def LoadAssemblyAndGetFunctionPointer(assemblyPathNative: int, typeNameNative: int, methodNameNative: int, delegateTypeNative: int, reserved: int, functionHandle: int) -> int: ...

    class ComponentEntryPoint(MulticastDelegate):
        def __init__(self, object: typing.Any, method: int) -> None: ...
        @property
        def Method(self) -> MethodInfo: ...
        @property
        def Target(self) -> typing.Any: ...
        def BeginInvoke(self, args: int, sizeBytes: int, callback: AsyncCallback, object: typing.Any) -> IAsyncResult: ...
        def EndInvoke(self, result: IAsyncResult) -> int: ...
        def Invoke(self, args: int, sizeBytes: int) -> int: ...



class IClassFactory(typing.Protocol):
    @abc.abstractmethod
    def CreateInstance(self, pUnkOuter: typing.Any, riid: clr.Reference[Guid], ppvObject: clr.Reference[int]) -> None: ...
    @abc.abstractmethod
    def LockServer(self, fLock: bool) -> None: ...


class InMemoryAssemblyLoader(abc.ABC):
    @staticmethod
    def LoadInMemoryAssembly(moduleHandle: int, assemblyPath: int) -> None: ...

