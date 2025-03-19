import sys

from random import randint as rand

from PyQt6 import uic
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve, QSize, QPoint, QUrl, QObject
from PyQt6.QtGui import QColor, QIcon, QPixmap, QPainter, QDesktopServices
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QProgressBar, QGraphicsBlurEffect, QPushButton, \
    QGraphicsDropShadowEffect, QSystemTrayIcon, QFrame, QGraphicsOpacityEffect, QHBoxLayout

from qfluentwidgets import PushButton, SystemTrayMenu, FluentIcon as fIcon, Action

import conf

excluded_number = []

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.m_Position = None
        self.p_Position = None
        self.r_Position = None
        self.init_ui()
        self.systemTrayIcon = SystemTrayIcon(self)
        self.systemTrayIcon.show()

    def init_ui(self):
        uic.loadUi("widget.ui", self)

        # 设置窗口无边框和透明背景
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        if sys.platform == 'darwin':
            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint |
                Qt.WindowType.Widget
            )
        else:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint |
                                Qt.WindowType.Tool)

        background = self.findChild(QFrame, 'backgnd')
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(28)
        shadow_effect.setXOffset(0)
        shadow_effect.setYOffset(6)
        shadow_effect.setColor(QColor(0, 0, 0, 75))
        background.setGraphicsEffect(shadow_effect)

        btn = self.findChild(PushButton, 'btn')
        btn.clicked.connect(lambda: self.pick())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.m_Position = event.globalPosition().toPoint() - self.pos()  # 获取鼠标相对窗口的位置
            self.p_Position = event.globalPosition().toPoint()  # 获取鼠标相对屏幕的位置
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.m_flag:
            self.move(event.globalPosition().toPoint() - self.m_Position)  # 更改窗口位置
            event.accept()

    def mouseReleaseEvent(self, event):
        self.r_Position = event.globalPosition()  # 获取鼠标相对窗口的位置

    def pick(self):
        num = rand(14, 14)
        while num in excluded_number:
            num = rand(14, 14)
        student = conf.get(num)
        name = self.findChild(QLabel, 'name')
        id = self.findChild(QLabel, 'id')
        name.setText(student['name'])
        id.setText(student['id'])

class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setIcon(parent.windowIcon())

        self.menu = SystemTrayMenu(parent=parent)
        self.menu.addActions([
            Action(fIcon.CLOSE, '关闭', triggered=lambda: sys.exit()),
        ])
        self.setContextMenu(self.menu)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    widget.raise_()
    sys.exit(app.exec())
