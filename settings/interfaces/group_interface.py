"""RandPicker 分组编辑界面。

此模块提供分组编辑界面的实现。
"""
from math import floor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLayoutItem, QWidget
from PyQt6.QtWidgets import QScroller
from loguru import logger
from qfluentwidgets import PushButton, PrimaryPushButton, Flyout, InfoBarIcon, FlyoutAnimationType, \
    SmoothScrollArea, CaptionLabel, FluentIcon as fIcon

import conf
from ..components.table_widget import GroupCard, GroupEditBox, GroupEnablePolicyBox
from .base_interface import SettingsInterface


def setup_group_edit_interface(window):
    """设置分组编辑界面
    
    :param window: 设置窗口实例
    """
    setup_group_edit(window)

    btn_new = window.findChild(PushButton, 'new_group')
    btn_reload = window.findChild(PushButton, 'reload_page')

    btn_new.clicked.connect(lambda: new_group(window))
    btn_new.setIcon(fIcon.ADD)
    btn_reload.clicked.connect(lambda: reload_group_edit(window))
    btn_reload.setIcon(fIcon.SYNC)

    btn_enable = window.findChild(PushButton, 'enable_groups')
    btn_enable.setIcon(fIcon.EDIT)
    btn_enable.clicked.connect(lambda: setup_group_enabled(window))


def setup_group_edit(window):
    """设置分组编辑页面
    
    :param window: 设置窗口实例
    """
    scroll_area = window.findChild(SmoothScrollArea, 'ge_scroll')  # 触摸屏适配
    QScroller.grabGesture(scroll_area.viewport(), QScroller.ScrollerGestureType.LeftMouseButtonGesture)

    layout = window.findChild(QGridLayout, 'group_card_layout')

    # 清空现有布局
    item_list = list(range(layout.count()))
    item_list.reverse()  # 倒序删除，避免影响布局顺序

    for i in item_list:
        item = layout.itemAt(i)
        if isinstance(item.widget(), CaptionLabel):
            continue
        layout.removeItem(item)
        if item.widget():
            item.widget().deleteLater()
    logger.success('清空了分组卡片所在的布局。')

    btn_save = window.findChild(PrimaryPushButton, 'save_group')

    btn_save.clicked.connect(lambda: save_groups(window))

    students = conf.stu.get_all_name()
    global_card = GroupCard(students=students)

    groups = len(conf.group.get_all())
    for i in range(groups):
        group = conf.group.get_single(i)
        stu = conf.group.get_stu_name(group)
        card = GroupCard(title=group['name'],
                         students=stu,
                         is_global=False,
                         parent=window)
        layout.addWidget(card, floor(i / 3) + 1, i % 3, 1, 1)

    layout.addWidget(global_card, 0, 0, 1, layout.columnCount())
    tips_group_empty = window.findChild(CaptionLabel, 'tips_group_empty')
    tips_group_empty.close()


def reload_group_edit(window):
    """重载分组编辑页面
    
    :param window: 设置窗口实例
    """
    layout = window.findChild(QGridLayout, 'group_card_layout')

    # 清空现有布局
    item_list = list(range(layout.count()))
    item_list.reverse()  # 倒序删除，避免影响布局顺序

    for i in item_list:
        item = layout.itemAt(i)
        if isinstance(item.widget(), CaptionLabel):
            continue
        layout.removeItem(item)
        if item.widget():
            item.widget().deleteLater()
    logger.success('清空了分组卡片所在的布局。')

    students = conf.stu.get_all_name()
    global_card = GroupCard(students=students)

    groups = len(conf.group.get_all())
    for i in range(groups):
        group = conf.group.get_single(i)
        stu = conf.group.get_stu_name(group)
        card = GroupCard(title=group['name'],
                         students=stu,
                         is_global=False,
                         parent=window)
        layout.addWidget(card, floor(i / 3) + 1, i % 3, 1, 1)

    layout.addWidget(global_card, 0, 0, 1, layout.columnCount())


def setup_group_enabled(window):
    """设置分组启用策略
    
    :param window: 设置窗口实例
    """
    group_enabled_edit = GroupEnablePolicyBox(window)
    group_enabled_edit.exec()


def new_group(window):
    """新建分组
    
    :param window: 设置窗口实例
    """
    students = conf.stu.get_all_name()
    layout = window.findChild(QGridLayout, 'group_card_layout')
    group_edit = GroupEditBox(parent=window,
                              new=True,
                              students=students,
                              target=layout)
    group_edit.exec()


def save_groups(window):
    """保存分组编辑设置
    
    :param window: 设置窗口实例
    """
    layout = window.findChild(QGridLayout, 'group_card_layout')
    groups = []
    for row in range(1, layout.rowCount()):
        for column in range(0, layout.columnCount()):
            stu = []
            item = layout.itemAtPosition(row, column)
            if not isinstance(item, QLayoutItem):
                logger.warning(f"保存分组时，对于 {row}, {column} 处来说，没有找到 QLayoutItem。")
                logger.warning(f"跳过 {row}, {column} 处的卡片。")
                continue

            card = item.widget()

            if card.isDeleted:
                logger.warning(f"保存分组时，卡片 {row}, {column} 被标记为已删除。")
                logger.warning(f"跳过 {row}, {column} 处的卡片。")
                continue

            title = card.titleLabel.text()
            stu_list = card.stuList
            stu_count = stu_list.count()
            for i in range(stu_count):
                stu.append(conf.stu.get_index_4name(stu_list.item(i).text()))
            group = {"name": title, "stu": stu}
            groups.append(group)
    students_data = conf.stu.get_all()
    conf.write_conf(students=students_data, groups=groups)

    # 显示保存成功提示
    Flyout.create(
        icon=InfoBarIcon.SUCCESS,
        title='分组设置已保存',
        content="分组设置已保存至 students.json。",
        target=window.groupEditInterface.save_group,
        parent=window,
        isClosable=False,
        aniType=FlyoutAnimationType.PULL_UP
    )

    # 重载页面
    reload_group_edit(window)