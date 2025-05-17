"""RandPicker 设置窗口。

此模块提供RandPicker的主设置窗口实现。
"""
import os
import sys
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, QSharedMemory, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from loguru import logger
from qfluentwidgets import FluentWindow, FluentIcon as fIcon, NavigationItemPosition

import conf
import update
from .interfaces.student_interface import setup_student_edit_interface, save_students
from .interfaces.group_interface import setup_group_edit_interface, setup_group_enabled
from .interfaces.ui_interface import setup_ui_interface
from .interfaces.about_interface import setup_about_interface
from .interfaces.update_interface import setup_update_interface

# 全局变量
settings = None
share = QSharedMemory('RandPicker')

APP_VERSION = str(update.APP_VERSION)
UPDATER_VERSION = str(update.UPDATER_VERSION) if hasattr(update, 'UPDATER_VERSION') else "不适用"


def open_settings():
    """
    启动设置。
    """
    global settings
    if settings is None or not settings.isVisible():
        settings = Settings()
        settings.closed.connect(cleanup_settings)
        settings.show()
        logger.info('启动设置。')
    else:
        settings.raise_()
        settings.activateWindow()


def cleanup_settings():
    """
    清理设置。
    """
    global settings
    logger.info('关闭设置。')
    del settings
    settings = None


class Settings(FluentWindow):
    """
    设置类。这个类没有参数。
    """
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.aboutInterface = uic.loadUi('./ui/settings/about.ui')
        self.aboutInterface.setObjectName('aboutInterface')
        self.stuEditInterface = uic.loadUi('./ui/settings/students.ui')
        self.stuEditInterface.setObjectName('stuEditInterface')
        self.uiInterface = uic.loadUi('./ui/settings/widget.ui')
        self.uiInterface.setObjectName('uiInterface')
        self.groupEditInterface = uic.loadUi('./ui/settings/group.ui')
        self.groupEditInterface.setObjectName('groupEditInterface')
        self.updateInterface = uic.loadUi('./ui/settings/update.ui')

        self.init_nav()
        self.setup_ui()

    def init_nav(self):  # 设置侧边栏
        self.addSubInterface(self.stuEditInterface, fIcon.EDIT, '学生编辑')
        self.addSubInterface(self.groupEditInterface, fIcon.PEOPLE, '小组编辑')
        self.navigationInterface.addSeparator(NavigationItemPosition.BOTTOM)
        if sys.platform == 'win32':
            self.addSubInterface(self.updateInterface, fIcon.UPDATE, '更新', NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.uiInterface, fIcon.SETTING, '界面设置', NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.aboutInterface, fIcon.INFO, '关于', NavigationItemPosition.BOTTOM)

    def setup_ui(self):  # 设置所有页面
        self.stackedWidget.setCurrentIndex(0)  # 设置初始页面
        self.setMinimumWidth(900)
        self.setMinimumHeight(400)
        self.navigationInterface.setExpandWidth(160)
        self.navigationInterface.setCollapsible(False)
        self.setMicaEffectEnabled(True)  # 启用云母效果

        # 修复设置窗口在各个屏幕分辨率DPI下的窗口大小
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        width = int(screen_width * 0.7)
        height = int(screen_height * 0.7)

        self.move(int(screen_width / 2 - width / 2), 150)
        self.resize(width, height)

        self.setWindowTitle('RandPicker 设置')
        self.setWindowIcon(QIcon('./img/Logo.png'))
        setup_about_interface(self)
        setup_student_edit_interface(self)
        setup_ui_interface(self)
        setup_group_edit_interface(self)
        setup_update_interface(self)

    def closeEvent(self, event):  # 重写 closeEvent
        self.closed.emit()
        event.accept()


def restart():
    global share
    if share.isAttached():
        share.detach()
        # share.deleteLater()
    logger.info("重新启动")
    os.execl(sys.executable, sys.executable, *sys.argv)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Settings()
    w.show()
    sys.exit(app.exec())