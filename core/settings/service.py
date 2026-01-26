"""
设置服务模块 - 获取但不需要配置
"""

from PySide6.QtCore import Slot, QObject, Signal
from loguru import logger

from ..integration.classisland import ciService


class SettingsService(QObject):
    connectivityUpdated = Signal(str, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        ciService.connectivityUpdated.connect(lambda x: self.updateConnectivityStatus("classisland", x))
        # cwService.connectivityUpdated.connect(lambda x: self.updateConnectivityStatus("classwidgets", x))
        # emit initial connectivity status so UI can render immediately
        self.updateConnectivityStatus("classisland", ciService.get_connectivity_status())

    @Slot(str, result=bool)
    def getNotifyAvailability(self, option: str) -> bool:
        """获取通知方式的可用性"""
        if option == "randpicker":
            return False
        elif option == "native":
            return True
        elif option == "classisland":
            return ciService.get_availability() or False
        elif option == "classwidgets":
            return False
        else:
            return False

    @Slot(str, result=bool)
    def getConnectivityStatus(self, option: str) -> bool:
        """获取通知方式的连接状态，供 QML 初始化状态"""
        if option == "classisland":
            return ciService.get_connectivity_status()
        elif option == "classwidgets":
            return False
        return False

    def updateConnectivityStatus(self, method: str, connectivity: bool):
        if method not in ["classisland", "classwidgets"]:
            return
        self.connectivityUpdated.emit(method, connectivity)
        logger.debug(f"触发通知方式 {method} 的连接状态更新: {connectivity}")
