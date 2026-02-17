"""
主模块
"""
import os
import sys

from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QApplication
from RinUI import ThemeManager
from loguru import logger

from core.choice import ChoiceMaker
from core.config import SettingsConfig, StudentsConfig
from core.integration import NotificationManager, ciService
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
        self.themeManager = None

        self.app = QApplication.instance()

        self.init()

    def init(self):
        logger.info("正在启动 RandPicker。")

        self.settingsConfig = SettingsConfig(self)

        self.open_uiaccess()

        self.studentsConfig = StudentsConfig(self)
        self.notificationManager = NotificationManager(self)
        self.choiceMaker = ChoiceMaker(self)
        self.themeManager = ThemeManager()

        self.themeManager.themeChanged.connect(lambda theme: self.onThemeChanged(theme))

        self.widget = RPWidget(self)
        self.widget.show()

        self.tray = RPTray(self)

    def open_settings(self):
        self.settingsWindow = SettingsWindow(self)

    def onThemeChanged(self, theme):
        logger.info(f"主题切换为 {theme}。")

    @Slot()
    def restart(self):
        logger.debug("触发重新启动")
        os.execl(sys.executable, sys.executable, *sys.argv)

    @Slot()
    def quit(self):
        logger.info("退出 RandPicker。")
        self.cleanup()
        self.app.quit()

    def cleanup(self):
        ciService.stop()

    def open_uiaccess(self):
        if not self.settingsConfig.getUIAccessEnabled():
            logger.debug("未启用 UIAccess，跳过加载。")
            return

        try:
            from core.uiaccess import IsUIAccess, run_with_uiaccess, check_privileges
        except ImportError as e:
            logger.error(f"导入 UIAccess 模块时发生错误: {e}，跳过启用 UIAccess。")
            return

        if IsUIAccess():
            logger.info("当前进程已具有 UIAccess 权限。")
            return

        if not check_privileges():
            logger.warning("您期望使用 UIAccess，但启用 UIAccess 需要管理员权限。")
            return

        try:
            logger.info("尝试以 UIAccess 权限重新启动程序。")
            if getattr(sys, "frozen", False):
                exe = sys.executable
                args = sys.argv[1:]
                cmdline = " ".join([f'"{exe}"'] + [f'"{arg}"' for arg in args])
            else:
                exe = sys.executable
                script = sys.argv[0]
                args = sys.argv[1:]
                cmdline = " ".join([f'"{exe}"', f'"{script}"'] + [f'"{arg}"' for arg in args])
            pid = run_with_uiaccess(cmdline, exe)
            if pid is not None:
                logger.info(f"UIAccess 进程 {pid} 启动成功，退出当前进程。")
                self.quit()
            else:
                logger.error("UIAccess 进程启动失败，继续使用当前进程。")
        except Exception as e:
            logger.error(f"启动 UIAccess 进程时发生异常: {e}，继续使用当前进程。")
