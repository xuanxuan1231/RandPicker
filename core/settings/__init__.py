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

        self.parent = parent
        self.studentsConfig = parent.studentsConfig
        self.config = parent.settingsConfig
        self.service = SettingsService()

        self.engine.rootContext().setContextProperty("SettingsService", self.service)
        self.engine.rootContext().setContextProperty("SettingsConfig", self.config)
        self.engine.rootContext().setContextProperty("ChoiceMaker", self.parent.choiceMaker)
        self.engine.rootContext().setContextProperty("StudentsConfig", self.studentsConfig)
        self.engine.rootContext().setContextProperty("VersionInfo", versionInfo)
        self.engine.rootContext().setContextProperty("AppMain", self.parent)
        self.engine.rootContext().setContextProperty("NotificationManager", self.parent.notificationManager)

        self.load(QML_DIR / "settings" / "main.qml")
