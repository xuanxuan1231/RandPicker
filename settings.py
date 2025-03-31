"""
设置。
"""
import os
import sys

from PyQt6 import uic
from PyQt6.QtCore import QUrl, pyqtSignal, QSharedMemory, Qt
from PyQt6.QtGui import QDesktopServices, QIcon, QIntValidator
from PyQt6.QtWidgets import QApplication, QTableWidgetItem, QHeaderView, QWidget, QHBoxLayout, QFileDialog
from loguru import logger
from qfluentwidgets import FluentWindow, FluentIcon as fIcon, PushButton, TableWidget, NavigationItemPosition, Flyout, \
    InfoBarIcon, FlyoutAnimationType, SwitchButton, Slider, MessageBox, BodyLabel, LineEdit, setTheme, ComboBox, Theme, \
    ToolButton

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
        btn_new_active.setOnText("开")
        btn_new_active.setOffText("关")
        btn_new_active.setChecked(True)
        btn_new_save.setIcon(fIcon.ADD)
        btn_new_save.clicked.connect(lambda: self.new_student())
        le_new_id.setValidator(QIntValidator(le_new_id))

        # 删除学生
        btn_del = self.findChild(ToolButton, 'del')
        btn_del.setIcon(fIcon.DELETE)
        btn_del.clicked.connect(lambda: table.removeRow(table.currentRow()))

    def new_student(self):
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

        table.setItem(row, 0, QTableWidgetItem(le_new_name.text()))
        table.setItem(row, 1, QTableWidgetItem(le_new_id.text()))

        # 初始化 slider
        slider_weight = Slider(Qt.Orientation.Horizontal)
        slider_weight.setObjectName('slider_weight')
        slider_weight.setSingleStep(1)
        slider_weight.setPageStep(1)
        slider_weight.setRange(1, 50)
        slider_weight.setValue(slider_new_weight.value())
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
        table.setCellWidget(row, 2, widget_weight)

        btn_active = SwitchButton()
        btn_active.setOnText('开')
        btn_active.setOffText('关')
        btn_active.setChecked(btn_new_active.isChecked())
        table.setCellWidget(row, 3, btn_active)

        le_new_name.setText('')
        le_new_id.setText('')
        slider_new_weight.setValue(1)
        btn_new_active.setChecked(True)

    def reset_weight(self):
        table = self.findChild(TableWidget, 'student_list')
        for row in range(0, table.rowCount()):
            table.cellWidget(row, 2).findChild(Slider, 'slider_weight').setValue(1)
        logger.info("重置了所有学生的权重为 1。")

    def reset_active(self):
        table = self.findChild(TableWidget, 'student_list')
        for row in range(0, table.rowCount()):
            table.cellWidget(row, 3).setChecked(True)
        logger.info("重置了所有学生的启用为 True。")

    def import_file(self, file_type='excel'):
        """
        通用文件导入方法
        :param file_type: 文件类型，支持'excel'或'csv'
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
                students = conf.excel2json(file_path)
            else:
                students = conf.csv2json(file_path)

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
                table.setItem(row, 0, QTableWidgetItem(student['name']))
                table.setItem(row, 1, QTableWidgetItem(str(student['id'])))

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
                table.setCellWidget(row, 2, widget_weight)
                btn_active = SwitchButton()
                btn_active.setOnText('开')
                btn_active.setOffText('关')
                if student['active']:
                    btn_active.setChecked(True)
                else:
                    btn_active.setChecked(False)
                table.setCellWidget(row, 3, btn_active)

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
        scale = int(float(conf.get_ini('General', 'scale')) * 100)
        elastic_animation = conf.get_ini('UI', 'elastic_animation') == 'true'

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

        # 设置控件初始值
        slider_avatar_size.setValue(avatar_size)
        btn_edge_hide.setChecked(edge_hide)
        btn_edge_hide.setOnText('开')
        btn_edge_hide.setOffText('关')
        btn_avatar.setChecked(avatar)
        btn_avatar.setOnText('开')
        btn_avatar.setOffText('关')
        btn_elastic_animation.setChecked(elastic_animation)
        btn_elastic_animation.setOnText('开')
        btn_elastic_animation.setOffText('关')
        slider_edge_distance.setValue(edge_distance)
        slider_hidden_width.setValue(hidden_width)
        slider_scale.setValue(scale)
        combo_theme.addItems(['浅色', '深色', '跟随系统'])
        combo_theme.setCurrentIndex(int(conf.get_ini('General', 'theme')))

        # 设置标签初始值
        label_avatar_size.setText(str(avatar_size))
        label_edge_distance.setText(str(edge_distance))
        label_hidden_width.setText(str(hidden_width))
        label_scale.setText(str(scale))

        # 绑定滑块值变化事件
        slider_avatar_size.valueChanged.connect(lambda value: label_avatar_size.setText(str(value)))
        slider_edge_distance.valueChanged.connect(lambda value: label_edge_distance.setText(str(value)))
        slider_hidden_width.valueChanged.connect(lambda value: label_hidden_width.setText(str(value)))
        slider_scale.valueChanged.connect(lambda value: self.uiInterface.scale_label.setText(str(value)))

        # 绑定保存按钮事件
        self.uiInterface.save_ui.clicked.connect(lambda: self.save_ui_settings())

    def save_ui_settings(self):
        # 获取控件值
        avatar_size = self.uiInterface.avatar_size.value()
        edge_hide = 'true' if self.uiInterface.edge_hide.isChecked() else 'false'
        edge_distance = self.uiInterface.edge_distance.value()
        hidden_width = self.uiInterface.hidden_width.value()
        avatar = 'true' if self.uiInterface.avatar.isChecked() else 'false'
        scale = self.uiInterface.scale.value() / 100
        theme = self.findChild(ComboBox, 'theme')

        conf.write_ini('UI', 'avatar_size', str(avatar_size),
                       'UI', 'edge_hide', edge_hide,
                       'UI', 'edge_distance', str(edge_distance),
                       'UI', 'hidden_width', str(hidden_width),
                       'UI', 'avatar', avatar,
                       'UI', 'elastic_animation', 'true' if self.uiInterface.elastic_animation.isChecked() else 'false',
                       'General', 'scale', str(scale),
                       'General', 'theme', str(theme.currentIndex()))

        if theme.currentIndex() == 0:
            tg_theme = Theme.LIGHT
        elif theme.currentIndex() == 1:
            tg_theme = Theme.DARK
        else:
            tg_theme = Theme.AUTO
        setTheme(tg_theme)

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
