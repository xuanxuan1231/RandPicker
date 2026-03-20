"""
主模块
"""
import os
import sys

from PySide6.QtCore import QObject, Property, Slot
from PySide6.QtWidgets import QApplication
from RinUI import ThemeManager
from loguru import logger

from .choice import ChoiceMaker
from .config import SettingsConfig, StudentsConfig
from .integration import NotificationManager
from .integration.classisland import ClassIslandIntegration
from .settings import SettingsWindow
from .tray import RPTray
from .widget import RPWidget


class RPMain(QObject):
    _instance: "RPMain" = None

    @classmethod
    def instance(cls) -> "RPMain":
        return cls._instance

    def __init__(self):
        super().__init__()
        RPMain._instance = self
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

        # 软件基础设施
        self.themeManager = ThemeManager()
        self.tray = RPTray()
        self.settingsConfig = SettingsConfig()

        # UI Access
        self.open_uiaccess()

        # 其他核心组件
        self.studentsConfig = StudentsConfig()
        self.notificationManager = NotificationManager()
        self.choiceMaker = ChoiceMaker()
        
        self.themeManager.themeChanged.connect(lambda theme: self.onThemeChanged(theme))

        self.widget = RPWidget()
        self.widget.show()


    @Slot()
    def open_settings(self):
        self.settingsWindow = SettingsWindow.instance()
        self.settingsWindow.show()
        self.settingsWindow.raise_()

    @Property(bool, constant=True)
    def isAdmin(self) -> bool:
        """返回当前进程是否以管理员（提升权限）身份运行。"""
        if sys.platform != "win32":
            return False
        try:
            from ctypes import windll
            return bool(windll.shell32.IsUserAnAdmin())
        except Exception:
            return False

    def onThemeChanged(self, theme):
        logger.info(f"主题切换为 {theme}。")

    @Slot()
    def restart(self):
        logger.debug("触发重新启动")
        self.cleanup()
        os.execl(sys.executable, sys.executable, *sys.argv)

    @Slot()
    def restartAsAdmin(self):
        if sys.platform != "win32":
            logger.warning("仅支持在 Windows 上以管理员权限重新启动。")
            return

        from ctypes import windll
        from subprocess import list2cmdline

        if getattr(sys, "frozen", False):
            exe = sys.executable
            params = list2cmdline(sys.argv[1:])
        else:
            exe = sys.executable
            params = list2cmdline([sys.argv[0]] + sys.argv[1:])
        try:
            logger.info("尝试以管理员权限重新启动程序。")
            result = windll.shell32.ShellExecuteW(None, "runas", exe, params, None, 1)
            if result <= 32:
                # 错误
                logger.error(f"以管理员权限重新启动失败，错误码: {result}。")
                return
            # 确认提权成功
            self.quit()
        except Exception as e:
            logger.exception(f"以管理员权限重新启动时发生异常: {e}。")
            return

    @Slot()
    def quit(self):
        logger.info("退出 RandPicker。")
        self.cleanup()
        self.app.quit()

    def cleanup(self):
        ci = ClassIslandIntegration.instance()
        if ci:
            ci.stop()
        # 清理人脸抽选资源
        from .face import FaceChooser
        fc = FaceChooser.instance()
        if fc:
            fc.cleanup()

    def open_uiaccess(self):
        if not self.settingsConfig.getUIAccessEnabled():
            logger.debug("未启用 UIAccess，跳过加载。")
            return

        try:
            from .uiaccess import IsUIAccess, run_with_uiaccess, check_privileges
        except ImportError as e:
            logger.exception(f"导入 UIAccess 模块时发生错误: {e}，跳过启用 UIAccess。")
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
            logger.exception(f"启动 UIAccess 进程时发生异常: {e}，继续使用当前进程。")
