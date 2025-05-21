"""RandPicker 工具函数。

此模块提供设置模块中使用的通用工具函数。
"""
import os
import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QRect
from loguru import logger


def get_screen_info():
    """获取屏幕信息
    
    :return: 屏幕宽度、高度和DPI
    """
    screen = QApplication.primaryScreen()
    geometry = screen.geometry()
    dpi = screen.logicalDotsPerInch()
    
    return {
        'width': geometry.width(),
        'height': geometry.height(),
        'dpi': dpi
    }


def calculate_window_size(scale_factor=0.7):
    """计算窗口大小
    
    :param scale_factor: 相对于屏幕大小的比例因子
    :return: 窗口宽度和高度
    """
    screen_info = get_screen_info()
    width = int(screen_info['width'] * scale_factor)
    height = int(screen_info['height'] * scale_factor)
    
    return width, height


def center_window(window, width, height):
    """将窗口居中显示
    
    :param window: 窗口实例
    :param width: 窗口宽度
    :param height: 窗口高度
    """
    screen_info = get_screen_info()
    x = int(screen_info['width'] / 2 - width / 2)
    y = int(screen_info['height'] / 2 - height / 2)
    
    window.setGeometry(QRect(x, y, width, height))


def restart_application():
    """重启应用程序
    
    此函数会完全重启应用程序，保留命令行参数
    """
    logger.info("正在重启应用程序...")
    os.execl(sys.executable, sys.executable, *sys.argv)


def is_dark_color(color):
    """判断颜色是否为深色
    
    :param color: 颜色字符串，格式为 #RRGGBB
    :return: 是否为深色
    """
    # 移除可能的 # 前缀
    if color.startswith('#'):
        color = color[1:]
    
    # 将颜色转换为RGB值
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)
    
    # 计算亮度 (基于人眼对不同颜色的感知)
    # 公式: 0.299*R + 0.587*G + 0.114*B
    brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    
    # 亮度小于0.5认为是深色
    return brightness < 0.5