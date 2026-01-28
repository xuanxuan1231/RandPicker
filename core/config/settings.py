"""
TODO)) 管理“设置”中的配置
"""

from pathlib import Path

from PySide6.QtCore import QObject, Slot
from RinUI import ConfigManager
from loguru import logger

from .dirs import CONFIG_DIR

DEFAULT_CONFIG = {
    "notification": {
        "fallback": True,
        "options": {
            "native": {
                "enabled": True
            },
            "classisland": {
                "enabled": False,
                "mask_duration": 0,
                "overlay_duration": 0,
                "overlay_type": 0 # 0: simple, 1: rolling, 2: auto
            },
            "randpicker": {
                "enabled": False
            },
            "classwidgets": {
                "enabled": False
            }
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
        data = options.get(option, {})
        return data.get("enabled", False)

    @Slot(str, bool)
    def setNotifyOptionStatus(self, option: str, status: bool) -> None:
        """设置通知方式状态"""
        notification = self.config.setdefault("notification", {})
        options = notification.setdefault("options", {})
        options[option]["enabled"] = status
        self.save_config()

    def getAllEnabledNotifyOptions(self) -> list:
        """获取所有启用的通知方式"""
        notification = self.config.get("notification", {})
        options = notification.get("options", {})
        result = []
        for opt, data in options.items():
            if data.get("enabled", False):
                result.append(opt)
        logger.info(f"当前启用的通知方式: {result}")
        return result

    @Slot(result=int)
    def getCiMaskDuration(self) -> int:
        """获取 ClassIsland 通知遮罩持续时间"""
        notification = self.config.get("notification", {})
        options = notification.get("options", {})
        ci_options = options.get("classisland", {})
        return ci_options.get("mask_duration", 0)

    @Slot(int)
    def setCiMaskDuration(self, duration: int):
        """设置 ClassIsland 通知遮罩持续时间"""
        notification = self.config.setdefault("notification", {})
        options = notification.setdefault("options", {})
        ci_options = options.setdefault("classisland", {})
        ci_options["mask_duration"] = duration
        self.save_config()

    @Slot(result=int)
    def getCiOverlayDuration(self) -> int:
        """获取 ClassIsland 通知正文持续时间"""
        notification = self.config.get("notification", {})
        options = notification.get("options", {})
        ci_options = options.get("classisland", {})
        return ci_options.get("overlay_duration", 0)

    @Slot(int)
    def setCiOverlayDuration(self, duration: int):
        """设置 ClassIsland 通知正文持续时间"""
        notification = self.config.setdefault("notification", {})
        options = notification.setdefault("options", {})
        ci_options = options.setdefault("classisland", {})
        ci_options["overlay_duration"] = duration
        self.save_config()

    # 仅供后端使用
    def getCiOverlayType(self) -> str:
        """获取 ClassIsland 通知正文类型"""
        notification = self.config.get("notification", {})
        options = notification.get("options", {})
        ci_options = options.get("classisland", {})
        overlay_type = ci_options.get("overlay_type", 0)
        match overlay_type:
            case 0:
                return "simple"
            case 1:
                return "rolling"
            case 2:
                return "auto"
            case _:
                return "simple"

    # 仅供前端使用
    @Slot(result=int)
    def getCiOverlayTypeIndex(self) -> int:
        """获取 ClassIsland 通知正文类型索引"""
        notification = self.config.get("notification", {})
        options = notification.get("options", {})
        ci_options = options.get("classisland", {})
        return ci_options.get("overlay_type", 0)

    @Slot(str)
    def setCiOverlayType(self, overlay_type: str):
        """设置 ClassIsland 通知正文类型"""
        notification = self.config.setdefault("notification", {})
        options = notification.setdefault("options", {})
        ci_options = options.setdefault("classisland", {})
        match overlay_type:
            case "simple":
                ci_options["overlay_type"] = 0
            case "rolling":
                ci_options["overlay_type"] = 1
            case "auto":
                ci_options["overlay_type"] = 2
            case _:
                ci_options["overlay_type"] = 0
        self.save_config()

    # endregion #
