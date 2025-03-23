import os
import sys
from random import choices

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QMouseEvent, QIcon, QPixmap, QPainter, QPainterPath
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGraphicsDropShadowEffect, QSystemTrayIcon, QFrame
from loguru import logger
from qfluentwidgets import PushButton, SystemTrayMenu, FluentIcon as fIcon, Action

import conf
from settings import open_settings, restart

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
        
        # 初始化时显示默认头像
        self.show_default_avatar()

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
            self.r_Position = event.globalPosition().toPoint()  # 记录鼠标释放位置
            event.accept()

    def pick(self):
        """
        随机选人。
        """
        self.is_picking = True
        # num = rand(1, conf.get_students_num())
        num = choices(list(range(1, conf.get_students_num() + 1)), weights=conf.get_weight(), k=1)[0]
        logger.info(f'随机数已生成。JSON 索引是 {num - 1}。它的选择权重是 {conf.get_weight()[num - 1]}。')
        student = conf.get(num)
        logger.debug(f'已获取 JSON 索引是 {num - 1} 的学生信息。{student}')
        name = self.findChild(QLabel, 'name')
        id_ = self.findChild(QLabel, 'id')
        avatar = self.findChild(QLabel, 'avatar')
        name.setText(f'{str(student['id'])[-2:]} {student['name']}')
        id_.setText(str(student['id']))
        
        # 设置头像
        avatar_path = None
        # 尝试不同的图片格式
        for ext in ['png', 'jpg', 'jpeg']:
            temp_path = f'./stu_photo/{student["id"]}.{ext}'
            if os.path.exists(temp_path):
                avatar_path = temp_path
                break
        
        # 如果没有找到学生照片，使用默认头像
        if not avatar_path and os.path.exists('./stu_photo/default.jpeg'):
            avatar_path = './stu_photo/default.jpeg'
            
        # 从配置文件获取头像大小
        avatar_size = int(conf.get_ini('UI', 'avatar_size'))
        
        if avatar_path:
            pixmap = QPixmap(avatar_path)
            # 确保图片按比例缩放到设定大小
            scaled_pixmap = pixmap.scaled(avatar_size, avatar_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
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
        else:
            # 如果连默认头像都没有，则显示空白
            avatar.setPixmap(QPixmap())
            
        avatar.setStyleSheet(f'border-radius: {avatar_size//2}px; background-color: transparent;')
        self.is_picking = False

    def show_default_avatar(self):
        """显示默认头像"""
        avatar = self.findChild(QLabel, 'avatar')
        avatar_size = int(conf.get_ini('UI', 'avatar_size'))
        
        # 使用默认头像
        if os.path.exists('./stu_photo/default.jpeg'):
            pixmap = QPixmap('./stu_photo/default.jpeg')
            # 确保图片按比例缩放到设定大小
            scaled_pixmap = pixmap.scaled(avatar_size, avatar_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
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
        else:
            avatar.setPixmap(QPixmap())
        
        # 设置圆角样式
        avatar.setStyleSheet(f'border-radius: {avatar_size//2}px; background-color: transparent;')
    
    def clear(self):
        if not self.is_picking:
            name = self.findChild(QLabel, 'name')
            id_ = self.findChild(QLabel, 'id')
            name.setText('')
            id_.setText('')
            logger.info('清除结果')
            return 0
        logger.warning('没有清除结果，因为正在选人。')

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and conf.get_ini('UI', 'edge_hide') == 'true' and self.r_Position is not None:
            screen = QApplication.screenAt(event.globalPosition().toPoint())
            if not screen:
                screen = QApplication.primaryScreen()
            screen_geometry = screen.geometry()
            edge_distance = int(conf.get_ini('UI', 'edge_distance'))
            hidden_width = int(conf.get_ini('UI', 'hidden_width'))
            window_geometry = self.geometry()

            # 检测是否靠近屏幕边缘
            if self.r_Position.x() <= screen_geometry.left() + edge_distance:
                # 靠左边缘
                window_geometry.moveLeft(screen_geometry.left() - window_geometry.width() + hidden_width)
                self.setGeometry(window_geometry)
                logger.info('窗口贴靠到左边缘')
            elif self.r_Position.x() >= screen_geometry.right() - edge_distance:
                # 靠右边缘
                window_geometry.moveLeft(screen_geometry.right() - hidden_width)
                self.setGeometry(window_geometry)
                logger.info('窗口贴靠到右边缘')
            event.accept()

    def mousePressEvent(self, event: QMouseEvent):
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
                    window_geometry.moveLeft(screen_geometry.left())
                else:
                    window_geometry.moveLeft(screen_geometry.right() - window_geometry.width())
                self.setGeometry(window_geometry)
                logger.info('窗口恢复显示')
                event.accept()
                return

            # 如果窗口未隐藏，则处理正常的拖动
            self.m_Position = event.globalPosition().toPoint() - self.pos()  # 获取鼠标相对窗口的位置
            self.p_Position = event.globalPosition().toPoint()  # 获取鼠标相对屏幕的位置
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
            Action(fIcon.SYNC, '重新启动', triggered=lambda: restart()),
            Action(fIcon.CLOSE, '关闭', triggered=lambda: sys.exit()),
        ])
        self.setContextMenu(self.menu)


if __name__ == "__main__":
    os.environ['QT_SCALE_FACTOR'] = str(conf.get_ini('General', 'scale'))
    app = QApplication(sys.argv)
    logger.info(f"RandPicker 启动。缩放系数 {os.environ['QT_SCALE_FACTOR']}。")
    logger.info("欢迎。")
    conf.check_config()
    widget = Widget()
    widget.show()
    widget.raise_()

    app.setQuitOnLastWindowClosed(False)

    sys.exit(app.exec())
