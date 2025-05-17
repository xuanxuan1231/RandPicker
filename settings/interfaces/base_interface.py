"""RandPicker 设置界面基类。

此模块提供设置界面的基础类和通用方法。
"""
from PyQt6.QtWidgets import QWidget


class SettingsInterface:
    """
    设置界面基类，提供通用的设置界面方法。
    """
    
    @staticmethod
    def setup_interface(window: QWidget):
        """
        设置界面的基本方法，子类应该重写此方法。
        
        :param window: 设置窗口实例
        :type window: QWidget
        """
        raise NotImplementedError("子类必须实现setup_interface方法")