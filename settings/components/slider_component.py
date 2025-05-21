"""RandPicker 滑块组件。

此模块提供滑块组件的实现，主要用于权重设置。
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import Slider, BodyLabel


def create_weight_slider_widget(initial_value=1):
    """创建权重滑块组件
    
    :param initial_value: 初始权重值，默认为1
    :return: 包含滑块和标签的组件
    """
    # 初始化 slider
    slider_weight = Slider(Qt.Orientation.Horizontal)
    slider_weight.setObjectName('slider_weight')
    slider_weight.setSingleStep(1)
    slider_weight.setPageStep(1)
    slider_weight.setRange(1, 50)
    slider_weight.setValue(initial_value)
    slider_weight.setTracking(True)

    # 初始化提示
    tip = BodyLabel()
    tip.setText(str(slider_weight.value()))
    tip.setFixedWidth(47)
    slider_weight.valueChanged.connect(lambda value, t=tip, s=slider_weight: t.setText(str(value)))

    # 初始化布局
    layout_weight = QHBoxLayout()
    layout_weight.setSpacing(3)
    layout_weight.setContentsMargins(12, 0, 0, 0)
    layout_weight.addWidget(slider_weight)
    layout_weight.addWidget(tip)

    # 初始化组件
    widget_weight = QWidget()
    widget_weight.setLayout(layout_weight)
    
    return widget_weight