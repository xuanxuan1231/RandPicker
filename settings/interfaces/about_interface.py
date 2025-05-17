"""RandPicker 关于界面。

此模块提供关于界面的实现。
"""
import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import PushButton, BodyLabel

from .base_interface import SettingsInterface


def setup_about_interface(window):
    """设置关于页面
    
    :param window: 设置窗口实例
    """
    btn_github = window.findChild(PushButton, 'btn_github')
    btn_github.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://github.com/xuanxuan1231/RandPicker')))

    btn_license = window.findChild(PushButton, 'btn_license')
    btn_license.clicked.connect(
        lambda: QDesktopServices.openUrl(QUrl('https://github.com/xuanxuan1231/RandPicker/blob/main/LICENSE')))