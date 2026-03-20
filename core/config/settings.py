"""
管理“设置”中的配置
"""

from pathlib import Path

from PySide6.QtCore import QObject, Slot, Signal, Property
from RinUI import ConfigManager
from loguru import logger

from .dirs import CONFIG_DIR

DEFAULT_CONFIG = {
    "appear_behave": {
        "general": {
            "run_as_admin": False
        },
        "widget": {
            "person_button": True,
            "group_button": True,
            "more_button": True,
            "memory_row": True
        }
    },
    "notification": {
        "fallback": True,
        "options": {
            "native": {
                "enabled": True,
                "format": {
                    "title": "抽选了 {count} {suffix}",
                    "body": "{names}",
                    "names": {
                        "separator": ",",
                    },
                    "suffix": {
                        "person": "位同学",
                        "group": "个小组"
                    }
                }
            },
            "classisland": {
                "enabled": False,
                "mask_duration": 0,
                "overlay_duration": 0,
                "overlay_type": 2,  # 0: simple, 1: rolling, 2: auto
                "format": {
                    "title": "抽选了 {count} {suffix}",
                    "body": "{names}",
                    "names": {
                        "separator": ",",
                    },
                    "suffix": {
                        "person": "位同学",
                        "group": "个小组"
                    }
                }
            },
            "randpicker": {
                "enabled": False
            },
            "classwidgets": {
                "enabled": False
            }
        }
    },
    "widget_position": {
        "x": None,
        "y": None
    },
    "advanced": {
        "uiaccess": False
    }
}



class SettingsConfig(ConfigManager, QObject):
    _instance: "SettingsConfig" = None

    showDrawButtonChanged = Signal()
    showGroupButtonChanged = Signal()
    showMoreButtonChanged = Signal()
    showMemoryRowChanged = Signal()

    @classmethod
    def instance(cls) -> "SettingsConfig":
        return cls._instance

    def __init__(self, parent=None):
        SettingsConfig._instance = self

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

    @Slot(str, result=dict)
    def getNotifyFormat(self, option: str) -> dict:
        """获取通知方式的格式化内容。
        """
        notification = self.config.get("notification", {})
        options = notification.get("options", {})
        data = options.get(option, {})
        format_data = data.get("format", {})
        if not isinstance(format_data, dict):
            format_data = {}

        title = format_data.get("title", "抽选了 {count} {suffix}")
        body = format_data.get("body", "{names}")

        names = format_data.get("names", {})
        if not isinstance(names, dict):
            names = {}
        separator = names.get("separator", ",")

        suffix = format_data.get("suffix", {})
        if not isinstance(suffix, dict):
            suffix = {}
        person_suffix = suffix.get("person", "位同学")
        group_suffix = suffix.get("group", "个小组")

        return {
            "title": title,
            "body": body,
            "names": {
                "separator": separator,
            },
            "suffix": {
                "person": person_suffix,
                "group": group_suffix,
            },
        }

    @Slot(str, dict)
    def setNotifyFormat(self, option: str, format_data: dict) -> None:
        """设置通知方式的格式化内容"""
        notification = self.config.setdefault("notification", {})
        options = notification.setdefault("options", {})
        data = options.setdefault(option, {})
        data["format"] = format_data
        self.save_config()

    # endregion #

    # region 窗口位置 #
    @Slot(result="QVariantList")
    def getWidgetPosition(self) -> list[int | None]:
        """获取主窗口位置"""
        widget_position = self.config.get("widget_position", {})
        x = widget_position.get("x", None)
        y = widget_position.get("y", None)
        return [x, y]

    @Slot(int, int)
    def setWidgetPosition(self, x: int, y: int) -> None:
        """设置主窗口位置"""
        self.config.setdefault("widget_position", {})
        self.config["widget_position"]["x"] = x
        self.config["widget_position"]["y"] = y
        self.save_config()

    # endregion #

    # region UIACCESS #
    def getUIAccessEnabled(self) -> bool:
        """获取 UIAccess 启用状态"""
        advanced = self.config.get("advanced", {})
        return bool(advanced.get("uiaccess", False))

    @Slot(bool)
    def setUIAccessEnabled(self, enabled: bool) -> None:
        """设置 UIAccess 启用状态"""
        advanced = self.config.setdefault("advanced", {})
        advanced["uiaccess"] = enabled
        self.save_config()
    # endregion #

    # region 外观 & 行为 #
    @Slot(result=bool)
    def getRunAsAdmin(self) -> bool:
        """获取是否以管理员权限运行"""
        appear_behave = self.config.get("appear_behave", {})
        general = appear_behave.get("general", {})
        return bool(general.get("run_as_admin", False))

    @Slot(bool)
    def setRunAsAdmin(self, run_as_admin: bool) -> None:
        """设置是否以管理员权限运行"""
        appear_behave = self.config.setdefault("appear_behave", {})
        general = appear_behave.setdefault("general", {})
        general["run_as_admin"] = run_as_admin
        self.save_config()

    @Property(bool, notify=showDrawButtonChanged)
    def showDrawButton(self):
        appear_behave = self.config.get("appear_behave", {})
        widget = appear_behave.get("widget", {})
        return bool(widget.get("person_button", True))

    @Property(bool, notify=showGroupButtonChanged)
    def showGroupButton(self):
        appear_behave = self.config.get("appear_behave", {})
        widget = appear_behave.get("widget", {})
        return bool(widget.get("group_button", True))

    @Property(bool, notify=showMoreButtonChanged)
    def showMoreButton(self):
        appear_behave = self.config.get("appear_behave", {})
        widget = appear_behave.get("widget", {})
        return bool(widget.get("more_button", True))

    @Property(bool, notify=showMemoryRowChanged)
    def showMemoryRow(self):
        appear_behave = self.config.get("appear_behave", {})
        widget = appear_behave.get("widget", {})
        return bool(widget.get("memory_row", True))

    @Slot(bool)
    def setShowDrawButton(self, show: bool) -> None:
        """设置是否显示抽选按钮"""
        appear_behave = self.config.setdefault("appear_behave", {})
        widget = appear_behave.setdefault("widget", {})
        widget["person_button"] = show
        self.save_config()
        self.showDrawButtonChanged.emit()

    @Slot(bool)
    def setShowGroupButton(self, show: bool) -> None:
        """设置是否显示抽选小组按钮"""
        appear_behave = self.config.setdefault("appear_behave", {})
        widget = appear_behave.setdefault("widget", {})
        widget["group_button"] = show
        self.save_config()
        self.showGroupButtonChanged.emit()

    @Slot(bool)
    def setShowMoreButton(self, show: bool) -> None:
        """设置是否显示更多按钮"""
        appear_behave = self.config.setdefault("appear_behave", {})
        widget = appear_behave.setdefault("widget", {})
        widget["more_button"] = show
        self.save_config()
        self.showMoreButtonChanged.emit()

    @Slot(bool)
    def setShowMemoryRow(self, show: bool) -> None:
        """设置是否显示记忆行（记忆 Toggle + 重置）"""
        appear_behave = self.config.setdefault("appear_behave", {})
        widget = appear_behave.setdefault("widget", {})
        widget["memory_row"] = show
        self.save_config()
        self.showMemoryRowChanged.emit()
    # endregion #
