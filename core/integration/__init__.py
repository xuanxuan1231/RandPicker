"""通知管理模块"""

from PySide6.QtCore import QObject
from loguru import logger

from core.integration.classisland import ciService
from core.integration.native import nativeNotifier


class NotificationManager(QObject):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.settingsConfig = parent.settingsConfig

    def send(self, pick_type: str, stus: list) -> None:
        """发送通知"""
        options = self.settingsConfig.getAllEnabledNotifyOptions()
        if not options:
            return
        if pick_type not in ["person", "group"]:
            logger.error(f"不支持的抽选类型: {pick_type}")
            return

        sent = False

        for option in options:
            if option == "native":
                try:
                    nativeNotifier.send_message(pick_type, stus)
                    sent = True
                except Exception:
                    logger.exception("Native 通知发送失败")
            elif option == "classisland":
                sent = ciService.send_message(pick_type, stus)
            elif option == "classwidgets":
                logger.error(f"不支持的通知方式: {option}")
            else:
                logger.error(f"不支持的通知方式: {option}")

        if not sent:
            try:
                title = f"抽选了 {len(stus)}" + ("名学生" if pick_type == "person" else "个小组")
                message = ", ".join(stus)
                from core.integration.native import NativeNotifier
                notifier = NativeNotifier()
                notifier.send(title, message)
            except Exception:
                logger.exception("Native 兜底通知发送失败")
