import os
import sys
from random import choices

from PyQt6 import uic
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QMouseEvent, QIcon, QPixmap, QPainter, QPainterPath, QPixmapCache
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGraphicsDropShadowEffect, QSystemTrayIcon, QFrame, QLayout
from loguru import logger
from qfluentwidgets import PushButton, SystemTrayMenu, FluentIcon as fIcon, Action, Dialog, PrimaryPushButton, \
    isDarkTheme, setTheme, Theme, qconfig, PixmapLabel

import conf
from settings import open_settings, share, restart

# 适配高DPI缩放
QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

widget = None
last_result = {}
last_pos = QPoint()

logger.add("./log/RandPicker_{time}.log", rotation="1 MB", encoding="utf-8", retention="1 minute")

# 自动切换主题
qconfig.themeChanged.connect(lambda: reload_widget())


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
        self.animation = None
        self.student = last_result
        self.init_ui()
        self.setWindowIcon(QIcon('./img/Logo.png'))
        self.systemTrayIcon = SystemTrayIcon(parent=self)
        self.systemTrayIcon.show()

    def init_ui(self):
        global last_pos
        self.is_avatar = True if conf.get_ini('UI', 'avatar') == 'true' else False
        # 设置主题
        if conf.get_ini('General', 'theme') == '0':
            setTheme(Theme.LIGHT)
        elif conf.get_ini('General', 'theme') == '1':
            setTheme(Theme.DARK)
        else:
            setTheme(Theme.AUTO)

        ui_file = f"./ui{'/dark/' if isDarkTheme() else '/'}{'widget.ui' if self.is_avatar else 'widget-no-avatar.ui'}"
        uic.loadUi(ui_file, self)

        logger.info(f"设置主题：{"深色" if isDarkTheme() else "浅色"}")

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

        self.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        if last_pos:
            logger.info(f'移动到重载前的位置 ({last_pos.x()}, {last_pos.y()})。')
            self.move(last_pos)
        elif conf.get_ini('Last', 'x') and conf.get_ini('Last', 'y'):
            x = int(conf.get_ini('Last', 'x'))
            y = int(conf.get_ini('Last', 'y'))
            pos = QPoint(x, y)
            logger.info(f'移动到上次关闭的位置 ({x}, {y})。')
            self.move(pos)

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

        self.clear()

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
            if window_geometry.left() < screen_geometry.left() or \
                    window_geometry.right() > screen_geometry.right() or \
                    window_geometry.top() < screen_geometry.top() or \
                    window_geometry.bottom() > screen_geometry.bottom():
                # 计算窗口应该显示的位置
                if window_geometry.left() < screen_geometry.left():
                    window_geometry.moveLeft(screen_geometry.left() + edge_distance)
                else:
                    window_geometry.moveRight(screen_geometry.right() - edge_distance)
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
        num = choices(conf.get_students_list(), weights=conf.get_weight(), k=1)[0]
        logger.info(f'随机数已生成。JSON 索引是 {num - 1}。它的选择权重是 {conf.get_all_weight()[num - 1]}。')
        self.student = conf.get(num)
        logger.debug(f'已获取 JSON 索引是 {num - 1} 的学生信息。{self.student}')
        name = self.findChild(QLabel, 'name')
        id_ = self.findChild(QLabel, 'id')
        name.setText(f'{str(self.student['id'])[-2:]} {self.student['name']}')
        id_.setText(str(self.student['id']))

        if self.is_avatar:
            # 设置头像
            avatar_path = None
            # 尝试不同的图片格式
            for ext in ['png', 'jpg', 'jpeg']:
                temp_path = f'./img/stu/{self.student['id']}.{ext}'
                if os.path.exists(temp_path):
                    avatar_path = temp_path
                    logger.success(f"找到了学生 {self.student['id']} 的头像 {self.student['id']}.{ext}。")
                    break
            self.student['avatar'] = avatar_path
            self.show_avatar(avatar_path)
        self.is_picking = False

    def clear(self):
        global last_result
        if not self.is_picking:
            name = self.findChild(QLabel, 'name')
            id_ = self.findChild(QLabel, 'id')
            if last_result:
                name.setText(f"{str(self.student['id'])[-2:]} {last_result['name']}")
                id_.setText(str(last_result['id']))
                if self.is_avatar:
                    self.show_avatar(last_result['avatar'])
                last_result = {}
                logger.info(f'加载重载前的结果。{last_result}')
            else:
                name.setText('无结果')
                id_.setText('000000')
                if self.is_avatar:
                    self.show_avatar()
                logger.info('清除结果')
            return
        logger.warning('没有清除结果，因为正在选人。')

    def show_avatar(self, file_path='./img/stu/default.jpeg'):
        avatar = self.findChild(PixmapLabel, 'avatar')
        avatar_size = int(conf.get_ini('UI', 'avatar_size'))
        if file_path is not None and os.path.exists(file_path):
            file_path = file_path
        elif os.path.exists('./img/stu/default.jpeg'):
            logger.warning(f"没有找到头像。使用默认头像。")
            file_path = './img/stu/default.jpeg'
        else:
            avatar.setPixmap(QPixmap())
            avatar.setStyleSheet(f'border-radius: {avatar_size // 2}px; background-color: transparent;')
            logger.warning(f"没有找到头像 {file_path} 和默认头像。使用空白。")
            return

        # 使用复合缓存键，避免重复创建
        final_cache_key = f"final_{file_path}_{avatar_size}"
        final_pixmap = QPixmapCache.find(final_cache_key)

        if not final_pixmap:
            # 原始图片缓存
            cache_key = f"{file_path}_{avatar_size}"
            pixmap = QPixmapCache.find(cache_key)
            if not pixmap:
                pixmap = QPixmap(file_path)
                scaled_pixmap = pixmap.scaled(avatar_size, avatar_size,
                                              Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                QPixmapCache.insert(cache_key, scaled_pixmap)
                pixmap = scaled_pixmap

            # 创建最终带圆形遮罩的图片
            final_pixmap = QPixmap(avatar_size, avatar_size)
            final_pixmap.fill(Qt.GlobalColor.transparent)

            with QPainter(final_pixmap) as painter:
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)

                # 先设置圆形裁剪区域
                path = QPainterPath()
                path.addEllipse(0, 0, avatar_size, avatar_size)
                painter.setClipPath(path)

                # 然后在裁剪区域内绘制图片
                x = (avatar_size - pixmap.width()) // 2
                y = (avatar_size - pixmap.height()) // 2
                painter.drawPixmap(x, y, pixmap)

            QPixmapCache.insert(final_cache_key, final_pixmap)

        avatar.setPixmap(final_pixmap)
        logger.success(f"显示头像 {file_path}。")
        avatar.setStyleSheet(f'border-radius: {avatar_size // 2}px; background-color: transparent;')

    def mouseReleaseEvent(self, event: QMouseEvent):
        screen = QApplication.screenAt(event.globalPosition().toPoint())
        if not screen:
            screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        edge_distance = int(conf.get_ini('UI', 'edge_distance'))
        hidden_width = int(conf.get_ini('UI', 'hidden_width'))
        window_geometry = self.geometry()
        if event.button() == Qt.MouseButton.LeftButton and conf.get_ini('UI',
                                                                        'edge_hide') == 'true' and self.r_Position is not None:
            # 检测是否靠近屏幕边缘
            if window_geometry.left() < screen_geometry.left() + edge_distance:
                # 靠左边缘
                self.animation = QPropertyAnimation(self, b"geometry")
                elastic_enabled = conf.get_ini('UI', 'elastic_animation') == 'true'
                if elastic_enabled:
                    self.animation.setDuration(300)
                    self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
                else:
                    self.animation.setDuration(150)
                    self.animation.setEasingCurve(QEasingCurve.Type.Linear)
                logger.debug(
                    f'弹性动画状态: {elastic_enabled}, 持续时间: {self.animation.duration()}ms, 缓动曲线: {self.animation.easingCurve().type()}')
                self.animation.setStartValue(window_geometry)
                window_geometry.moveRight(screen_geometry.left() + hidden_width)
                self.animation.setEndValue(window_geometry)
                self.animation.start()
                logger.info('窗口贴靠到左边缘')
            elif window_geometry.right() > screen_geometry.right() - edge_distance:
                # 靠右边缘
                self.animation = QPropertyAnimation(self, b"geometry")
                elastic_enabled = conf.get_ini('UI', 'elastic_animation') == 'true'
                if elastic_enabled:
                    self.animation.setDuration(300)
                    self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
                else:
                    self.animation.setDuration(150)
                    self.animation.setEasingCurve(QEasingCurve.Type.Linear)
                logger.debug(
                    f'弹性动画状态: {elastic_enabled}, 持续时间: {self.animation.duration()}ms, 缓动曲线: {self.animation.easingCurve().type()}')
                self.animation.setStartValue(window_geometry)
                window_geometry.moveLeft(screen_geometry.right() - hidden_width)
                self.animation.setEndValue(window_geometry)
                self.animation.start()
                logger.info('窗口贴靠到右边缘。')
            elif window_geometry.top() < screen_geometry.top() + edge_distance:
                # 靠上边缘
                self.animation = QPropertyAnimation(self, b"geometry")
                elastic_enabled = conf.get_ini('UI', 'elastic_animation') == 'true'
                if elastic_enabled:
                    self.animation.setDuration(300)
                    self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
                else:
                    self.animation.setDuration(150)
                    self.animation.setEasingCurve(QEasingCurve.Type.Linear)
                logger.debug(
                    f'弹性动画状态: {elastic_enabled}, 持续时间: {self.animation.duration()}ms, 缓动曲线: {self.animation.easingCurve().type()}')
                self.animation.setStartValue(window_geometry)
                window_geometry.moveTop(screen_geometry.top() + edge_distance)
                self.animation.setEndValue(window_geometry)
                self.animation.start()
                logger.info('窗口调整到屏幕顶部内。')
            elif window_geometry.bottom() > screen_geometry.bottom() - edge_distance:
                # 靠下边缘
                self.animation = QPropertyAnimation(self, b"geometry")
                elastic_enabled = conf.get_ini('UI', 'elastic_animation') == 'true'
                if elastic_enabled:
                    self.animation.setDuration(300)
                    self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
                else:
                    self.animation.setDuration(150)
                    self.animation.setEasingCurve(QEasingCurve.Type.Linear)
                logger.debug(
                    f'弹性动画状态: {elastic_enabled}, 持续时间: {self.animation.duration()}ms, 缓动曲线: {self.animation.easingCurve().type()}')
                self.animation.setStartValue(window_geometry)
                window_geometry.moveBottom(screen_geometry.bottom() - edge_distance)
                self.animation.setEndValue(window_geometry)
                self.animation.start()
                logger.info('窗口调整到屏幕底部内。')

        event.accept()

    def closeEvent(self, a0):
        global last_result, last_pos
        self.systemTrayIcon.hide()
        self.systemTrayIcon.deleteLater()
        last_result = self.student
        last_pos = self.pos()
        conf.write_ini('Last', 'x', last_pos.x(),
                       'Last', 'y', last_pos.y())


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
            Action(fIcon.SYNC, '重新启动', triggered=lambda: restart()),  # 添加重启选项
            Action(fIcon.CLOSE, '关闭', triggered=lambda: stop()),
        ])
        self.setContextMenu(self.menu)


def reload_widget():
    global widget
    if widget is None:
        return
    if widget.isVisible():
        widget.close()
    logger.debug("重载浮窗")
    init()


def init():
    global widget
    widget = Widget()
    widget.show()
    widget.raise_()


def stop():
    global widget
    if widget.isVisible():
        widget.close()
    sys.exit()


if __name__ == "__main__":
    os.environ['QT_SCALE_FACTOR'] = str(float(conf.get_ini('General', 'scale')))
    app = QApplication(sys.argv)
    logger.info(f"RandPicker 启动。缩放系数 {os.environ['QT_SCALE_FACTOR']}。")
    if share.isAttached():
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
    share.create(1)
    logger.info("欢迎。")
    conf.check_config()
    init()

    app.setQuitOnLastWindowClosed(False)

    sys.exit(app.exec())
