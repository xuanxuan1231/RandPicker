"""
浮窗后端：加载并控制 QML 窗口。
"""

from loguru import logger
from RinUI.core.launcher import RinUIWindow
from .config.dirs import *
from .git_info import gitInfo


class RPWidget(RinUIWindow):
    """Load and manage the floating widget window using RinUIWindow."""

    def __init__(self, parent=None):
        self.parent = parent

        qml_path = QML_DIR / "widget.qml"
        if not qml_path.exists():
            logger.exception(f"Widget QML 文件不存在: {qml_path}")
            self.window = None
            return
        super().__init__(qml_path)
        self.engine.rootContext().setContextProperty("widget", self)
        self.engine.rootContext().setContextProperty("ChoiceMaker", getattr(self.parent, "choiceMaker", None))
        self.engine.rootContext().setContextProperty("GitInfo", gitInfo)

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
