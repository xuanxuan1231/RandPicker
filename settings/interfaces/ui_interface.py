"""RandPicker 界面设置。

此模块提供界面设置功能的实现。
"""
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QScroller
from loguru import logger
from qfluentwidgets import Slider, SwitchButton, BodyLabel, PushButton, ComboBox, Flyout, InfoBarIcon, \
    FlyoutAnimationType, ColorDialog, setTheme, setThemeColor, isDarkTheme, Theme, SmoothScrollArea
from PyQt6.QtCore import Qt

import conf
from .base_interface import SettingsInterface


def setup_ui_interface(window):
    """设置界面设置页面
    
    :param window: 设置窗口实例
    """
    # 触摸屏适配
    scroll_area = window.findChild(SmoothScrollArea, 'wg_scroll')
    QScroller.grabGesture(scroll_area.viewport(), QScroller.ScrollerGestureType.LeftMouseButtonGesture)
    
    # 从配置文件加载设置
    avatar_size = int(conf.ini.get('UI', 'avatar_size'))
    edge_hide = conf.ini.get('UI', 'edge_hide') == 'true'
    edge_distance = int(conf.ini.get('UI', 'edge_distance'))
    hidden_width = int(conf.ini.get('UI', 'hidden_width'))
    avatar = conf.ini.get('UI', 'avatar') == 'true'
    scale = int(float(conf.ini.get('General', 'scale')) * 100)
    elastic_animation = conf.ini.get('UI', 'elastic_animation') == 'true'

    slider_avatar_size = window.findChild(Slider, 'avatar_size')
    label_avatar_size = window.findChild(BodyLabel, 'avatar_size_label')
    btn_edge_hide = window.findChild(SwitchButton, 'edge_hide')
    btn_avatar = window.findChild(SwitchButton, 'avatar')
    btn_elastic_animation = window.findChild(SwitchButton, 'elastic_animation')
    slider_edge_distance = window.findChild(Slider, 'edge_distance')
    label_edge_distance = window.findChild(BodyLabel, 'edge_distance_label')
    slider_hidden_width = window.findChild(Slider, 'hidden_width')
    label_hidden_width = window.findChild(BodyLabel, 'hidden_width_label')
    slider_scale = window.findChild(Slider, 'scale')
    label_scale = window.findChild(BodyLabel, 'scale_label')
    combo_theme = window.findChild(ComboBox, 'theme')
    btn_color = window.findChild(PushButton, 'color')
    label_color = window.findChild(BodyLabel, 'color_label')

    # 设置控件初始值
    slider_avatar_size.setValue(avatar_size)
    btn_edge_hide.setChecked(edge_hide)
    btn_avatar.setChecked(avatar)
    btn_elastic_animation.setChecked(elastic_animation)
    slider_edge_distance.setValue(edge_distance)
    slider_hidden_width.setValue(hidden_width)
    slider_scale.setValue(scale)
    combo_theme.addItems(['浅色', '深色', '跟随系统'])
    combo_theme.setCurrentIndex(int(conf.ini.get('General', 'theme')))

    # 设置标签初始值
    label_avatar_size.setText(str(avatar_size))
    label_edge_distance.setText(str(edge_distance))
    label_hidden_width.setText(str(hidden_width))
    label_scale.setText(str(scale))

    # 设置颜色标签和预览
    current_color = conf.ini.get('Color', 'dark' if isDarkTheme() else 'light')
    label_color.setText(current_color.lower())
    color_obj = QColor(current_color)
    label_color.setStyleSheet(
        f"background-color: {current_color}; color: {'white' if color_obj.lightness() < 128 else 'black'}; padding: 2px; border-radius: 5px")

    # 绑定滑块值变化事件
    slider_avatar_size.valueChanged.connect(lambda value: label_avatar_size.setText(str(value)))
    slider_edge_distance.valueChanged.connect(lambda value: label_edge_distance.setText(str(value)))
    slider_hidden_width.valueChanged.connect(lambda value: label_hidden_width.setText(str(value)))
    slider_scale.valueChanged.connect(lambda value: window.uiInterface.scale_label.setText(str(value)))

    # 绑定按钮事件
    btn_color.clicked.connect(lambda: setup_color_dialog(window))
    window.uiInterface.save_ui.clicked.connect(lambda: save_ui_settings(window))


def setup_color_dialog(window):
    """设置颜色选取器
    
    :param window: 设置窗口实例
    """
    label_color = window.findChild(BodyLabel, 'color_label')
    current_color = QColor(label_color.text())
    dialog_color = ColorDialog(current_color, '选择主题颜色', window, enableAlpha=False)
    dialog_color.yesButton.setText('好')

    # 更新颜色标签和预览
    def update_color_preview(color):
        label_color.setText(color.name())
        label_color.setStyleSheet(
            f"background-color: {color.name()}; color: {'white' if color.lightness() < 128 else 'black'}; padding: 2px; border-radius: 3px;")

    # 初始化颜色预览
    update_color_preview(current_color)

    dialog_color.colorChanged.connect(update_color_preview)
    dialog_color.exec()


def save_ui_settings(window):
    """保存界面设置
    
    :param window: 设置窗口实例
    """
    # 获取控件值
    avatar_size = window.uiInterface.avatar_size.value()
    edge_hide = 'true' if window.uiInterface.edge_hide.isChecked() else 'false'
    edge_distance = window.uiInterface.edge_distance.value()
    hidden_width = window.uiInterface.hidden_width.value()
    avatar = 'true' if window.uiInterface.avatar.isChecked() else 'false'
    scale = window.uiInterface.scale.value() / 100
    theme = window.findChild(ComboBox, 'theme')
    color = window.findChild(BodyLabel, 'color_label')

    conf.ini.write('UI', 'avatar_size', str(avatar_size),
                   'UI', 'edge_hide', edge_hide,
                   'UI', 'edge_distance', str(edge_distance),
                   'UI', 'hidden_width', str(hidden_width),
                   'UI', 'avatar', avatar,
                   'UI', 'elastic_animation', 'true' if window.uiInterface.elastic_animation.isChecked() else 'false',
                   'General', 'scale', str(scale),
                   'General', 'theme', str(theme.currentIndex()),
                   'Color', 'dark' if isDarkTheme() else 'light', color.text())

    if theme.currentIndex() == 0:
        tg_theme = Theme.LIGHT
    elif theme.currentIndex() == 1:
        tg_theme = Theme.DARK
    else:
        tg_theme = Theme.AUTO
    setTheme(tg_theme)

    setThemeColor(conf.ini.get('Color', 'dark' if isDarkTheme() else 'light'))

    # 显示保存成功提示
    Flyout.create(
        icon=InfoBarIcon.SUCCESS,
        title='界面设置已保存',
        content="界面设置已保存至 config.ini。",
        target=window.uiInterface.save_ui,
        parent=window,
        isClosable=False,
        aniType=FlyoutAnimationType.PULL_UP
    )

    # 更新颜色标签和预览
    current_color = conf.ini.get('Color', 'dark' if isDarkTheme() else 'light')
    color.setText(current_color)
    color_obj = QColor(current_color)
    color.setStyleSheet(
        f"background-color: {current_color}; color: {'white' if color_obj.lightness() < 128 else 'black'}; padding: 2px; border-radius: 3px;")

    logger.info('界面设置已保存')