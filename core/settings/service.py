"""
设置服务模块 - 获取但不需要配置
"""
import platform

from PySide6.QtCore import Slot, QObject, Signal
from loguru import logger

from ..integration.classisland import ciService


class SettingsService(QObject):
    connectivityUpdated = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        ciService.connectivityUpdated.connect(lambda x: self.updateConnectivityStatus("classisland", x))
        # cwService.connectivityUpdated.connect(lambda x: self.updateConnectivityStatus("classwidgets", x))

    @Slot(str, result=bool)
    def getNotifyAvailability(self, option: str) -> bool:
        """获取通知方式的可用性"""
        match option:
            case "randpicker":
                return False
            case "native":
                return True
            case "classisland":
                return True
            case "classwidgets":
                return False
            case _:
                return False

    @Slot(str, result=str)
    def getConnectivityStatus(self, option: str) -> str:
        """获取通知方式的连接状态，供 QML 初始化状态"""
        match option:
            case "classisland": return ciService.get_connectivity_status()
            case "classwidgets": return "NotAvailable"
            case _: return "NotAvailable"

    def updateConnectivityStatus(self, method: str, connectivity: str) -> None:
        if method not in ["classisland", "classwidgets"]:
            return
        self.connectivityUpdated.emit(method, connectivity)
        logger.debug(f"触发通知方式 {method} 的连接状态更新: {connectivity}")

    @Slot(result=str)
    def getDotNetDownloadLink(self):
        match platform.system():
            case "win32" : running_os = "windows"
            case "linux" :
                return "https://learn.microsoft.com/dotnet/core/install/linux?WT.mc_id=dotnet-35129-website"
            case "darwin": running_os = "macos"
            case _:
                return "https://dotnet.microsoft.com/en-us/download/dotnet/scripts"

        match platform.machine().lower():
            case "amd64" | "x86_64"  : arch = "x64"
            case "arm64" | "aarch64" : arch = "arm64"
            case _:
                return "https://dotnet.microsoft.com/en-us/download/dotnet/scripts"

        return f"https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-8.0.23-{running_os}-{arch}-installer"
