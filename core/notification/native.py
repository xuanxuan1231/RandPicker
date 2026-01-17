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
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="RandPicker",
            )
            logger.success(f"Native 通知发送成功: {title}: {message}")
        except Exception as e:
            logger.error(f"Native 通知发送失败: {e}")
