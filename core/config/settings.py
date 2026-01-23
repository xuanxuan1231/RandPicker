"""
TODO)) 管理“设置”中的配置
"""

from PySide6.QtCore import QObject, Slot
from RinUI import ConfigManager
from pathlib import Path
from .dirs import CONFIG_DIR

DEFAULT_CONFIG = {
    "notification": {
        "fallback": True,
        "options": {
            "native": True,
            "classisland": False,
            "RandPicker": False,
            "classwidgets": False,
        },
    }
}

class SettingsConfig(ConfigManager, QObject):
    def __init__(self, parent=None):
        self.parent = parent

        ConfigManager.__init__(self, ".", Path(CONFIG_DIR) / "settings.json")
        QObject.__init__(self)

        self.load_config(DEFAULT_CONFIG)

    # region 通知 #
    @Slot(result=bool)
    def getNotifyFallback(self) -> bool:
        """获取通知回退选项"""
        notification = self.config.get("notification", {})
        return notification.get("fallback", True)

    @Slot(bool)
    def setNotifyFallback(self, value: bool) -> None:
        """设置通知回退选项"""
        notification = self.config.setdefault("notification", {})
        notification["fallback"] = value
        self.save_config()

    @Slot(str, result=bool)
    def getNotifyOptionStatus(self, option: str) -> bool:
        """获取通知方式状态"""
        notification = self.config.get("notification", {})
        options = notification.get("options", {})
        return options.get(option, False)

    @Slot(str, bool)
    def setNotifyOptionStatus(self, option: str, status: bool) -> None:
        """设置通知方式状态"""
        notification = self.config.setdefault("notification", {})
        options = notification.setdefault("options", {})
        options[option] = status
        self.save_config()

    # endregion #