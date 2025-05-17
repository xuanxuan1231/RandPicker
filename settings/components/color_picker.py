"""RandPicker 颜色选择器组件。

此模块提供颜色选择器组件的实现，用于主题颜色设置。
"""
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import ColorDialog, BodyLabel


def create_color_dialog(window, current_color_label):
    """创建颜色选择对话框
    
    :param window: 父窗口
    :param current_color_label: 当前颜色标签
    :return: 颜色对话框实例
    """
    current_color = QColor(current_color_label.text())
    dialog_color = ColorDialog(current_color, '选择主题颜色', window, enableAlpha=False)
    dialog_color.yesButton.setText('好')
    
    return dialog_color


def update_color_preview(color, label):
    """更新颜色预览
    
    :param color: 颜色对象
    :param label: 标签控件
    """
    label.setText(color.name())
    label.setStyleSheet(
        f"background-color: {color.name()}; color: {'white' if color.lightness() < 128 else 'black'}; padding: 2px; border-radius: 3px;")