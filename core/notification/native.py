"""
向系统发送通知
"""

from loguru import logger
from plyer import notification

class NativeNotifier:
    def __init__(self):
        pass

    def send(self, title: str, message: str) -> None:
        """发送系统通知"""
        notification.notify(
            title=title,
            message=message,
            app_name="RandPicker",
        )
        print(f"Notification - {title}: {message}")