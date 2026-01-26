import typing, clr, abc
from System import Array_1
from dotnetCampus.Ipc.Messages import IpcMessage

class IIpcObjectSerializer(typing.Protocol):
    @abc.abstractmethod
    def Serialize(self, value: typing.Any) -> Array_1[int]: ...
    # Skipped Deserialize due to it being static, abstract and generic.

    Deserialize : Deserialize_MethodGroup
    class Deserialize_MethodGroup:
        def __getitem__(self, t:typing.Type[Deserialize_1_T1]) -> Deserialize_1[Deserialize_1_T1]: ...

        Deserialize_1_T1 = typing.TypeVar('Deserialize_1_T1')
        class Deserialize_1(typing.Generic[Deserialize_1_T1]):
            Deserialize_1_T = IIpcObjectSerializer.Deserialize_MethodGroup.Deserialize_1_T1
            def __call__(self, data: Array_1[int]) -> Deserialize_1_T:...




class IpcObjectJsonSerializer(IIpcObjectSerializer):
    def __init__(self) -> None: ...
    def Serialize(self, value: typing.Any) -> Array_1[int]: ...
    # Skipped Deserialize due to it being static, abstract and generic.

    Deserialize : Deserialize_MethodGroup
    class Deserialize_MethodGroup:
        def __getitem__(self, t:typing.Type[Deserialize_1_T1]) -> Deserialize_1[Deserialize_1_T1]: ...

        Deserialize_1_T1 = typing.TypeVar('Deserialize_1_T1')
        class Deserialize_1(typing.Generic[Deserialize_1_T1]):
            Deserialize_1_T = IpcObjectJsonSerializer.Deserialize_MethodGroup.Deserialize_1_T1
            def __call__(self, byteList: Array_1[int]) -> Deserialize_1_T:...




class JsonIpcMessageSerializer(abc.ABC):
    @staticmethod
    def Serialize(tag: str, model: typing.Any) -> IpcMessage: ...
    # Skipped TryDeserialize due to it being static, abstract and generic.

    TryDeserialize : TryDeserialize_MethodGroup
    class TryDeserialize_MethodGroup:
        def __getitem__(self, t:typing.Type[TryDeserialize_1_T1]) -> TryDeserialize_1[TryDeserialize_1_T1]: ...

        TryDeserialize_1_T1 = typing.TypeVar('TryDeserialize_1_T1')
        class TryDeserialize_1(typing.Generic[TryDeserialize_1_T1]):
            TryDeserialize_1_T = JsonIpcMessageSerializer.TryDeserialize_MethodGroup.TryDeserialize_1_T1
            def __call__(self, message: IpcMessage, model: clr.Reference[TryDeserialize_1_T]) -> bool:...



