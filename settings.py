"""
设置。
"""
import os
import sys

from PyQt6 import uic
from PyQt6.QtCore import QUrl, pyqtSignal, QSharedMemory, Qt
from PyQt6.QtGui import QDesktopServices, QIcon
from PyQt6.QtWidgets import QApplication, QTableWidgetItem, QHeaderView, QWidget, QHBoxLayout, QFileDialog
from loguru import logger
from qfluentwidgets import FluentWindow, FluentIcon as fIcon, PushButton, TableWidget, NavigationItemPosition, Flyout, \
    InfoBarIcon, FlyoutAnimationType, SwitchButton, Slider, LineEdit, MessageBox

import conf

settings = None

share = QSharedMemory('RandPicker')


def open_settings():
    global settings
    if settings is None or not settings.isVisible():
        settings = Settings()
        settings.closed.connect(cleanup_settings)
        settings.show()
        logger.info('打开“设置”')
    else:
        settings.raise_()
        settings.activateWindow()


def cleanup_settings():
    global settings
    logger.info('关闭“设置”')
    del settings
    settings = None


class Settings(FluentWindow):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.aboutInterface = uic.loadUi('./ui/settings/about.ui')
        self.aboutInterface.setObjectName('aboutInterface')
        self.stuEditInterface = uic.loadUi('./ui/settings/students.ui')
        self.stuEditInterface.setObjectName('stuEditInterface')
        self.uiInterface = uic.loadUi('./ui/settings/widget.ui')
        self.uiInterface.setObjectName('uiInterface')

        self.init_nav()
        self.setup_ui()

    def init_nav(self):  # 设置侧边栏
        self.addSubInterface(self.stuEditInterface, fIcon.EDIT, '学生信息编辑')
        self.navigationInterface.addSeparator(NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.uiInterface, fIcon.SETTING, '界面设置', NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.aboutInterface, fIcon.INFO, '关于', NavigationItemPosition.BOTTOM)

    def setup_ui(self):  # 设置所有页面
        self.stackedWidget.setCurrentIndex(0)  # 设置初始页面
        self.setMinimumWidth(700)
        self.setMinimumHeight(400)
        self.navigationInterface.setExpandWidth(200)
        self.navigationInterface.setCollapsible(False)
        self.setMicaEffectEnabled(True)  # 启用云母效果

        # 修复设置窗口在各个屏幕分辨率DPI下的窗口大小
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        width = int(screen_width * 0.6)
        height = int(screen_height * 0.7)

        self.move(int(screen_width / 2 - width / 2), 150)
        self.resize(width, height)

        self.setWindowTitle('RandPicker 设置')
        self.setWindowIcon(QIcon('./img/Logo.png'))
        self.setup_about_interface()
        self.setup_student_edit_interface()
        self.setup_ui_interface()

    def setup_about_interface(self):  # 设置 关于 页面
        btn_github = self.findChild(PushButton, 'btn_github')
        btn_github.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://github.com/xuanxuan1231/RandPicker')))

        btn_license = self.findChild(PushButton, 'btn_license')
        btn_license.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl('https://github.com/xuanxuan1231/RandPicker/blob/main/LICENSE')))

    def setup_student_edit_interface(self):  # 设置 学生信息编辑 页面
        table = self.findChild(TableWidget, 'student_list')
        table.setBorderVisible(True)
        table.setBorderRadius(8)
        table.setWordWrap(True)
        table.setColumnCount(4)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setHorizontalHeaderLabels(['姓名', '学号', '权重', '启用'])

        students = conf.get_all_students()
        table.setRowCount(conf.get_students_num())

        for row, student in enumerate(students['students']):
            table.setItem(row, 0, QTableWidgetItem(student['name']))
            table.setItem(row, 1, QTableWidgetItem(str(student['id'])))

            # 初始化 slider
            slider_weight = Slider(Qt.Orientation.Horizontal)
            slider_weight.setObjectName('slider_weight')
            slider_weight.setSingleStep(1)
            slider_weight.setPageStep(1)
            slider_weight.setRange(1, 50)
            slider_weight.setValue(student.get('weight', 1))
            slider_weight.setTracking(True)

            # 初始化提示
            tip = LineEdit()
            tip.setEnabled(False)
            tip.setText(str(slider_weight.value()))
            tip.setFixedWidth(47)
            slider_weight.valueChanged.connect(lambda value, t=tip, s=slider_weight: t.setText(str(value)))

            # 初始化布局
            layout_weight = QHBoxLayout()
            layout_weight.setSpacing(3)
            layout_weight.setContentsMargins(0, 0, 0, 0)
            layout_weight.addWidget(slider_weight)
            layout_weight.addWidget(tip)

            # 初始化组件
            widget_weight = QWidget()
            widget_weight.setLayout(layout_weight)

            # 添加 cellWidget
            table.setCellWidget(row, 2, widget_weight)

            btn_active = SwitchButton()
            btn_active.setOnText('开')
            btn_active.setOffText('关')
            if student['active']:
                btn_active.setChecked(True)
            else:
                btn_active.setChecked(False)
            table.setCellWidget(row, 3, btn_active)

        # 绑定保存按钮事件
        btn_save = self.findChild(PushButton, 'save_student')
        btn_save.clicked.connect(lambda: self.save_students())

        # 绑定 Excel 导入按钮事件
        btn_import = self.findChild(PushButton, 'import_excel')
        btn_import.clicked.connect(lambda: self.import_excel())

    def import_excel(self):
        # 打开文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择 Excel 文件",
            "",
            "Microsoft Excel 文件 (*.xlsx *.xls)"
        )

        if not file_path:
            return  # 用户取消了选择

        try:
            # 导入
            students = conf.excel2json(file_path)

            if not students or 'students' not in students or not students['students']:
                MessageBox.warning(
                    self,
                    "导入失败",
                    "Excel 文件中没有找到有效的学生数据。\n"
                    "请确保您的表格中包含包含 weight，name，id 和 active 列。",
                    self
                )
                return

            # 更新表格显示
            table = self.findChild(TableWidget, 'student_list')
            table.setRowCount(len(students['students']))

            for row, student in enumerate(students['students']):
                table.setItem(row, 0, QTableWidgetItem(student['name']))
                table.setItem(row, 1, QTableWidgetItem(str(student['id'])))
                table.setItem(row, 2, QTableWidgetItem(str(student.get('weight', 1))))

            # 显示成功提示
            btn_import = self.findChild(PushButton, 'import_excel')
            Flyout.create(
                icon=InfoBarIcon.SUCCESS,
                title='Excel导入成功',
                content=f"已从{os.path.basename(file_path)}导入{len(students['students'])}条学生记录。",
                target=btn_import,
                parent=self,
                isClosable=False,
                aniType=FlyoutAnimationType.PULL_UP
            )
            logger.info(f'从Excel导入了{len(students["students"])}条学生记录')

        except Exception as e:
            MessageBox.critical(
                self,
                "导入错误",
                f"导入Excel文件时发生错误：\n{str(e)}\n\n请确保Excel文件格式正确，并包含weight、name和id列。",
                self
            )
            logger.error(f'Excel导入错误: {str(e)}')

    def save_students(self):
        table = self.findChild(TableWidget, 'student_list')
        students = {'students': [{} for _ in range(table.rowCount())]}

        for row in range(0, table.rowCount()):
            # logger.debug(f"正在保存学生信息。第 {row} 行。")
            name = table.item(row, 0).text()
            id_ = int(table.item(row, 1).text())
            weight = table.cellWidget(row, 2).findChild(Slider, 'slider_weight').value()
            is_active = table.cellWidget(row, 3).isChecked()
            students["students"][row] = {"name": name, "id": id_, "weight": weight, "active": is_active}

        conf.write_conf(students)
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
        # 从配置文件加载设置
        avatar_size = int(conf.get_ini('UI', 'avatar_size'))
        edge_hide = conf.get_ini('UI', 'edge_hide') == 'true'
        edge_distance = int(conf.get_ini('UI', 'edge_distance'))
        hidden_width = int(conf.get_ini('UI', 'hidden_width'))
        avatar = conf.get_ini('UI', 'avatar') == 'true'

        # 设置控件初始值
        self.uiInterface.avatar_size.setValue(avatar_size)
        self.uiInterface.edge_hide.setChecked(edge_hide)
        self.uiInterface.edge_hide.setOnText('开')
        self.uiInterface.edge_hide.setOffText('关')
        self.uiInterface.avatar.setChecked(avatar)
        self.uiInterface.avatar.setOnText('开')
        self.uiInterface.avatar.setOffText('关')
        self.uiInterface.edge_distance.setValue(edge_distance)
        self.uiInterface.hidden_width.setValue(hidden_width)

        # 设置标签初始值
        self.uiInterface.avatar_size_label.setText(str(avatar_size))
        self.uiInterface.edge_distance_label.setText(str(edge_distance))
        self.uiInterface.hidden_width_label.setText(str(hidden_width))

        # 绑定滑块值变化事件
        self.uiInterface.avatar_size.valueChanged.connect(lambda value: self.uiInterface.avatar_size_label.setText(str(value)))
        self.uiInterface.edge_distance.valueChanged.connect(lambda value: self.uiInterface.edge_distance_label.setText(str(value)))
        self.uiInterface.hidden_width.valueChanged.connect(lambda value: self.uiInterface.hidden_width_label.setText(str(value)))

        # 绑定保存按钮事件
        self.uiInterface.save_ui.clicked.connect(lambda: self.save_ui_settings())

    def save_ui_settings(self):
        # 获取控件值
        avatar_size = self.uiInterface.avatar_size.value()
        edge_hide = 'true' if self.uiInterface.edge_hide.isChecked() else 'false'
        edge_distance = self.uiInterface.edge_distance.value()
        hidden_width = self.uiInterface.hidden_width.value()
        avatar = 'true' if self.uiInterface.avatar.isChecked() else 'false'

        # 更新配置文件
        config = conf.config
        config.read('config.ini')
        if 'UI' not in config:
            config['UI'] = {}
        config['UI']['avatar_size'] = str(avatar_size)
        config['UI']['edge_hide'] = edge_hide
        config['UI']['edge_distance'] = str(edge_distance)
        config['UI']['hidden_width'] = str(hidden_width)
        config['UI']['avatar'] = avatar
        with open('config.ini', 'w', encoding='utf-8') as f:
            config.write(f)

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
        logger.info('界面设置已保存')

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()


def restart():
    global share
    if share.attach():
        share.detach()
        share.deleteLater()
    logger.info("重新启动")
    os.execl(sys.executable, sys.executable, *sys.argv)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Settings()
    w.show()
    sys.exit(app.exec())
