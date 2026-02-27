"""通知管理模块"""
from typing import Optional

from PySide6.QtCore import QObject, Slot
from loguru import logger

from ..config.settings import SettingsConfig
from .classisland import ClassIslandIntegration
from .native import NativeNotifier


class NotificationManager(QObject):
    _instance: "NotificationManager" = None

    @classmethod
    def instance(cls) -> "NotificationManager":
        return cls._instance

    def __init__(self, parent=None):
        super().__init__()
        NotificationManager._instance = self
        self.settingsConfig = SettingsConfig.instance()
        self.nativeNotifier = NativeNotifier()
        self.ciService = ClassIslandIntegration()
        try:
            self.ciService.start()
        except Exception as e:
            logger.exception(f"初始化 ClassIsland 集成服务时出错: {e}")

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
                nativeSent = self.nativeNotifier.send_message(pick_type, stus)
                sent = sent or nativeSent
            elif option == "classisland":
                ciSent = self.ciService.send_message(pick_type, stus)
                sent = sent or ciSent
            elif option == "classwidgets":
                logger.error(f"不支持的通知方式: {option}")
            else:
                logger.error(f"不支持的通知方式: {option}")

        # 发送失败，则使用备选通知
        if not sent and self.settingsConfig.getNotifyFallback():
            try:
                self.nativeNotifier.send_message(pick_type, stus)
            except Exception:
                logger.exception("Native 回退通知发送失败")

    def send_raw(self, title: str, message: str, option: Optional[str] = None) -> None:
        """发送原始通知"""
        if option is None:
            options = self.settingsConfig.getAllEnabledNotifyOptions()
        else:
            options = [option]

        for opt in options:
            if opt == "native":
                self.nativeNotifier.send(title, message)
            elif opt == "classisland":
                self.ciService.send_raw(title, message)
            elif opt == "classwidgets":
                logger.error(f"不支持的通知方式: {opt}")
            else:
                logger.error(f"不支持的通知方式: {opt}")

    @Slot(str)
    def sendTest(self, option):
        match option:
            case "native":
                self.nativeNotifier.send_test()
            case "classisland":
                self.ciService.send_test()
            case "classwidgets":
                logger.error(f"不支持的通知方式: {option}")
            case _:
                logger.error(f"不支持的通知方式: {option}")
