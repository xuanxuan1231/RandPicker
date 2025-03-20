import sys
from random import randint as rand

from PyQt6 import uic
from PyQt6.QtCore import Qt, QRect, QPoint, QSize, QTimer, QPropertyAnimation, QEasingCurve, QVariantAnimation
from PyQt6.QtGui import QColor, QMouseEvent, QCursor
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGraphicsDropShadowEffect, QSystemTrayIcon, QFrame, QGraphicsBlurEffect
from qfluentwidgets import PushButton, SystemTrayMenu, FluentIcon as fIcon, Action

import conf

excluded_number = []

class Widget(QWidget):
    """
    主浮窗。
    """
    def __init__(self):
        super().__init__()
        self.m_Position = None
        self.p_Position = None
        self.r_Position = None
        # 窗口状态相关属性
        self.is_collapsed = False  # 是否已收起
        self.collapse_edge = None  # 收起的边缘：'left', 'right', 'top', 'bottom'
        self.normal_geometry = None  # 正常状态下的几何信息
        self.collapsed_geometry = None  # 收起状态下的几何信息
        self.edge_distance_threshold = 20  # 边缘检测阈值（像素）
        self.collapse_timer = QTimer(self)  # 用于延迟收起窗口
        self.collapse_timer.setSingleShot(True)
        self.collapse_timer.timeout.connect(self.collapse_window)
        # 添加自动收回计时器
        self.auto_collapse_timer = QTimer(self)
        self.auto_collapse_timer.setSingleShot(True)
        self.auto_collapse_timer.timeout.connect(self.collapse_window)
        
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
        elif sys.platform == 'win32':
            # 针对Windows平台的特殊处理，确保在Windows 11上也能正确显示
            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint |
                Qt.WindowType.SubWindow | Qt.WindowType.Tool
            )
            # 确保窗口始终置顶
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
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

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            # 如果窗口处于收起状态，则展开窗口
            if self.is_collapsed:
                # 立即展开窗口，无需拖动
                self.expand_window()
                event.accept()
                return
            
            self.m_Position = event.globalPosition().toPoint() - self.pos()  # 获取鼠标相对窗口的位置
            self.p_Position = event.globalPosition().toPoint()  # 获取鼠标相对屏幕的位置
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            # 如果窗口处于收起状态，则先恢复窗口
            if self.is_collapsed:
                self.expand_window()
            
            # 更改窗口位置
            self.move(event.globalPosition().toPoint() - self.m_Position)
            event.accept()

    def mouseReleaseEvent(self, event):
        # 检测窗口是否靠近屏幕边缘
        if not self.is_collapsed and event.button() == Qt.MouseButton.LeftButton:
            self.check_edge_proximity()
        event.accept()
        
    def check_edge_proximity(self):
        """检测窗口是否靠近屏幕边缘"""
        # 获取屏幕尺寸
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        
        # 获取窗口位置
        window_rect = self.geometry()
        
        # 检测是否靠近各个边缘
        distance_to_left = window_rect.left()
        distance_to_right = screen_rect.right() - window_rect.right()
        distance_to_top = window_rect.top()
        distance_to_bottom = screen_rect.bottom() - window_rect.bottom()
        
        # 保存当前几何信息，用于恢复窗口
        self.normal_geometry = self.geometry()
        
        # 判断最近的边缘
        min_distance = min(distance_to_left, distance_to_right, distance_to_top, distance_to_bottom)
        
        # 如果靠近边缘，则准备收起窗口
        if min_distance < self.edge_distance_threshold:
            if min_distance == distance_to_left:
                self.collapse_edge = 'left'
            elif min_distance == distance_to_right:
                self.collapse_edge = 'right'
            elif min_distance == distance_to_top:
                self.collapse_edge = 'top'
            else:  # distance_to_bottom
                self.collapse_edge = 'bottom'
            
            # 启动定时器，延迟收起窗口（避免误触发）
            self.collapse_timer.start(300)
    
    def collapse_window(self):
        """收起窗口，只显示一个圆角矩形提示条，且只露出一半，带动画效果"""
        if self.is_collapsed:
            return
            
        # 停止自动收回计时器（如果正在运行）
        if self.auto_collapse_timer.isActive():
            self.auto_collapse_timer.stop()
            
        # 获取屏幕尺寸
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        
        # 保存当前几何信息，用于动画起始位置
        start_geometry = self.geometry()
        
        # 计算收起后的窗口位置和大小
        # 修改为更宽的提示条，使其看起来像圆角矩形
        collapsed_width = 40  # 收起后的宽度，增加宽度使其更容易被点击
        collapsed_height = 80  # 收起后的高度，减小高度使其更像一个圆角矩形
        
        # 计算水平收起位置
        if self.collapse_edge == 'left':
            # 水平收起，只露出右侧边缘
            collapsed_rect = QRect(-collapsed_width + 10, self.normal_geometry.center().y() - collapsed_height // 2, 
                                  collapsed_width, collapsed_height)
        elif self.collapse_edge == 'right':
            # 水平收起，只露出左侧边缘
            collapsed_rect = QRect(screen_rect.width() - 10, 
                                  self.normal_geometry.center().y() - collapsed_height // 2,
                                  collapsed_width, collapsed_height)
        elif self.collapse_edge == 'top':
            # 水平收起，只露出底部边缘
            collapsed_rect = QRect(self.normal_geometry.center().x() - collapsed_width // 2, 
                                  -collapsed_height + 10, collapsed_width, collapsed_height)
        else:  # bottom
            # 水平收起，只露出顶部边缘
            collapsed_rect = QRect(self.normal_geometry.center().x() - collapsed_width // 2, 
                                  screen_rect.height() - 10,
                                  collapsed_width, collapsed_height)
        
        # 保存收起状态的几何信息
        self.collapsed_geometry = collapsed_rect
        
        # 创建动画效果
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)  # 动画持续时间（毫秒）
        self.animation.setStartValue(start_geometry)
        self.animation.setEndValue(collapsed_rect)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)  # 缓动曲线
        
        # 设置窗口为收起状态
        self.is_collapsed = True
        
        # 隐藏主要内容，只显示一个圆角矩形提示条
        background = self.findChild(QFrame, 'backgnd')
        if background:
            # 使用与主窗口相同的颜色，但添加半透明和模糊效果
            # 创建颜色动画 - 云母效果
            self.color_animation = QVariantAnimation()
            self.color_animation.setDuration(300)  # 动画持续时间（毫秒）
            self.color_animation.setStartValue(QColor(245, 245, 250, 255))  # 微调颜色，增加一点蓝色调
            self.color_animation.setEndValue(QColor(245, 245, 250, 210))  # 增加透明度以展现云母效果
            self.color_animation.valueChanged.connect(lambda color: self.update_background_color(background, color))
            self.color_animation.start()
            
            # 设置模糊效果 - 减小模糊半径以提高清晰度
            blur_effect = QGraphicsBlurEffect()
            blur_effect.setBlurRadius(3)  # 减小模糊半径，提高清晰度
            background.setGraphicsEffect(blur_effect)
        
        # 启动动画
        self.animation.start()
        
    def update_background_color(self, background, color):
        """更新背景颜色"""
        # 云母效果：微弱彩虹色调的半透明效果，边框更亮
        background.setStyleSheet(f"background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()}); \
                                 border-radius: 12px; \
                                 border: 1px solid rgba(255, 255, 255, 180); \
                                 background-image: linear-gradient(135deg, \
                                    rgba(255, 255, 255, 0.1), \
                                    rgba(255, 255, 255, 0.05) 25%, \
                                    rgba(255, 255, 255, 0.15) 50%, \
                                    rgba(255, 255, 255, 0.05) 75%, \
                                    rgba(255, 255, 255, 0.1));")
    
    def expand_window(self):
        """展开窗口到正常状态，带动画效果"""
        if not self.is_collapsed:
            return
            
        # 保存收起状态的几何信息，用于动画起始位置
        start_geometry = self.geometry()
        
        # 调整展开后的位置，避免再次被识别为靠近边缘
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        adjusted_geometry = QRect(self.normal_geometry)
        
        # 根据收起的边缘，将窗口向屏幕中心方向移动一定距离
        offset = 30  # 移动的像素距离
        if self.collapse_edge == 'left':
            adjusted_geometry.moveLeft(self.normal_geometry.left() + offset)
        elif self.collapse_edge == 'right':
            adjusted_geometry.moveLeft(self.normal_geometry.left() - offset)
        elif self.collapse_edge == 'top':
            adjusted_geometry.moveTop(self.normal_geometry.top() + offset)
        elif self.collapse_edge == 'bottom':
            adjusted_geometry.moveTop(self.normal_geometry.top() - offset)
            
        # 确保窗口不会超出屏幕范围
        if adjusted_geometry.left() < 0:
            adjusted_geometry.moveLeft(0)
        if adjusted_geometry.right() > screen_rect.width():
            adjusted_geometry.moveRight(screen_rect.width())
        if adjusted_geometry.top() < 0:
            adjusted_geometry.moveTop(0)
        if adjusted_geometry.bottom() > screen_rect.height():
            adjusted_geometry.moveBottom(screen_rect.height())
            
        # 更新正常状态的几何信息
        self.normal_geometry = adjusted_geometry
        
        # 创建动画效果
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)  # 动画持续时间（毫秒）
        self.animation.setStartValue(start_geometry)
        self.animation.setEndValue(adjusted_geometry)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)  # 缓动曲线
        
        # 设置窗口为非收起状态
        self.is_collapsed = False
        
        # 恢复背景样式，添加毛玻璃效果
        background = self.findChild(QFrame, 'backgnd')
        if background:
            # 云母效果：微弱彩虹色调的半透明效果
            background.setStyleSheet("background-color: rgba(245, 245, 250, 230); \
                                    border-radius: 8px; \
                                    border: 1px solid rgba(255, 255, 255, 180); \
                                    background-image: linear-gradient(135deg, \
                                        rgba(255, 255, 255, 0.1), \
                                        rgba(255, 255, 255, 0.05) 25%, \
                                        rgba(255, 255, 255, 0.15) 50%, \
                                        rgba(255, 255, 255, 0.05) 75%, \
                                        rgba(255, 255, 255, 0.1));")
            
            # 添加模糊效果 - 减小模糊半径以提高清晰度
            blur_effect = QGraphicsBlurEffect()
            blur_effect.setBlurRadius(5)  # 减小模糊半径，提高清晰度
            background.setGraphicsEffect(blur_effect)
            
            # 恢复阴影效果
            QTimer.singleShot(300, lambda: self.restore_shadow_effect(background))
        
        # 启动动画
        self.animation.start()
        
        # 不再自动收回窗口，除非用户主动触发或靠近屏幕边缘
        # self.auto_collapse_timer.start(15000)
        
    def restore_shadow_effect(self, background):
        """恢复阴影效果 - 云母效果专用"""
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(24)  # 稍微减小模糊半径
        shadow_effect.setXOffset(0)
        shadow_effect.setYOffset(5)  # 稍微减小阴影偏移
        shadow_effect.setColor(QColor(0, 0, 0, 65))  # 减小阴影不透明度，使其更轻盈
        background.setGraphicsEffect(shadow_effect)
    
    def mouseDoubleClickEvent(self, event):
        """双击事件处理"""
        if self.is_collapsed:
            self.expand_window()
        event.accept()
        
    def pick(self):
        """
        随机选人。
        """
        num = rand(1, conf.get_students_num())
        while num in excluded_number:
            num = rand(1, conf.get_students_num())
        student = conf.get_with_short_id(num)
        name = self.findChild(QLabel, 'name')
        id_ = self.findChild(QLabel, 'id')
        
        # 添加错误处理，确保student不为None
        if student is None:
            name.setText(f'{num} 未找到学生信息')
            id_.setText('N/A')
            return
            
        name.setText(f'{num} {student["name"]}')
        id_.setText(student["id"])

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
    # 确保窗口置顶显示
    widget.raise_()
    widget.activateWindow()
    # 在Windows平台上额外调用setWindowState确保窗口正确显示
    if sys.platform == 'win32':
        widget.setWindowState(widget.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
    sys.exit(app.exec())
