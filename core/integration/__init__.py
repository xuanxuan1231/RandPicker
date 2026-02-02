"""通知管理模块"""

from PySide6.QtCore import QObject, Slot
from loguru import logger

from core.integration.classisland import ciService
from core.integration.native import nativeNotifier


class NotificationManager(QObject):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.settingsConfig = parent.settingsConfig

        # 因为相关 service 在它自己那实例化了，就在这重新加一下 rpmain 相关的属性
        ciService.main = parent
        ciService.settingsConfig = self.settingsConfig
        nativeNotifier.main = parent
        nativeNotifier.settingsConfig = self.settingsConfig

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
                nativeSent = nativeNotifier.send_message(pick_type, stus)
                sent = sent or nativeSent
            elif option == "classisland":
                ciSent = ciService.send_message(pick_type, stus)
                sent = sent or ciSent
            elif option == "classwidgets":
                logger.error(f"不支持的通知方式: {option}")
            else:
                logger.error(f"不支持的通知方式: {option}")

        # 发送失败，则使用备选通知
        if not sent and self.settingsConfig.getNotifyFallback():
            try:
                nativeNotifier.send_message(pick_type, stus)
            except Exception:
                logger.exception("Native 回退通知发送失败")

    @Slot(str)
    def sendTest(self, option):
        match option:
            case "native":
                nativeNotifier.send_test()
            case "classisland":
                ciService.send_test()
            case "classwidgets":
                logger.error(f"不支持的通知方式: {option}")
            case _:
                logger.error(f"不支持的通知方式: {option}")
