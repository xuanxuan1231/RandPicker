"""
主模块
"""
import sys
import os
from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QApplication
from loguru import logger

from core.choice import ChoiceMaker
from core.config import SettingsConfig, StudentsConfig
from core.integration import NotificationManager
from core.settings import SettingsWindow
from core.tray import RPTray
from core.widget import RPWidget


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

        self.app = QApplication.instance()

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

    @Slot()
    def restart(self):
        logger.debug("触发重新启动")
        os.execl(sys.executable, sys.executable, *sys.argv)

    @Slot()
    def quit(self):
        logger.info("退出 RandPicker。")
        self.app.quit()
