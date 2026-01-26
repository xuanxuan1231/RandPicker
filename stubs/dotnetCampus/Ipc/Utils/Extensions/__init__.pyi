import typing, clr, abc
from dotnetCampus.Ipc.Messages import IpcMessage
from System import Array_1
from dotnetCampus.Ipc.Context import IPeerMessageArgs

class PeerMessageArgsExtension(abc.ABC):
    # Skipped TryGetPayload due to it being static, abstract and generic.

    TryGetPayload : TryGetPayload_MethodGroup
    class TryGetPayload_MethodGroup:
        @typing.overload
        def __call__(self, ipcMessage: clr.Reference[IpcMessage], requiredHeader: int, subMessage: clr.Reference[IpcMessage]) -> bool:...
        @typing.overload
        def __call__(self, ipcMessage: clr.Reference[IpcMessage], requiredHeader: Array_1[int], subMessage: clr.Reference[IpcMessage]) -> bool:...
        @typing.overload
        def __call__(self, args: IPeerMessageArgs, requiredHeader: int, subMessage: clr.Reference[IpcMessage]) -> bool:...


