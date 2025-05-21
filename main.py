"""
RandPicker 主程序 (LTS版本)。

此版本专注于稳定性和可靠性，适合长期支持使用。
"""

import os
import random
import sys
from random import choices
from typing import override

from PyQt6 import uic
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QLocale
from PyQt6.QtGui import QColor, QMouseEvent, QIcon, QPixmap, QPainter, QPainterPath, QPixmapCache
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGraphicsDropShadowEffect, QSystemTrayIcon, QFrame, QLayout
from loguru import logger
from qfluentwidgets import PushButton, SystemTrayMenu, FluentIcon as fIcon, Action, Dialog, PrimaryPushButton, \
    isDarkTheme, setTheme, Theme, qconfig, PixmapLabel, FluentTranslator, setThemeColor, SystemThemeListener

import conf
from settings import open_settings, share, restart
from settings.interfaces.history_interface import add_history_entry
from datetime import datetime

# 适配高DPI缩放
QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

# 建立几个空的全局变量
widget = None
last_result = {}
last_pos = QPoint()

# 记录日志
# LTS版本使用更可靠的日志配置，增加保留时间和错误捕获
try:
    # 确保日志目录存在
    os.makedirs("./log", exist_ok=True)
    logger.add("./log/RandPicker_{time}.log", 
              rotation="1 MB", 
              encoding="utf-8", 
              retention="7 days",
              backtrace=True, 
              diagnose=True,
              catch=True)
    logger.info("LTS版本日志系统初始化成功")
