import abc
from dotnetCampus.Ipc.IpcRouteds.DirectRouteds import JsonIpcDirectRoutedProvider
from dotnetCampus.Ipc.Pipes import PeerProxy, IpcProvider
from System.Threading.Tasks import Task

class IpcClient:
    def __init__(self) -> None: ...
    @property
    def JsonIpcProvider(self) -> JsonIpcDirectRoutedProvider: ...
    @property
    def PeerProxy(self) -> PeerProxy: ...
    @PeerProxy.setter
    def PeerProxy(self, value: PeerProxy) -> PeerProxy: ...
    @classmethod
    @property
    def PipeName(cls) -> str: ...
    @property
    def Provider(self) -> IpcProvider: ...
    def Connect(self) -> Task: ...


class IpcRoutedNotifyIds(abc.ABC):
    CurrentTimeStateChangedNotifyId : str
    OnAfterSchoolNotifyId : str
    OnBreakingTimeNotifyId : str
    OnClassNotifyId : str

