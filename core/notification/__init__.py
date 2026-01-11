"""通知管理模块"""

from PySide6.QtCore import QObject

class NotificationManager(QObject):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    def send(self, option: str, title: str, message: str) -> None:
        """发送通知"""
        if option == "native":
            from core.notification.native import NativeNotifier
            notifier = NativeNotifier()
            notifier.send(title, message)
        else:
            print(f"Unsupported notification option: {option}")