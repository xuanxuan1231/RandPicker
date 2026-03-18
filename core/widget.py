"""
浮窗后端
"""

from RinUI.core.launcher import RinUIWindow
from loguru import logger

from .choice import ChoiceMaker
from .config.dirs import *
from .config.settings import SettingsConfig
from .version_info import versionInfo


class RPWidget(RinUIWindow):
    """Load and manage the floating widget window using RinUIWindow."""

    _instance: "RPWidget" = None

    @classmethod
    def instance(cls) -> "RPWidget":
        return cls._instance

    def __init__(self, parent=None):
        RPWidget._instance = self

        qml_path = QML_DIR / "widget.qml"
        if not qml_path.exists():
            logger.error(f"Widget QML 文件不存在: {qml_path}")
            self.window = None
            return
        

        from .main import RPMain
        self.main = RPMain.instance()

        super().__init__()
        self.engine.rootContext().setContextProperty("widget", self)
        self.engine.rootContext().setContextProperty("AppMain", self.main)
        self.engine.rootContext().setContextProperty("ChoiceMaker", ChoiceMaker.instance())
        self.engine.rootContext().setContextProperty("VersionInfo", versionInfo)
        self.engine.rootContext().setContextProperty("SettingsConfig", SettingsConfig.instance())

        self.load(qml_path)
        self.window = getattr(self, "root_window", None)

    def show(self) -> None:
        if self.window:
            self.window.show()
        else:
            logger.error("Widget 窗口未初始化，无法显示。")

    def hide(self) -> None:
        if self.window:
            self.window.hide()

    def close(self) -> None:
        if self.window:
            self.window.close()