except Exception as e:
    print(f"日志系统初始化失败: {e}")

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
        self.is_avatar = False
        self.animation = None
        self.student = last_result
        self.init_ui()
        self.setWindowIcon(QIcon('./img/Logo.png'))
        self.systemTrayIcon = SystemTrayIcon(parent=self)
        self.systemTrayIcon.show()
        self.themeListener = SystemThemeListener(self)
        self.themeListener.start()

    def init_ui(self):
        global last_pos
        self.is_avatar = True if conf.ini.get('UI', 'avatar') == 'true' else False

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
        elif conf.ini.get('Last', 'x') and conf.ini.get('Last', 'y'):
            x = int(conf.ini.get('Last', 'x'))
            y = int(conf.ini.get('Last', 'y'))
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

        btn_person = self.findChild(PrimaryPushButton, 'btn_person')
        btn_person.clicked.connect(lambda: self.pick_person())

        btn_group = self.findChild(PushButton, 'btn_group')
        btn_group.clicked.connect(lambda: self.pick_group())

        self.clear()

    @override
    def mousePressEvent(self, event: QMouseEvent):
        edge_distance = int(conf.ini.get('UI', 'edge_distance'))
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

    @override
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            if self.m_Position is not None:
                self.move(event.globalPosition().toPoint() - self.m_Position)  # 更改窗口位置
                self.r_Position = event.globalPosition().toPoint()  # 记录鼠标释放位置
                event.accept()

    def pick_person(self):
        """
        随机选人。
        
        LTS版本增强了错误处理和边缘情况处理。
        """
        try:
            students = []

            if conf.ini.get('Group', 'global') == 'true' or conf.ini.get('Group', 'group') == '':
                logger.debug('使用全局分组。')
                students = conf.stu.get_active_index()
            else:
                group_str = conf.ini.get('Group', 'groups')
                if group_str and group_str.strip():
                    groups = group_str.split(', ')
                    logger.debug(f'使用分组 {groups}。')
                    for group in groups:
                        try:
                            group_index = int(group)
                            students.extend(conf.group.get_stu_index(group_index))
                        except (ValueError, TypeError) as e:
                            logger.error(f'分组转换错误: {e}，跳过此分组')
                else:
                    logger.warning('分组字符串为空，使用全局分组')
                    students = conf.stu.get_active_index()
            
            name = self.findChild(QLabel, 'name')
            id_ = self.findChild(QLabel, 'id')

            if not students:
                logger.warning('没有可用的学生数据')
                name.setText('无结果')
                id_.setText('000000')
                if self.is_avatar:
                    self.show_avatar()
                return

            # 确保权重列表长度与学生列表一致
            weights = conf.stu.get_weight(students)
            if len(weights) != len(students):
                logger.error(f'权重列表长度({len(weights)})与学生列表长度({len(students)})不匹配，使用均等权重')
                weights = [1] * len(students)
            
            # 安全地选择学生
            try:
                num = choices(students, weights=weights, k=1)[0]
                logger.info(f'随机数已生成。JSON 索引是 {num}。它的选择权重是 {conf.stu.get_all_weight()[num]}。')
                self.student = conf.stu.get_single(num)
                logger.debug(f'已获取 JSON 索引是 {num} 的学生信息。{self.student}')
                
                # 确保学生数据完整
                if not self.student or 'name' not in self.student or 'id' not in self.student:
                    logger.error(f'学生数据不完整: {self.student}')
                    name.setText('数据错误')
                    id_.setText('000000')
                    if self.is_avatar:
                        self.show_avatar()
                    return
                
                name.setText(f'{str(self.student["id"])[-2:]} {self.student["name"]}')
                id_.setText(str(self.student["id"]))

                if self.is_avatar:
                    # 设置头像
                    avatar_path = None
                    # 尝试不同的图片格式
                    for ext in ['png', 'jpg', 'jpeg']:
                        temp_path = f'./img/stu/{self.student["id"]}.{ext}'
                        if os.path.exists(temp_path):
                            avatar_path = temp_path
                            logger.success(f"找到了学生 {self.student["id"]} 的头像 {self.student["id"]}.{ext}。")
                            break
                    self.student['avatar'] = avatar_path
                    self.show_avatar(avatar_path)

                # 记录历史
                try:
                    add_history_entry({'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                                      'type': 'person', 
                                      'result': f'{self.student["id"]} {self.student["name"]}'})
                except Exception as e:
                    logger.error(f'记录历史失败: {e}')
            except IndexError:
                logger.error('选择学生时发生索引错误，可能是空列表或权重问题')
                name.setText('选择错误')
                id_.setText('000000')
                if self.is_avatar:
                    self.show_avatar()
        except Exception as e:
            logger.exception(f'随机选人过程中发生错误: {e}')
            name = self.findChild(QLabel, 'name')
            id_ = self.findChild(QLabel, 'id')
            if name and id_:
                name.setText('系统错误')
                id_.setText('000000')
            if self.is_avatar:
                self.show_avatar()

    def clear(self):
        global last_result
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

    def pick_group(self):
        """
        随机选小组。
        
        LTS版本增强了错误处理和边缘情况处理。
        """
        try:
            # 获取所有小组
            all_groups = conf.group.get_all()
            groups = len(all_groups)
            
            if groups < 1:
                logger.warning('没有可用的小组数据，切换到选人模式')
                self.pick_person()
                return
                
            # 安全地生成随机数
            try:
                num = random.randint(0, groups - 1)
                logger.debug(f'随机数已生成。小组的 JSON 索引是 {num}。')
                
                # 获取小组信息
                group = conf.group.get_single(num)
                if not group or 'name' not in group:
                    logger.error(f'小组数据不完整: {group}')
                    name = self.findChild(QLabel, 'name')
                    id_ = self.findChild(QLabel, 'id')
                    if name and id_:
                        name.setText('小组数据错误')
                        id_.setText('请检查小组配置')
                    if self.is_avatar:
                        self.show_avatar()
                    return
                    
                logger.debug(f'已获取 JSON 索引是 {num} 的小组信息。{group}')
                
                # 获取小组成员名称
                try:
                    student_names = conf.group.get_stu_name(group)
                    students = ', '.join(student_names) if student_names else '(空小组)'
                except Exception as e:
                    logger.error(f'获取小组成员名称失败: {e}')
                    students = '(获取成员失败)'
                
                # 更新UI
                name = self.findChild(QLabel, 'name')
                id_ = self.findChild(QLabel, 'id')
                if name and id_:
                    logger.debug(f"信息已解析。名称：{group['name']}；学生：{students}。")
                    name.setText(group['name'])
                    id_.setText(students)
                
                if self.is_avatar:
                    self.show_avatar()

                # 记录历史
                try:
                    add_history_entry({'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                                      'type': 'group', 
                                      'result': f'{group["name"]} ({students})'})
                except Exception as e:
                    logger.error(f'记录历史失败: {e}')
                    
            except ValueError as e:
                logger.error(f'生成随机数时发生错误: {e}')
                name = self.findChild(QLabel, 'name')
                id_ = self.findChild(QLabel, 'id')
                if name and id_:
                    name.setText('随机选择错误')
                    id_.setText('请检查小组配置')
                if self.is_avatar:
                    self.show_avatar()
                    
        except Exception as e:
            logger.exception(f'随机选组过程中发生错误: {e}')
            name = self.findChild(QLabel, 'name')
            id_ = self.findChild(QLabel, 'id')
            if name and id_:
                name.setText('系统错误')
                id_.setText('请检查日志')
            if self.is_avatar:
                self.show_avatar()

    def show_avatar(self, file_path='./img/stu/default.jpeg'):
        """
        显示头像
        
        LTS版本增强了错误处理和资源管理
        """
        try:
            avatar = self.findChild(PixmapLabel, 'avatar')
            if not avatar:
                logger.error('未找到头像控件')
                return
                
            # 安全地获取头像大小
            try:
                avatar_size = int(conf.ini.get('UI', 'avatar_size'))
                if avatar_size <= 0:
                    logger.warning(f'头像大小配置异常: {avatar_size}，使用默认值60')
                    avatar_size = 60
            except (ValueError, TypeError) as e:
                logger.error(f'头像大小配置错误: {e}，使用默认值60')
                avatar_size = 60
            
            # 检查文件路径
            if file_path is not None and os.path.exists(file_path):
                # 文件路径有效，不需要修改
                pass
            elif os.path.exists('./img/stu/default.jpeg'):
                logger.warning(f"没有找到头像 {file_path}。使用默认头像。")
                file_path = './img/stu/default.jpeg'
            else:
                logger.warning(f"没有找到头像 {file_path} 和默认头像。使用空白。")
                avatar.setPixmap(QPixmap())
                avatar.setStyleSheet(f'border-radius: {avatar_size // 2}px; background-color: transparent;')
                return

            # 使用复合缓存键，避免重复创建
            try:
                final_cache_key = f"final_{file_path}_{avatar_size}"
                final_pixmap = QPixmapCache.find(final_cache_key)

                if not final_pixmap:
                    # 原始图片缓存
                    cache_key = f"{file_path}_{avatar_size}"
                    pixmap = QPixmapCache.find(cache_key)
                    
                    if not pixmap:
                        # 加载并缩放图片
                        try:
                            pixmap = QPixmap(file_path)
                            if pixmap.isNull():
                                logger.error(f'无法加载图片: {file_path}')
                                avatar.setPixmap(QPixmap())
                                avatar.setStyleSheet(f'border-radius: {avatar_size // 2}px; background-color: transparent;')
                                return
                                
                            scaled_pixmap = pixmap.scaled(avatar_size, avatar_size,
                                                        Qt.AspectRatioMode.KeepAspectRatio,
                                                        Qt.TransformationMode.SmoothTransformation)
                            QPixmapCache.insert(cache_key, scaled_pixmap)
                            pixmap = scaled_pixmap
                        except Exception as e:
                            logger.error(f'图片处理错误: {e}')
                            avatar.setPixmap(QPixmap())
                            avatar.setStyleSheet(f'border-radius: {avatar_size // 2}px; background-color: transparent;')
                            return

                    # 创建最终带圆形遮罩的图片
                    final_pixmap = QPixmap(avatar_size, avatar_size)
                    final_pixmap.fill(Qt.GlobalColor.transparent)

                    try:
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
                    except Exception as e:
                        logger.error(f'绘制圆形头像错误: {e}')
                        avatar.setPixmap(pixmap)  # 退回到使用原始图片
                        avatar.setStyleSheet(f'border-radius: {avatar_size // 2}px; background-color: transparent;')
                        return

                    QPixmapCache.insert(final_cache_key, final_pixmap)

                avatar.setPixmap(final_pixmap)
                logger.success(f"显示头像 {file_path}。")
                avatar.setStyleSheet(f'border-radius: {avatar_size // 2}px; background-color: transparent;')
            except Exception as e:
                logger.error(f'缓存处理错误: {e}')
                # 尝试直接设置图片作为备选方案
                try:
                    direct_pixmap = QPixmap(file_path)
                    if not direct_pixmap.isNull():
                        avatar.setPixmap(direct_pixmap.scaled(avatar_size, avatar_size))
                        avatar.setStyleSheet(f'border-radius: {avatar_size // 2}px; background-color: transparent;')
                    else:
                        avatar.setPixmap(QPixmap())
                        avatar.setStyleSheet(f'border-radius: {avatar_size // 2}px; background-color: transparent;')
                except:
                    avatar.setPixmap(QPixmap())
                    avatar.setStyleSheet(f'border-radius: {avatar_size // 2}px; background-color: transparent;')
        except Exception as e:
            logger.exception(f'显示头像过程中发生错误: {e}')
            # 尝试重置头像控件
            try:
                avatar = self.findChild(PixmapLabel, 'avatar')
                if avatar:
                    avatar.setPixmap(QPixmap())
                    avatar.setStyleSheet('background-color: transparent;')
            except:
                pass

    @override
    def mouseReleaseEvent(self, event: QMouseEvent):
        screen = QApplication.screenAt(event.globalPosition().toPoint())
        if not screen:
            screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        edge_distance = int(conf.ini.get('UI', 'edge_distance'))
        hidden_width = int(conf.ini.get('UI', 'hidden_width'))
        window_geometry = self.geometry()
        if event.button() == Qt.MouseButton.LeftButton and conf.ini.get('UI',
                                                                        'edge_hide') == 'true' and self.r_Position is not None:
            # 检测是否靠近屏幕边缘
            if window_geometry.left() < screen_geometry.left() + edge_distance:
                # 靠左边缘
                self.animation = QPropertyAnimation(self, b"geometry")
                elastic_enabled = conf.ini.get('UI', 'elastic_animation') == 'true'
                if elastic_enabled:
                    self.animation.setDuration(300)
                    self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
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
                elastic_enabled = conf.ini.get('UI', 'elastic_animation') == 'true'
                if elastic_enabled:
                    self.animation.setDuration(300)
                    self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
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
                elastic_enabled = conf.ini.get('UI', 'elastic_animation') == 'true'
                if elastic_enabled:
                    self.animation.setDuration(300)
                    self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
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
                elastic_enabled = conf.ini.get('UI', 'elastic_animation') == 'true'
                if elastic_enabled:
                    self.animation.setDuration(300)
                    self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
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

    @override
    def closeEvent(self, e):
        global last_result, last_pos
        self.systemTrayIcon.hide()
        self.systemTrayIcon.deleteLater()
        last_result = self.student
        last_pos = self.pos()
        conf.ini.write('Last', 'x', last_pos.x(),
                       'Last', 'y', last_pos.y())
        self.themeListener.terminate()
        self.themeListener.deleteLater()
        super().closeEvent(e)


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
    if isDarkTheme():
        setThemeColor(conf.ini.get('Color', 'dark'))
    else:
        setThemeColor(conf.ini.get('Color', 'light'))
    widget.show()
    widget.raise_()


