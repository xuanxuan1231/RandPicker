"""
系统托盘菜单：提供显示/隐藏与退出控制。
"""

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication, QMenu, QStyle, QSystemTrayIcon
from loguru import logger


class RPTray(QObject):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.tray = None
        self.menu = None
        self.toggle_action = None
        self._init_tray()

    def _init_tray(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            logger.warning("系统托盘不可用，跳过托盘菜单。")
            return

        icon = QApplication.style().standardIcon(QStyle.SP_ComputerIcon)
        self.tray = QSystemTrayIcon(icon, self)
        self.tray.setToolTip("RandPicker")

        self.menu = QMenu()
        self.toggle_action = self.menu.addAction("隐藏窗口", self.toggle_visibility)
        self.menu.addSeparator()
        self.menu.addAction("退出", self.quit_app)

        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self._handle_activation)
        self.tray.show()
        self._sync_action_text()

    def _handle_activation(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.toggle_visibility()

    def toggle_visibility(self):
        widget = getattr(self.main, "widget", None)
        if not widget or not getattr(widget, "window", None):
            logger.warning("窗口未初始化，无法切换可见性。")
            return

        if widget.window.isVisible():
            widget.hide()
        else:
            widget.show()
        self._sync_action_text()

    def _sync_action_text(self):
        widget = getattr(self.main, "widget", None)
        if not self.toggle_action or not widget or not getattr(widget, "window", None):
            return
        text = "隐藏窗口" if widget.window.isVisible() else "显示窗口"
        self.toggle_action.setText(text)

    def quit_app(self):
        widget = getattr(self.main, "widget", None)
        if widget:
            widget.close()
        QApplication.quit()
