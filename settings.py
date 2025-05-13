"""
RandPicker 设置。
"""
import os
import sys
from math import floor
from typing import override
from time import sleep

from PyQt6 import uic
from PyQt6.QtCore import QUrl, pyqtSignal, QSharedMemory, Qt
from PyQt6.QtGui import QDesktopServices, QIcon, QIntValidator, QColor
from PyQt6.QtWidgets import QApplication, QTableWidgetItem, QHeaderView, QWidget, QHBoxLayout, QFileDialog, QVBoxLayout, \
    QListWidget, QAbstractItemView, QGridLayout, QListWidgetItem, QScroller, QButtonGroup, QLayoutItem
from loguru import logger
from qfluentwidgets import FluentWindow, FluentIcon as fIcon, PushButton, TableWidget, NavigationItemPosition, Flyout, \
    InfoBarIcon, FlyoutAnimationType, SwitchButton, Slider, MessageBox, BodyLabel, LineEdit, setTheme, ComboBox, Theme, \
    ToolButton, ColorDialog, setThemeColor, isDarkTheme, CheckBox, ListWidget, SubtitleLabel, CardWidget, CaptionLabel, \
    RoundMenu, Action, TransparentDropDownToolButton, PrimaryPushButton, MessageBoxBase, \
    StrongBodyLabel, SmoothScrollArea, RadioButton, TitleLabel, InfoBar, InfoBarPosition

import conf
import update

settings = None

share = QSharedMemory('RandPicker')

APP_VERSION = str(update.APP_VERSION)
UPDATER_VERSION = str(update.UPDATER_VERSION)


def open_settings():
    """
    启动设置。
    """
    global settings
    if settings is None or not settings.isVisible():
        settings = Settings()
        settings.closed.connect(cleanup_settings)
        settings.show()
        logger.info('启动设置。')
    else:
        settings.raise_()
        settings.activateWindow()


def cleanup_settings():
    """
    清理设置。
    """
    global settings
    logger.info('关闭设置。')
    del settings
    settings = None