def stop():
    global widget
    if widget.isVisible():
        widget.close()
    sys.exit()


if __name__ == "__main__":
    # LTS版本增强了启动过程的错误处理和资源管理
    try:
        # 确保配置目录存在
        os.makedirs("./img/stu", exist_ok=True)
        
        # 安全地获取缩放系数
        try:
            scale_factor = float(conf.ini.get('General', 'scale'))
            if scale_factor <= 0:
                logger.warning(f'缩放系数异常: {scale_factor}，使用默认值1.0')
                scale_factor = 1.0
        except (ValueError, TypeError) as e:
            logger.error(f'缩放系数配置错误: {e}，使用默认值1.0')
            scale_factor = 1.0
            
        os.environ['QT_SCALE_FACTOR'] = str(scale_factor)
        
        # 初始化应用
        app = QApplication(sys.argv)
        translator = FluentTranslator(QLocale(QLocale.Language.Chinese, QLocale.Country.China))
        app.installTranslator(translator)
        logger.info(f"RandPicker LTS版本启动。缩放系数 {os.environ['QT_SCALE_FACTOR']}。")
        
        # 检查是否已有实例运行
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
            
        # 创建共享内存
        try:
            share.create(1)
        except Exception as e:
            logger.error(f"创建共享内存失败: {e}")
            msg_box = Dialog(
                'RandPicker 启动错误',
                f'创建共享内存失败: {e}\n请尝试重新启动应用。'
            )
            msg_box.yesButton.setText('退出')
            msg_box.cancelButton.hide()
            msg_box.exec()
            sys.exit(-1)
            
        logger.info("欢迎使用RandPicker LTS版本。")
        
        # 设置主题
        try:
            theme_setting = conf.ini.get('General', 'theme')
            if theme_setting == '0':
                setTheme(Theme.LIGHT)
            elif theme_setting == '1':
                setTheme(Theme.DARK)
            else:
                setTheme(Theme.AUTO)
        except Exception as e:
            logger.error(f"设置主题失败: {e}，使用默认主题")
            setTheme(Theme.AUTO)
            
        # 初始化主窗口
        init()
        
        # LTS版本移除测试代码
        # open_settings()  # 移除直接打开设置窗口的测试代码

        app.setQuitOnLastWindowClosed(False)
        sys.exit(app.exec())
        
    except Exception as e:
        # 捕获所有未处理的异常
        error_msg = f"启动过程中发生严重错误: {e}"
        print(error_msg)
        try:
            logger.exception(error_msg)
            # 尝试显示错误对话框
            app = QApplication.instance()
            if not app:
                app = QApplication(sys.argv)
            msg_box = Dialog(
                'RandPicker 启动失败',
                f'启动过程中发生严重错误:\n{e}\n\n请查看日志获取详细信息。'
            )
            msg_box.yesButton.setText('退出')
            msg_box.cancelButton.hide()
            msg_box.exec()
        except:
            pass
        sys.exit(-1)

