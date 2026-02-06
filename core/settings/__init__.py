"""
设置模块
"""

from RinUI import RinUIWindow

from .service import SettingsService
from ..config.dirs import *
from ..version_info import versionInfo

class SettingsWindow(RinUIWindow):
    def __init__(self, parent):
        super().__init__()

        self.main = parent
        self.studentsConfig = parent.studentsConfig
        self.config = parent.settingsConfig
        self.service = SettingsService()

        self.engine.rootContext().setContextProperty("SettingsService", self.service)
        self.engine.rootContext().setContextProperty("SettingsConfig", self.config)
        self.engine.rootContext().setContextProperty("ChoiceMaker", self.main.choiceMaker)
        self.engine.rootContext().setContextProperty("StudentsConfig", self.studentsConfig)
        self.engine.rootContext().setContextProperty("VersionInfo", versionInfo)
        self.engine.rootContext().setContextProperty("AppMain", self.main)
        self.engine.rootContext().setContextProperty("NotificationManager", self.main.notificationManager)

        self.load(QML_DIR / "settings" / "main.qml")

        self.main.themeManager.themeChanged.connect(lambda theme: self.onThemeChanged(theme))
        icon_path = str(
            ASSETS_DIR / ("icon-light.jpg" if self.main.themeManager.get_theme() == "Light" else "icon-dark.jpg"))
        self.setIcon(icon_path)

    def onThemeChanged(self, theme):
        icon_path = str(
            ASSETS_DIR / ("icon-light.jpg" if self.main.themeManager.get_theme() == "Light" else "icon-dark.jpg"))
        self.setIcon(icon_path)