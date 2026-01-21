"""
设置服务模块 - 获取但不需要配置
"""

from PySide6.QtCore import Slot, QObject

from ..integration.classisland import ciService

class SettingsService(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(str, result=bool)
    def getNotifyAvailability(self, option: str) -> bool:
        """获取通知方式的可用性"""
        if option == "RandPicker":
            return False
        elif option == "native":
            return True
        elif option == "classisland":
            return ciService.get_availability() or False
        elif option == "classwidgets":
            return False
        else:
            return False