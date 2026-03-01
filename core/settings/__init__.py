"""
设置模块
"""

from RinUI import RinUIWindow

from .service import SettingsService
from ..choice import ChoiceMaker
from ..config import SettingsConfig, StudentsConfig
from ..config.dirs import *
from ..integration import NotificationManager
from ..version_info import versionInfo


class SettingsWindow(RinUIWindow):
    _instance: "SettingsWindow" = None

    def __init__(self, parent=None):
        super().__init__()

        from ..main import RPMain  # 延迟导入，避免循环引用
        self.main = RPMain.instance()

        self.service = SettingsService()

        self.engine.rootContext().setContextProperty("SettingsService", self.service)
        self.engine.rootContext().setContextProperty("SettingsConfig", SettingsConfig.instance())
        self.engine.rootContext().setContextProperty("ChoiceMaker", ChoiceMaker.instance())
        self.engine.rootContext().setContextProperty("StudentsConfig", StudentsConfig.instance())
        self.engine.rootContext().setContextProperty("VersionInfo", versionInfo)
        self.engine.rootContext().setContextProperty("AppMain", self.main)
        self.engine.rootContext().setContextProperty("NotificationManager", NotificationManager.instance())

        self.load(QML_DIR / "settings" / "main.qml")

        self.main.themeManager.themeChanged.connect(self.onThemeChanged)
        icon_path = str(
            ASSETS_DIR / ("icon-light.jpg" if self.main.themeManager.get_theme() == "Light" else "icon-dark.jpg"))
        self.setIcon(icon_path)

    @classmethod
    def instance(cls) -> "SettingsWindow":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def onThemeChanged(self):
        icon_path = str(
            ASSETS_DIR / ("icon-light.jpg" if self.main.themeManager.get_theme() == "Light" else "icon-dark.jpg"))
        self.setIcon(icon_path)
