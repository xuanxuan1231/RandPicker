"""
向系统发送通知
"""

from PySide6.QtGui import QIcon
from loguru import logger
from multipledispatch import dispatch

from ..config.dirs import ASSETS_DIR
from ..config.settings import SettingsConfig
from ..tray import RPTray


class NativeNotifier:
    _instance: "NativeNotifier" = None

    @classmethod
    def instance(cls) -> "NativeNotifier":
        return cls._instance

    def __init__(self):
        NativeNotifier._instance = self
        self.settingsConfig = SettingsConfig.instance()
        self.tray = RPTray.instance()

    @dispatch(str, list)
    def send_message(self, pick_type: str, stus: list) -> bool:
        """发送通知消息"""
        try:
            title, message = self._format_message(pick_type, stus)
            self._send(title, message)
            return True
        except Exception as e:
            logger.exception(f"Native 通知发送失败: {e}")
            return False

    @dispatch(str, str)
    def send_message(self, title: str, message: str) -> bool:
        """发送原始通知消息"""
        try:
            self._send(title, message)
            return True
        except Exception as e:
            logger.exception(f"Native 通知发送失败: {e}")
            return False

    def send_test(self) -> None:
        """发送测试通知"""
        try:
            title = "测试通知"
            message = "这是一条来自 RandPicker 的测试通知。"
            self._send(title, message)
        except Exception as e:
            logger.exception(f"Native 测试通知发送失败: {e}")

    def _format_message(self, pick_type: str, stus: list) -> tuple[str, str]:
        """格式化通知消息"""
        format = self.settingsConfig.getNotifyFormat("native")

        names = format['names']['separator'].join([s.get("name", "未知") for s in stus])
        count = len(stus)
        suffix = format['suffix']['person'] if pick_type == "person" else format['suffix']['group']

        title_template = format['title']
        body_template = format['body']

        title = title_template.replace("{count}", str(count)).replace("{suffix}", suffix).replace("{names}",
                                                                                                  names)
        body = body_template.replace("{count}", str(count)).replace("{suffix}", suffix).replace("{names}",
                                                                                                names)
        return title, body

    def _send(self, title: str, message: str) -> None:
        """发送系统通知"""
        try:
            self.tray.trayIcon.showMessage(
                title,
                message,
                QIcon(str(ASSETS_DIR / "icon-light.jpg")),
                5000,
            )

            logger.success(f"Native 通知发送成功: {title}: {message}")
        except Exception as e:
            logger.exception(f"Native 通知发送失败: {e}")