class Settings(FluentWindow):
    """
    设置类。这个类没有参数。
    """
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.aboutInterface = uic.loadUi('./ui/settings/about.ui')
        self.aboutInterface.setObjectName('aboutInterface')
        self.stuEditInterface = uic.loadUi('./ui/settings/students.ui')
        self.stuEditInterface.setObjectName('stuEditInterface')
        self.uiInterface = uic.loadUi('./ui/settings/widget.ui')
        self.uiInterface.setObjectName('uiInterface')
        self.groupEditInterface = uic.loadUi('./ui/settings/group.ui')
        self.groupEditInterface.setObjectName('groupEditInterface')
        self.updateInterface = uic.loadUi('./ui/settings/update.ui')

        self.init_nav()
        self.setup_ui()

    def init_nav(self):  # 设置侧边栏
        self.addSubInterface(self.stuEditInterface, fIcon.EDIT, '学生编辑')
        self.addSubInterface(self.groupEditInterface, fIcon.PEOPLE, '小组编辑')
        self.navigationInterface.addSeparator(NavigationItemPosition.BOTTOM)
        if sys.platform == 'win32':
            self.addSubInterface(self.updateInterface, fIcon.UPDATE, '更新', NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.uiInterface, fIcon.SETTING, '界面设置', NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.aboutInterface, fIcon.INFO, '关于', NavigationItemPosition.BOTTOM)

    def setup_ui(self):  # 设置所有页面
        self.stackedWidget.setCurrentIndex(0)  # 设置初始页面
        self.setMinimumWidth(900)
        self.setMinimumHeight(400)
        self.navigationInterface.setExpandWidth(160)
        self.navigationInterface.setCollapsible(False)
        self.setMicaEffectEnabled(True)  # 启用云母效果

        # 修复设置窗口在各个屏幕分辨率DPI下的窗口大小
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        width = int(screen_width * 0.7)
        height = int(screen_height * 0.7)

        self.move(int(screen_width / 2 - width / 2), 150)
        self.resize(width, height)

        self.setWindowTitle('RandPicker 设置')
        self.setWindowIcon(QIcon('./img/Logo.png'))
        self.setup_about_interface()
        self.setup_student_edit_interface()
        self.setup_ui_interface()
        self.setup_group_edit_interface()
        self.setup_update_interface()

    def setup_about_interface(self):  # 设置 关于 页面
        btn_github = self.findChild(PushButton, 'btn_github')
        btn_github.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://github.com/xuanxuan1231/RandPicker')))

        btn_license = self.findChild(PushButton, 'btn_license')
        btn_license.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl('https://github.com/xuanxuan1231/RandPicker/blob/main/LICENSE')))
        if sys.platform != 'win32':
            caption_update = self.findChild(BodyLabel, 'caption_update')
            caption_update.setText('您的系统不支持应用内更新。')

    def setup_student_edit_interface(self):  # 设置 学生编辑 页面
        table = self.findChild(TableWidget, 'student_list')
        table.setBorderVisible(True)
        table.setBorderRadius(8)
        table.setWordWrap(True)
        table.setColumnCount(4)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        table.setHorizontalHeaderLabels(['', '姓名', '学号', '权重'])

        students = conf.stu.get_all()
        table.setRowCount(len(students))

        for row, student in enumerate(students):
            table.setItem(row, 1, QTableWidgetItem(student['name']))
            table.setItem(row, 2, QTableWidgetItem(str(student['id'])))

            # 初始化 slider
            slider_weight = Slider(Qt.Orientation.Horizontal)
            slider_weight.setObjectName('slider_weight')
            slider_weight.setSingleStep(1)
            slider_weight.setPageStep(1)
            slider_weight.setRange(1, 50)
            slider_weight.setValue(student.get('weight', 1))
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

            # 添加 cellWidget
            table.setCellWidget(row, 3, widget_weight)

            btn_active = CheckBox()
            if student['active']:
                btn_active.setChecked(True)
            else:
                btn_active.setChecked(False)
            table.setCellWidget(row, 0, btn_active)

        # 绑定保存按钮事件
        btn_save = self.findChild(PushButton, 'save_student')
        btn_save.clicked.connect(lambda: self.save_students())

        # 绑定 Excel 导入按钮事件
        btn_import_excel = self.findChild(PushButton, 'import_excel')
        btn_import_excel.clicked.connect(lambda: self.import_file())

        # 绑定 csv 导入按钮事件
        btn_import_csv = self.findChild(PushButton, 'import_csv')
        btn_import_csv.clicked.connect(lambda: self.import_file('csv'))

        # 绑定重置按钮事件
        btn_reset_weight = self.findChild(PushButton, 'reset_weight')
        btn_reset_weight.clicked.connect(lambda: self.reset_weight())
        btn_reset_active = self.findChild(PushButton, 'reset_active')
        btn_reset_active.clicked.connect(lambda: self.reset_active())

        # 添加学生
        le_new_id = self.findChild(LineEdit, 'new_id')
        slider_new_weight = self.findChild(Slider, 'new_weight')
        label_new_weight = self.findChild(BodyLabel, 'new_weight_label')
        btn_new_active = self.findChild(SwitchButton, 'new_active')
        btn_new_save = self.findChild(ToolButton, 'new_save')
        slider_new_weight.valueChanged.connect(lambda: label_new_weight.setText(str(slider_new_weight.value())))
        btn_new_active.setChecked(True)
        btn_new_save.setIcon(fIcon.ADD)
        btn_new_save.clicked.connect(lambda: self.new_student())
        le_new_id.setValidator(QIntValidator(le_new_id))

        # 删除学生
        btn_del = self.findChild(ToolButton, 'del')
        btn_del.setIcon(fIcon.DELETE)
        btn_del.clicked.connect(lambda: table.removeRow(table.currentRow()))

    def new_student(self):  # 新增学生
        le_new_name = self.findChild(LineEdit, 'new_name')
        le_new_id = self.findChild(LineEdit, 'new_id')
        slider_new_weight = self.findChild(Slider, 'new_weight')
        btn_new_active = self.findChild(SwitchButton, 'new_active')
        table = self.findChild(TableWidget, 'student_list')

        if le_new_name.text() == '' or le_new_name.text().isspace() \
                or le_new_id.text() == '':
            return

        row = table.rowCount()
        table.setRowCount(table.rowCount() + 1)
        # 向表格添加新的项目
        table.setItem(row, 1, QTableWidgetItem(le_new_name.text()))
        table.setItem(row, 2, QTableWidgetItem(le_new_id.text()))

        slider_weight = Slider(Qt.Orientation.Horizontal)
        slider_weight.setObjectName('slider_weight')
        slider_weight.setSingleStep(1)
        slider_weight.setPageStep(1)
        slider_weight.setRange(1, 50)
        slider_weight.setValue(slider_new_weight.value())
        slider_weight.setTracking(True)

        tip = BodyLabel()
        tip.setText(str(slider_weight.value()))
        tip.setFixedWidth(47)
        slider_weight.valueChanged.connect(lambda value, t=tip, s=slider_weight: t.setText(str(value)))

        layout_weight = QHBoxLayout()
        layout_weight.setSpacing(3)
        layout_weight.setContentsMargins(12, 0, 0, 0)
        layout_weight.addWidget(slider_weight)
        layout_weight.addWidget(tip)

        # 初始化组件
        widget_weight = QWidget()
        widget_weight.setLayout(layout_weight)

        table.setCellWidget(row, 3, widget_weight)

        btn_active = CheckBox()
        btn_active.setChecked(btn_new_active.isChecked())
        table.setCellWidget(row, 0, btn_active)

        le_new_name.setText('')
        le_new_id.setText('')
        slider_new_weight.setValue(1)
        btn_new_active.setChecked(True)

    def reset_weight(self):  # 重置权重
        table = self.findChild(TableWidget, 'student_list')
        for row in range(0, table.rowCount()):
            table.cellWidget(row, 3).findChild(Slider, 'slider_weight').setValue(1)
        logger.info("重置了所有学生的权重为 1。")

    def reset_active(self):  # 重置 启用
        table = self.findChild(TableWidget, 'student_list')
        for row in range(0, table.rowCount()):
            table.cellWidget(row, 0).setChecked(True)
        logger.info("重置了所有学生的启用为 True。")

    def import_file(self, file_type='excel'):  # 导入
        """
        通用文件导入方法
        :param file_type: 文件类型，支持 'excel' 或 'csv'
        """
        # 打开文件选择对话框
        if file_type.lower() == 'excel':
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "选择 Excel 文件",
                "",
                "Microsoft Excel 文件 (*.xlsx *.xls)"
            )
        else:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "选择 CSV 文件",
                "",
                "CSV 文件 (*.csv)"
            )

        if not file_path:
            return  # 用户取消了选择

        try:
            # 导入
            if file_type.lower() == 'excel':
                students = conf.imp.excel2json(file_path)
            else:
                students = conf.imp.csv2json(file_path)

            if not students or 'students' not in students or not students['students']:
                MessageBox(
                    "导入失败",
                    "没有找到有效的学生数据。\n"
                    "请确保您的表格中包含包含 weight，name，id 和 active 列。",
                    self
                )
                return

            # 更新表格显示
            table = self.findChild(TableWidget, 'student_list')
            table.setRowCount(len(students['students']))

            for row, student in enumerate(students['students']):
                table.setItem(row, 1, QTableWidgetItem(student['name']))
                table.setItem(row, 2, QTableWidgetItem(str(student['id'])))

                # 初始化第 2, 3 row 的 cellwidget
                slider_weight = Slider(Qt.Orientation.Horizontal)
                slider_weight.setObjectName('slider_weight')
                slider_weight.setSingleStep(1)
                slider_weight.setPageStep(1)
                slider_weight.setRange(1, 50)
                slider_weight.setValue(student.get('weight', 1))
                slider_weight.setTracking(True)
                tip = BodyLabel()
                tip.setText(str(slider_weight.value()))
                tip.setFixedWidth(47)
                slider_weight.valueChanged.connect(lambda value, t=tip, s=slider_weight: t.setText(str(value)))
                layout_weight = QHBoxLayout()
                layout_weight.setSpacing(3)
                layout_weight.setContentsMargins(12, 0, 0, 0)
                layout_weight.addWidget(slider_weight)
                layout_weight.addWidget(tip)
                widget_weight = QWidget()
                widget_weight.setLayout(layout_weight)
                table.setCellWidget(row, 3, widget_weight)
                btn_active = CheckBox()
                if student['active']:
                    btn_active.setChecked(True)
                else:
                    btn_active.setChecked(False)
                table.setCellWidget(row, 0, btn_active)

            # 显示成功提示
            btn_import = self.findChild(PushButton, 'import_excel')
            Flyout.create(
                icon=InfoBarIcon.SUCCESS,
                title='导入成功',
                content=f"导入了 {len(students['students'])} 条学生记录。",
                target=btn_import,
                parent=self,
                isClosable=False,
                aniType=FlyoutAnimationType.PULL_UP
            )
            logger.info(f'从 {file_type} 文件导入了 {len(students["students"])} 条学生记录')

        except Exception as e:
            MessageBox(
                "导入错误",
                f"请确保文件格式正确。它应该包含 weight，name，id 和 active 列。",
                self
            )
            logger.error(f'从文件导入时发生错误: {str(e)}')

    def save_students(self):  # 保存 学生 设置
        table = self.findChild(TableWidget, 'student_list')
        students = [{} for _ in range(table.rowCount())]

        for row in range(0, table.rowCount()):
            # logger.debug(f"正在保存学生信息。第 {row} 行。")
            name = table.item(row, 1).text()
            id_ = int(table.item(row, 2).text())
            weight = table.cellWidget(row, 3).findChild(Slider, 'slider_weight').value()
            is_active = table.cellWidget(row, 0).isChecked()
            students[row] = {"name": name, "id": id_, "weight": weight, "active": is_active}

        conf.write_conf(students=students)
        btn_save = self.findChild(PushButton, 'save_student')
        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title='学生信息已保存',
            content="学生信息已保存至 students.json。",
            target=btn_save,
            parent=self,
            isClosable=False,
            aniType=FlyoutAnimationType.PULL_UP
        )
        logger.info('学生信息已保存')

    def setup_ui_interface(self):  # 设置 界面设置 页面
        # 触摸屏适配
        scroll_area = self.findChild(SmoothScrollArea, 'wg_scroll')
        QScroller.grabGesture(scroll_area.viewport(), QScroller.ScrollerGestureType.LeftMouseButtonGesture)
        
        # 从配置文件加载设置
        avatar_size = int(conf.ini.get('UI', 'avatar_size'))
        edge_hide = conf.ini.get('UI', 'edge_hide') == 'true'
        edge_distance = int(conf.ini.get('UI', 'edge_distance'))
        hidden_width = int(conf.ini.get('UI', 'hidden_width'))
        avatar = conf.ini.get('UI', 'avatar') == 'true'
        scale = int(float(conf.ini.get('General', 'scale')) * 100)
        elastic_animation = conf.ini.get('UI', 'elastic_animation') == 'true'

        slider_avatar_size = self.findChild(Slider, 'avatar_size')
        label_avatar_size = self.findChild(BodyLabel, 'avatar_size_label')
        btn_edge_hide = self.findChild(SwitchButton, 'edge_hide')
        btn_avatar = self.findChild(SwitchButton, 'avatar')
        btn_elastic_animation = self.findChild(SwitchButton, 'elastic_animation')
        slider_edge_distance = self.findChild(Slider, 'edge_distance')
        label_edge_distance = self.findChild(BodyLabel, 'edge_distance_label')
        slider_hidden_width = self.findChild(Slider, 'hidden_width')
        label_hidden_width = self.findChild(BodyLabel, 'hidden_width_label')
        slider_scale = self.findChild(Slider, 'scale')
        label_scale = self.findChild(BodyLabel, 'scale_label')
        combo_theme = self.findChild(ComboBox, 'theme')
        btn_color = self.findChild(PushButton, 'color')
        label_color = self.findChild(BodyLabel, 'color_label')

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
        slider_scale.valueChanged.connect(lambda value: self.uiInterface.scale_label.setText(str(value)))

        # 绑定按钮事件
        btn_color.clicked.connect(lambda: self.setup_color_dialog())
        self.uiInterface.save_ui.clicked.connect(lambda: self.save_ui_settings())

    def setup_color_dialog(self):  # 设置颜色选取器
        label_color = self.findChild(BodyLabel, 'color_label')
        current_color = QColor(label_color.text())
        dialog_color = ColorDialog(current_color, '选择主题颜色', self, enableAlpha=False)
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

    def save_ui_settings(self):  # 保存 界面设置 设置
        # 获取控件值
        avatar_size = self.uiInterface.avatar_size.value()
        edge_hide = 'true' if self.uiInterface.edge_hide.isChecked() else 'false'
        edge_distance = self.uiInterface.edge_distance.value()
        hidden_width = self.uiInterface.hidden_width.value()
        avatar = 'true' if self.uiInterface.avatar.isChecked() else 'false'
        scale = self.uiInterface.scale.value() / 100
        theme = self.findChild(ComboBox, 'theme')
        color = self.findChild(BodyLabel, 'color_label')

        conf.ini.write('UI', 'avatar_size', str(avatar_size),
                       'UI', 'edge_hide', edge_hide,
                       'UI', 'edge_distance', str(edge_distance),
                       'UI', 'hidden_width', str(hidden_width),
                       'UI', 'avatar', avatar,
                       'UI', 'elastic_animation', 'true' if self.uiInterface.elastic_animation.isChecked() else 'false',
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
            target=self.uiInterface.save_ui,
            parent=self,
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

    def setup_group_edit_interface(self):
        self.setup_group_edit()

        btn_new = self.findChild(PushButton, 'new_group')
        btn_reload = self.findChild(PushButton, 'reload_page')

        btn_new.clicked.connect(lambda: self.new_group())
        btn_new.setIcon(fIcon.ADD)
        btn_reload.clicked.connect(lambda: self.reload_group_edit())
        btn_reload.setIcon(fIcon.SYNC)

        btn_enable = self.findChild(PushButton, 'enable_groups')
        btn_enable.setIcon(fIcon.EDIT)
        btn_enable.clicked.connect(lambda: self.setup_group_enabled())

    def setup_group_edit(self):  # 设置 分组编辑 页面
        scroll_area = self.findChild(SmoothScrollArea, 'ge_scroll')  # 触摸屏适配
        QScroller.grabGesture(scroll_area.viewport(), QScroller.ScrollerGestureType.LeftMouseButtonGesture)

        layout = self.findChild(QGridLayout, 'group_card_layout')

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

        btn_save = self.findChild(PrimaryPushButton, 'save_group')

        btn_save.clicked.connect(lambda: self.save_groups())

        students = conf.stu.get_all_name()
        global_card = GroupCard(students=students)

        groups = len(conf.group.get_all())
        for i in range(groups):
            group = conf.group.get_single(i)
            stu = conf.group.get_stu_name(group)
            card = GroupCard(title=group['name'],
                             students=stu,
                             is_global=False,
                             parent=self)
            layout.addWidget(card, floor(i / 3) + 1, i % 3, 1, 1)

        layout.addWidget(global_card, 0, 0, 1, layout.columnCount())
        tips_group_empty = self.findChild(CaptionLabel, 'tips_group_empty')
        tips_group_empty.close()

    def reload_group_edit(self): # 重载 分组编辑 页面
        layout = self.findChild(QGridLayout, 'group_card_layout')

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
                             parent=self)
            layout.addWidget(card, floor(i / 3) + 1, i % 3, 1, 1)

        layout.addWidget(global_card, 0, 0, 1, layout.columnCount())

    def setup_group_enabled(self):
        group_enabled_edit = GroupEnablePolicyBox(self)
        group_enabled_edit.exec()

    def new_group(self):  # 新建分组
        students = conf.stu.get_all_name()
        layout = self.findChild(QGridLayout, 'group_card_layout')
        group_edit = GroupEditBox(parent=self,
                                  new=True,
                                  students=students,
                                  target=layout)
        group_edit.exec()

    def save_groups(self):  # 保存 分组编辑 设置
        layout = self.findChild(QGridLayout, 'group_card_layout')
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
        conf.write_conf(groups=groups)

        # 显示保存成功提示
        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title='分组设置已保存',
            content="分组设置已保存至 students.json。",
            target=self.groupEditInterface.save_group,
            parent=self,
            isClosable=False,
            aniType=FlyoutAnimationType.PULL_UP
        )

        # 重载页面
        self.reload_group_edit()
    
    def setup_update_interface(self):  # 设置 更新 页面
        global APP_VERSION, UPDATER_VERSION
        caption_app = self.findChild(BodyLabel, 'caption_app')
        caption_app.setText(f"当前版本：{APP_VERSION}。没有获取到最新版本。")

        if UPDATER_VERSION:
            caption_updater = self.findChild(BodyLabel, 'caption_updater')
            caption_updater.setText(f"当前版本：{UPDATER_VERSION}。没有获取到最新版本。")

        btn_check_app = self.findChild(PushButton, 'check_app')
        btn_check_app.clicked.connect(lambda: self.check_update_app())
        btn_check_updater = self.findChild(PushButton, 'check_updater')
        btn_check_updater.clicked.connect(lambda: self.check_update_updater())

        btn_update_app = self.findChild(PrimaryPushButton, 'update_app')
        btn_update_app.setEnabled(False)
        btn_update_app.clicked.connect(lambda: self.update_app())
        btn_update_updater = self.findChild(PrimaryPushButton, 'update_updater')
        btn_update_updater.setEnabled(False)
        btn_update_updater.clicked.connect(lambda: self.update_updater())

        combo_origin_app = self.findChild(ComboBox, 'app_origin')
        combo_origin_app.addItems(['GitHub', 'OSS (不可用)'])
        combo_origin_app.setCurrentIndex(int(conf.ini.get('Update', 'app')))
        combo_origin_app.currentIndexChanged.connect(lambda index: conf.ini.write('Update', 'app', str(index)))

        combo_origin_updater = self.findChild(ComboBox, 'updater_origin')
        combo_origin_updater.addItems(['GitHub', 'OSS (不可用)'])
        combo_origin_updater.setCurrentIndex(int(conf.ini.get('Update', 'updater')))
        combo_origin_updater.currentIndexChanged.connect(lambda index: conf.ini.write('Update', 'updater', str(index)))

    def check_update_app(self):
        try:
            updates = update.check_update_app(conf.ini.get('Update', 'app'))
        except Exception as e:
            InfoBar.error(
                title='检查更新失败',
                content=f"检查更新失败：{str(e)}",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return
        
        InfoBar.success(
            title='检查更新成功',
            content="RandPicker 有新更新" if not updates['is_latest'] else "RandPicker 已是最新版本",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        caption_app = self.findChild(BodyLabel, 'caption_app')
        title_app = self.findChild(TitleLabel, 'title_app')
        btn_update_app = self.findChild(PrimaryPushButton, 'update_app')
        caption_app.setText(f"当前版本：{APP_VERSION}。最新版本：{updates['version']}。")
        if updates['is_latest']:
            title_app.setText('已是最新版本。')
            btn_update_app.setEnabled(False)
        else:
            title_app.setText('有可用更新。')
            btn_update_app.setEnabled(True)


    def check_update_updater(self):
        try:
            updates = update.check_update_updater(conf.ini.get('Update', 'updater'))
        except Exception as e:
            InfoBar.error(
                title='检查更新失败',
                content=f"检查更新失败：{str(e)}",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return
        
        InfoBar.success(
            title='检查更新成功',
            content="更新助理有新更新" if not updates['is_latest'] else "更新助理已是最新版本",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        caption_updater = self.findChild(BodyLabel, 'caption_updater')
        title_updater = self.findChild(TitleLabel, 'title_updater')
        btn_update_updater = self.findChild(PrimaryPushButton, 'update_updater')
        caption_updater.setText(f"当前版本：{UPDATER_VERSION}。最新版本：{updates['version']}。")
        if updates['is_latest']:
            title_updater.setText('已是最新版本。')
            btn_update_updater.setEnabled(False)
        else:
            title_updater.setText('有可用更新。')
            btn_update_updater.setEnabled(True)

    def update_app(self):
        w = UpdateConfirmBox(self, app=True)
        w.exec()

    def update_updater(self):
        global UPDATER_VERSION
        w = UpdateConfirmBox(self, app=False)
        w.exec()
        UPDATER_VERSION = str(update.UPDATER_VERSION)
        self.check_update_updater()

    @override
    def closeEvent(self, event):  # 重写 closeEvent
        self.closed.emit()
        event.accept()


class UpdateConfirmBox(MessageBoxBase):
    """
    更新确认框。

    :param parent: 父控件。
    :type parent: QWidget | None
    :param title: 标题。
    :type title: str
    :param content: 内容。
    :type content: str
    :param target: 目标控件。
    :type target: QWidget | None

    :raises: None

    :returns: None
    """

    def __init__(self, parent=None, app: bool = False):
        super().__init__(parent)
        self.app = app
        if self.app:
            self.title = '确实要更新 RandPicker？'
            self.content = '将使用 RandPicker 更新助理更新 RandPicker。\n' \
                          'RandPicker 将会退出。请在操作前保存您的更改。\n' \
                          '如果更新助理没有打开，请先更新它。'
        else:
            self.title = '确实要更新 RandPicker 更新助理？'
            self.content = '将更新 RandPicker 更新助理。\n' \
                          'RandPicker 不会被关闭。'
            
        self.titleLabel = TitleLabel(self.title, self)
        self.contentLabel = BodyLabel(self.content, self)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.contentLabel)

        self.yesButton.clicked.connect(self.update)

    def update(self):
        self.yesButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
        if self.app:
            update.update_app()
        else:
            update.update_updater(parent=self)
        self.close()


class GroupCard(CardWidget):  # 分组卡片
    """
    一个表示学生分组的小部件，包含标题、学生列表和管理选项。

    该类继承自 `CardWidget`，提供了一个用于管理学生分组的用户界面。它包括一个标题、学生姓名列表以及一个菜单，
    菜单中包含编辑分组、删除分组和撤销删除的操作。该小部件设计用于需要管理学生分组的大型应用程序中。

    :param title: 分组名称，默认为 '所有学生'。
    :type title: str
    :param students: 分组内的学生姓名列表，默认为 ['未知学生']。
    :type students: list
    :param parent: 父窗口部件，默认为 None。
    :type parent: QWidget | None
    :param is_global: 是否是全局分组（所有学生），默认为 True。
    :type is_global: bool
    """

    def __init__(
            self, title: str = '所有学生', students: list = None, parent: QWidget | None = None,
            is_global: bool = True):
        super().__init__(parent)
        if students is None:
            students = ['未知学生']
        self.exist_students = students
        self.title = title
        self.parent = parent
        self.isDeleted = False

        self.setMinimumHeight(250)

        self.titleLabel = SubtitleLabel(title, self)
        self.moreButton = TransparentDropDownToolButton(fIcon.MORE, self)
        self.moreMenu = RoundMenu(parent=self.moreButton)
        self.stuList = ListWidget(self)

        self.hBoxLayout_Title = QHBoxLayout()
        self.vBoxLayout = QVBoxLayout(self)

        if is_global:
            self.moreButton.setEnabled(False)

        self.action_del = Action(
            fIcon.DELETE, f'删除分组 {title}',
            triggered=lambda: self.del_group()
        )
        self.action_undo_del = Action(
            fIcon.CANCEL, f'撤销删除分组 {title}',
            triggered=lambda: self.undo_del_group()
        )
        self.action_undo_del.setEnabled(False)

        self.moreMenu.addActions([
            Action(
                fIcon.EDIT, '添加或删除学生',
                triggered=lambda: self.set_group()
            ),
            self.action_del,
            self.action_undo_del
        ])
        self.moreButton.setMenu(self.moreMenu)

        self.stuList.addItems(students)
        self.stuList.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        self.stuList.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        # 内容
        self.vBoxLayout.setContentsMargins(6, 6, 6, 6)
        self.vBoxLayout.setSpacing(3)
        self.vBoxLayout.addLayout(self.hBoxLayout_Title)
        self.vBoxLayout.addWidget(self.stuList)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # 标题栏
        self.hBoxLayout_Title.setSpacing(12)
        self.hBoxLayout_Title.setContentsMargins(12, 8, 12, 6)
        # self.hBoxLayout_Title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout_Title.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout_Title.addWidget(self.moreButton, 0, Qt.AlignmentFlag.AlignRight)

    def set_group(self):
        students = conf.stu.get_all_name()
        stu_count = self.stuList.count()
        self.exist_students = []
        for i in range(stu_count):
            item = self.stuList.item(i)
            self.exist_students.append(item.text())
        w = GroupEditBox(parent=self.parent,
                         name=self.title,
                         students=students,
                         exist_students=self.exist_students,
                         target=self)
        w.exec()

    def del_group(self):
        self.action_del.setEnabled(False)
        self.action_undo_del.setEnabled(True)

        self.titleLabel.setText(self.title + ' (删除)')
        self.isDeleted = True

    def undo_del_group(self):
        self.action_del.setEnabled(True)
        self.action_undo_del.setEnabled(False)

        self.titleLabel.setText(self.title)
        self.isDeleted = False


class GroupEditBox(MessageBoxBase):
    """
    编辑分组。

    :param parent: 父控件。
    :type parent: QWidget | None
    :param new: 是否是新建分组。
    :type new: bool
    :param name: 分组现在的名称 (修改分组)。
    :type name: str | None
    :param students: 所有学生的列表。
    :type students: list
    :param exist_students: 已在分组中的学生 (修改分组)。
    :type exist_students: list | None
    :param target: 要修改的布局或控件。新建分组需要 QGridLayout，修改分组需要 GroupCard。
    :type target: QWidget | None

    :raises: None

    :returns: None
    """

    def __init__(self, parent=None, new: bool = False, name: str = None, students: list = None,
                 exist_students: list = None, target: QWidget | None = None):
        super().__init__(parent)
        self.target = target
        self.parent = parent
        self.name = name
        self.titleLabel = SubtitleLabel(text=f'{'添加' if new else '修改'}分组{" " + name if name else ''}')
        self.subtitleLabel_name = StrongBodyLabel(text='分组名称')
        self.nameLineEdit = LineEdit()
        self.captionLabel_name = CaptionLabel(text='名称不能为空。')
        self.subtitleLabel_stu = StrongBodyLabel(text='学生')
        self.stuList = ListWidget()

        self.nameLineEdit.setPlaceholderText('分组名称')
        if name:
            self.nameLineEdit.setText(name)

        self.stuList.setMinimumHeight(200)
        self.stuList.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.stuList.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        for student in students:
            checkbox = CheckBox(text=student)  # 创建复选框
            if exist_students is None:
                checkbox.setChecked(False)
            elif student in exist_students:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)
            list_item = QListWidgetItem()  # 创建列表项

            # 将复选框与列表项关联起来
            self.stuList.addItem(list_item)
            self.stuList.setItemWidget(list_item, checkbox)

        # 将组件添加到布局中
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.subtitleLabel_name)
        self.viewLayout.addWidget(self.nameLineEdit)
        self.viewLayout.addWidget(self.captionLabel_name)
        self.viewLayout.addWidget(self.subtitleLabel_stu)
        self.viewLayout.addWidget(self.stuList)

        # 设置确认按钮操作
        self.yesButton.clicked.connect(lambda: self.save())

        # 设置对话框的最小宽度
        self.widget.setMinimumWidth(350)

    def save(self):
        if self.validate():
            stu = []
            stu_count = self.stuList.count()
            name = self.nameLineEdit.text()
            for i in range(stu_count):
                item = self.stuList.itemWidget(self.stuList.item(i))
                if item.isChecked():
                    stu.append(item.text())

            if isinstance(self.target, GroupCard):
                self.target.titleLabel.setText(name)
                self.target.stuList.clear()
                self.target.stuList.addItems(stu)

                logger.success(f'修改了分组 {self.name} -> {name} 的信息。')
            elif isinstance(self.target, QGridLayout):
                card = GroupCard(title=name,
                                 students=stu,
                                 is_global=False,
                                 parent=self.parent)
                row = self.target.rowCount() - 1
                students = conf.stu.get_all_name()
                global_card = GroupCard(students=students)
                for column in range(1, 3):
                    if not self.target.itemAtPosition(row, column):
                        self.target.addWidget(card, row, column, 1, 1)
                        self.target.addWidget(global_card, 0, 0, 1, self.target.columnCount())
                        logger.success(f'添加了新分组 {name}。')
                        return
                self.target.addWidget(card, row + 1, 0, 1, 1)
                self.target.addWidget(global_card, 0, 0, 1, self.target.columnCount())
                logger.success(f'添加了新分组 {name}。')
            else:
                return

    def validate(self) -> bool:
        if self.nameLineEdit.text() != '' and not self.nameLineEdit.text().isspace():
            return True
        self.captionLabel_name.setTextColor(QColor(255, 0, 0))
        return False


class GroupEnablePolicyBox(MessageBoxBase):
    """
    编辑分组启用。

    """

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.titleLabel = SubtitleLabel(text='编辑分组策略')

        self.btn_global = RadioButton(text='所有学生')
        self.btn_group = RadioButton(text='分组')

        self.group_btn_global = QButtonGroup()
        self.group_btn_global.addButton(self.btn_global, 0)
        self.group_btn_global.addButton(self.btn_group, 1)

        if conf.ini.get('Group', 'global') == 'true':
            self.btn_global.setChecked(True)
        else:
            self.btn_group.setChecked(True)

        self.yesButton.clicked.connect(lambda: self.save())

        self.groupList = ListWidget()
        self.groupList.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        enabled_group = conf.ini.get('Group', 'group').split(', ')

        for group_num in range(len(conf.group.get_all())):
            group = conf.group.get_single(group_num)

            checkbox = CheckBox(text=group['name'])  # 创建复选框
            if enabled_group is None:
                checkbox.setChecked(False)
            elif str(group_num) in enabled_group:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)

            list_item = QListWidgetItem()  # 创建列表项

            # 将复选框与列表项关联起来
            self.groupList.addItem(list_item)
            self.groupList.setItemWidget(list_item, checkbox)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.btn_global)
        self.viewLayout.addWidget(self.btn_group)
        self.viewLayout.addWidget(self.groupList)

    def save(self):
        count = self.groupList.count()
        enable_group = []
        for group in range(count):
            item = self.groupList.item(group)
            if item is None:
                continue
            widget = self.groupList.itemWidget(item)
            if not isinstance(widget, CheckBox):
                return
            if widget.isChecked():
                enable_group.append(group)

        conf.ini.write('Group', 'global', str(self.btn_global.isChecked()),
                       'Group', 'group', str(enable_group).replace('[', '').replace(']', ''))


def restart():
    global share
    if share.isAttached():
        share.detach()
        # share.deleteLater()
    logger.info("重新启动")
    os.execl(sys.executable, sys.executable, *sys.argv)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Settings()
    w.show()
    sys.exit(app.exec())

