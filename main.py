import os
import sys
from random import choices

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QMouseEvent, QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGraphicsDropShadowEffect, QSystemTrayIcon, QFrame
from loguru import logger
from qfluentwidgets import PushButton, SystemTrayMenu, FluentIcon as fIcon, Action, Dialog

import conf
from settings import open_settings, share

# 适配高DPI缩放
QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

logger.add("./log/RandPicker_{time}.log", rotation="1 MB", encoding="utf-8", retention="1 minute")


class Widget(QWidget):
    """
    主浮窗。
    """

    def __init__(self):
        super().__init__()
        self.m_Position = None
        self.p_Position = None
        self.r_Position = None
        self.is_picking = False
        self.init_ui()
        self.setWindowIcon(QIcon('./img/Logo.png'))
        self.systemTrayIcon = SystemTrayIcon(self)
        self.systemTrayIcon.show()

    def init_ui(self):
        uic.loadUi("./ui/widget.ui", self)

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

        btn_clear = self.findChild(PushButton, 'btn_clear')
        btn_clear.clicked.connect(lambda: self.clear())
        # btn_clear.clicked.connect(lambda: open_settings())  # Debug Only

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.m_Position = event.globalPosition().toPoint() - self.pos()  # 获取鼠标相对窗口的位置
            self.p_Position = event.globalPosition().toPoint()  # 获取鼠标相对屏幕的位置
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.m_Position)  # 更改窗口位置
            event.accept()

    def pick(self):
        """
        随机选人。
        """
        self.is_picking = True
        # num = rand(1, conf.get_students_num())
        num = choices(conf.get_students_list(), weights=conf.get_weight(), k=1)[0]
        logger.info(f'随机数已生成。JSON 索引是 {num - 1}。它的选择权重是 {conf.get_all_weight()[num - 1]}。')
        student = conf.get(num)
        logger.debug(f'已获取 JSON 索引是 {num - 1} 的学生信息。{student}')
        name = self.findChild(QLabel, 'name')
        id_ = self.findChild(QLabel, 'id')
        name.setText(f'{str(student['id'])[-2:]} {student['name']}')
        id_.setText(str(student['id']))
        self.is_picking = False

    def clear(self):  # 清除结果
        if not self.is_picking:
            name = self.findChild(QLabel, 'name')
            id_ = self.findChild(QLabel, 'id')
            name.setText('无结果')
            id_.setText('000000')
            logger.info('清除结果')
            return 0
        logger.warning('没有清除结果，因为正在选人。')


class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setIcon(parent.windowIcon())
        self.menu = SystemTrayMenu(title="RandPicker", parent=parent)
        self.menu.addActions([
            Action(fIcon.SETTING, '设置', triggered=lambda: open_settings()),
        ])
        self.menu.addSeparator()
        self.menu.addActions([
            # Action(fIcon.SYNC, '重新启动', triggered=lambda: restart()),
            Action(fIcon.CLOSE, '关闭', triggered=lambda: sys.exit()),
        ])
        self.setContextMenu(self.menu)


if __name__ == "__main__":
    os.environ['QT_SCALE_FACTOR'] = str(conf.get_ini('General', 'scale'))
    share.create(1)
    app = QApplication(sys.argv)
    logger.info(f"RandPicker 启动。缩放系数 {os.environ['QT_SCALE_FACTOR']}。")
    if share.attach():
        logger.warning("有一个实例正在运行，或者上次没有正常退出。")
        logger.error("不欢迎。")
        msg_box = Dialog(
            'RandPicker 正在运行',
            'RandPicker 正在运行！请勿打开多个实例，否则将会出现不可预知的问题。'
        )
        msg_box.yesButton.setText('好')
        msg_box.cancelButton.hide()
        msg_box.buttonLayout.insertStretch(0, 1)
        msg_box.setFixedWidth(550)
        msg_box.exec()
        logger.info("退出。")
        sys.exit(-1)
    logger.info("欢迎。")
    conf.check_config()
    widget = Widget()
    widget.show()
    widget.raise_()

    app.setQuitOnLastWindowClosed(False)

    sys.exit(app.exec())
