import os
import sys
from random import choices

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QMouseEvent, QIcon, QPixmap, QPainter, QPainterPath
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGraphicsDropShadowEffect, QSystemTrayIcon, QFrame
from loguru import logger
from qfluentwidgets import PushButton, SystemTrayMenu, FluentIcon as fIcon, Action, Dialog, AvatarWidget, \
    PrimaryPushButton

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
        self.is_avatar = False
        self.init_ui()
        self.setWindowIcon(QIcon('./img/Logo.png'))
        self.systemTrayIcon = SystemTrayIcon(self)
        self.systemTrayIcon.show()

    def init_ui(self):
        self.is_avatar = True if conf.get_ini('UI', 'avatar') == 'true' else False
        if self.is_avatar:
            uic.loadUi("./ui/widget.ui", self)
        else:
            uic.loadUi("./ui/widget-no-avatar.ui", self)

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

        btn = self.findChild(PrimaryPushButton, 'btn')
        btn.clicked.connect(lambda: self.pick())

        btn_clear = self.findChild(PushButton, 'btn_clear')
        btn_clear.clicked.connect(lambda: self.clear())

        if self.is_avatar:
            self.show_avatar()

    def mousePressEvent(self, event: QMouseEvent):
        edge_distance = int(conf.get_ini('UI', 'edge_distance'))
        if event.button() == Qt.MouseButton.LeftButton:
            # 检查窗口是否处于隐藏状态
            screen = QApplication.screenAt(event.globalPosition().toPoint())
            if not screen:
                screen = QApplication.primaryScreen()
            screen_geometry = screen.geometry()
            window_geometry = self.geometry()

            # 如果窗口被隐藏在左边或右边，则恢复显示
            if window_geometry.left() < screen_geometry.left() or window_geometry.right() > screen_geometry.right():
                # 计算窗口应该显示的位置
                if window_geometry.left() < screen_geometry.left():
                    window_geometry.moveLeft(screen_geometry.left()  + edge_distance)
                else:
                    window_geometry.moveRight(screen_geometry.right() - window_geometry.width())
                self.setGeometry(window_geometry)
                logger.info('窗口恢复显示')
                event.accept()
                return

            # 如果窗口未隐藏，则处理正常的拖动
            self.m_Position = event.globalPosition().toPoint() - self.pos()  # 获取鼠标相对窗口的位置
            self.p_Position = event.globalPosition().toPoint()  # 获取鼠标相对屏幕的位置
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.m_Position)  # 更改窗口位置
            self.r_Position = event.globalPosition().toPoint()  # 记录鼠标释放位置
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

        if self.is_avatar:
            # 设置头像
            avatar_path = None
            # 尝试不同的图片格式
            for ext in ['png', 'jpg', 'jpeg']:
                temp_path = f'./img/stu/{student['id']}.{ext}'
                if os.path.exists(temp_path):
                    avatar_path = temp_path
                    logger.success(f"找到了学生 {student['id']} 的头像 {student['id']}.{ext}。")
                    break

            self.show_avatar(avatar_path)
        self.is_picking = False

    
    def clear(self):
        if not self.is_picking:
            name = self.findChild(QLabel, 'name')
            id_ = self.findChild(QLabel, 'id')
            name.setText('无结果')
            id_.setText('000000')
            if self.is_avatar:
                self.show_avatar()
            logger.info('清除结果')
            return 0
        logger.warning('没有清除结果，因为正在选人。')

    def show_avatar(self, file_path='./img/stu/default.jpeg'):
        avatar = self.findChild(QLabel, 'avatar')
        avatar_size = int(conf.get_ini('UI', 'avatar_size'))
        if file_path is not None and os.path.exists(file_path):
            file_path = file_path
        elif os.path.exists('./img/stu/default.jpeg'):
            file_path = './img/stu/default.jpeg'
            logger.warning(f"没有找到头像 {file_path}。使用默认头像。")
        else:
            avatar.setPixmap(QPixmap())
            avatar.setStyleSheet(f'border-radius: {avatar_size // 2}px; background-color: transparent;')
            logger.warning(f"没有找到头像 {file_path} 和默认头像。使用空白。")
            return
        pixmap = QPixmap(file_path)
        # 确保图片按比例缩放到设定大小
        scaled_pixmap = pixmap.scaled(avatar_size, avatar_size, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        # 创建一个设定大小的透明pixmap
        final_pixmap = QPixmap(avatar_size, avatar_size)
        final_pixmap.fill(Qt.GlobalColor.transparent)
        # 在中心位置绘制缩放后的图片
        painter = QPainter(final_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 计算居中位置
        x = (avatar_size - scaled_pixmap.width()) // 2
        y = (avatar_size - scaled_pixmap.height()) // 2
        painter.drawPixmap(x, y, scaled_pixmap)
        painter.end()

        # 创建圆形遮罩
        mask = QPixmap(avatar_size, avatar_size)
        mask.fill(Qt.GlobalColor.transparent)
        mask_painter = QPainter(mask)
        mask_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        mask_painter.setBrush(Qt.GlobalColor.white)
        mask_painter.drawEllipse(0, 0, avatar_size, avatar_size)
        mask_painter.end()

        # 应用圆形遮罩
        masked_pixmap = QPixmap(avatar_size, avatar_size)
        masked_pixmap.fill(Qt.GlobalColor.transparent)
        masked_painter = QPainter(masked_pixmap)
        masked_painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 使用QPainterPath创建圆形裁剪区域
        path = QPainterPath()
        path.addEllipse(0, 0, avatar_size, avatar_size)
        masked_painter.setClipPath(path)
        masked_painter.drawPixmap(0, 0, final_pixmap)
        masked_painter.end()

        avatar.setPixmap(masked_pixmap)
        logger.success(f"显示头像 {file_path}。")
        avatar.setStyleSheet(f'border-radius: {avatar_size // 2}px; background-color: transparent;')

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and conf.get_ini('UI', 'edge_hide') == 'true' and self.r_Position is not None:
            screen = QApplication.screenAt(event.globalPosition().toPoint())
            if not screen:
                screen = QApplication.primaryScreen()
            screen_geometry = screen.geometry()
            screen_available = screen.availableGeometry()
            edge_distance = int(conf.get_ini('UI', 'edge_distance'))
            hidden_width = int(conf.get_ini('UI', 'hidden_width'))
            window_geometry = self.geometry()

            # 检测是否靠近屏幕边缘
            if window_geometry.left() < screen_geometry.left() + edge_distance:
                # 靠左边缘
                window_geometry.moveRight(screen_geometry.left() + hidden_width)
                self.setGeometry(window_geometry)
                logger.info('窗口贴靠到左边缘')
            elif window_geometry.right() > screen_geometry.right() - edge_distance:
                # 靠右边缘
                window_geometry.moveLeft(screen_geometry.right() - hidden_width)
                self.setGeometry(window_geometry)
                logger.info('窗口贴靠到右边缘。')
            '''elif window_geometry.y() > screen_available.top():
                # 靠上边缘
                window_geometry.moveTop(screen_available.top())
                logger.info('窗口从上边缘弹出。')
            elif window_geometry.bottom() > screen_available.bottom():
                # 靠下边缘
                window_geometry.moveBottom(screen_geometry.bottom())
                logger.info('窗口从下边缘弹出。')'''
            event.accept()



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
