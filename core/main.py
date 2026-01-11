"""
主模块
"""
from PySide6.QtCore import QObject
from loguru import logger

from core.choice import ChoiceMaker
from core.config.settings import SettingsConfig
from core.config.students import StudentsConfig
from core.widget import RPWidget
from core.tray import RPTray
from core.notification import NotificationManager


class RPMain(QObject):
    def __init__(self):
        super().__init__()
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

