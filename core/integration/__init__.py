"""通知管理模块"""

from PySide6.QtCore import QObject
from loguru import logger

class NotificationManager(QObject):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    def send(self, option: str, title: str, message: str) -> None:
        """发送通知"""
        if option == "native":
            from core.integration.native import NativeNotifier
            notifier = NativeNotifier()
            notifier.send(title, message)
        elif option == "classisland":
            logger.error(f"不支持的通知方式: {option}")
            return
            from core.integration.classisland import ClassIslandNotifier
            ciIntegration.send_message(title, message)
        elif option == "classwidgets":
            logger.error(f"不支持的通知方式: {option}")
            return
            from core.integration.classwidgets import ClassWidgetsNotifier
            notifier = ClassWidgetsNotifier(self.parent)
            notifier.send(title, message)
        else:
            logger.error(f"不支持的通知方式: {option}")