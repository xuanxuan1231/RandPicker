"""
设置。
"""
import os
import sys

from PyQt6 import uic
from PyQt6.QtCore import QUrl, pyqtSignal, QSharedMemory, Qt
from PyQt6.QtGui import QDesktopServices, QIcon
from PyQt6.QtWidgets import QApplication, QTableWidgetItem, QHeaderView
from loguru import logger
from qfluentwidgets import FluentWindow, FluentIcon as fIcon, PushButton, TableWidget, NavigationItemPosition, Flyout, \
    InfoBarIcon, FlyoutAnimationType, SwitchButton, Slider

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

        self.init_nav()
        self.setup_ui()

    def init_nav(self):  # 设置侧边栏
        self.addSubInterface(self.stuEditInterface, fIcon.EDIT, '学生信息编辑')
        self.navigationInterface.addSeparator(NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.aboutInterface, fIcon.INFO, '关于', NavigationItemPosition.BOTTOM)

    def setup_ui(self):  # 设置所有页面
        self.stackedWidget.setCurrentIndex(0)  # 设置初始页面
        self.setMinimumWidth(700)
        self.setMinimumHeight(400)
        self.navigationInterface.setExpandWidth(200)
        self.navigationInterface.setCollapsible(False)
        self.setMicaEffectEnabled(True)

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
            slider_weight = Slider(Qt.Orientation.Horizontal)
            slider_weight.setSingleStep(1)
            slider_weight.setPageStep(1)
            slider_weight.setRange(1, 50)
            slider_weight.setValue(student['weight'])
            slider_weight.setToolTip(f"{student['weight']}")
            slider_weight.valueChanged.connect(lambda value, slider=slider_weight: slider.setToolTip(f"{value}"))
            table.setCellWidget(row, 2, slider_weight)
            btn_active = SwitchButton()
            btn_active.setOnText('开')
            btn_active.setOffText('关')
            if student['active']:
                btn_active.setChecked(True)
            else:
                btn_active.setChecked(False)
            table.setCellWidget(row, 3, btn_active)

        btn_save = self.findChild(PushButton, 'save_student')
        btn_save.clicked.connect(lambda: self.save_students())

    def save_students(self):
        table = self.findChild(TableWidget, 'student_list')
        students = {'students': [{} for _ in range(table.rowCount())]}

        for row in range(0, table.rowCount()):
            # logger.debug(f"正在保存学生信息。第 {row} 行。")
            name = table.item(row, 0).text()
            id_ = int(table.item(row, 1).text())
            # weight = int(table.item(row, 2).text())
            weight = table.cellWidget(row, 2).value()
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
