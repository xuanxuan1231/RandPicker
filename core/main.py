"""
主模块
"""
from PySide6.QtCore import QObject
from loguru import logger

from core.choice import ChoiceMaker
from core.config import SettingsConfig, StudentsConfig
from core.widget import RPWidget
from core.tray import RPTray
from core.integration import NotificationManager
from core.settings import SettingsWindow


class RPMain(QObject):
    def __init__(self):
        super().__init__()
        self.settingsWindow = None
        self.tray = None
        self.choiceMaker = None
        self.notificationManager = None
        self.studentsConfig = None
        self.settingsConfig = None
        self.widget = None
        self.init()

    def init(self):
        logger.info("正在启动 RandPicker。")

        self.settingsConfig = SettingsConfig(self)
        self.studentsConfig = StudentsConfig(self)
        self.notificationManager = NotificationManager(self)
        self.choiceMaker = ChoiceMaker(self)

        self.widget = RPWidget(self)
        self.widget.show()

        self.tray = RPTray(self)

    def open_settings(self):
        self.settingsWindow = SettingsWindow(self)


