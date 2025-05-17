"""RandPicker 学生编辑界面。

此模块提供学生编辑界面的实现。
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QColor
from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView, QWidget, QHBoxLayout, QFileDialog, QVBoxLayout
from loguru import logger
from qfluentwidgets import PushButton, TableWidget, Flyout, InfoBarIcon, FlyoutAnimationType, \
    SwitchButton, Slider, MessageBox, BodyLabel, LineEdit, ToolButton, CheckBox, FluentIcon as fIcon

import conf
from ..components.slider_component import create_weight_slider_widget
from .base_interface import SettingsInterface


def setup_student_edit_interface(window):
    """设置学生编辑界面
    
    :param window: 设置窗口实例
    """
    table = window.findChild(TableWidget, 'student_list')
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
        widget_weight = create_weight_slider_widget(student.get('weight', 1))
        table.setCellWidget(row, 3, widget_weight)

        btn_active = CheckBox()
        if student['active']:
            btn_active.setChecked(True)
        else:
            btn_active.setChecked(False)
        table.setCellWidget(row, 0, btn_active)

    # 绑定保存按钮事件
    btn_save = window.findChild(PushButton, 'save_student')
    btn_save.clicked.connect(lambda: save_students(window))

    # 绑定 Excel 导入按钮事件
    btn_import_excel = window.findChild(PushButton, 'import_excel')
    btn_import_excel.clicked.connect(lambda: import_file(window))

    # 绑定 csv 导入按钮事件
    btn_import_csv = window.findChild(PushButton, 'import_csv')
    btn_import_csv.clicked.connect(lambda: import_file(window, 'csv'))

    # 绑定重置按钮事件
    btn_reset_weight = window.findChild(PushButton, 'reset_weight')
    btn_reset_weight.clicked.connect(lambda: reset_weight(window))
    btn_reset_active = window.findChild(PushButton, 'reset_active')
    btn_reset_active.clicked.connect(lambda: reset_active(window))

    # 添加学生
    le_new_id = window.findChild(LineEdit, 'new_id')
    slider_new_weight = window.findChild(Slider, 'new_weight')
    label_new_weight = window.findChild(BodyLabel, 'new_weight_label')
    btn_new_active = window.findChild(SwitchButton, 'new_active')
    btn_new_save = window.findChild(ToolButton, 'new_save')
    slider_new_weight.valueChanged.connect(lambda: label_new_weight.setText(str(slider_new_weight.value())))
    btn_new_active.setChecked(True)
    btn_new_save.setIcon(fIcon.ADD)
    btn_new_save.clicked.connect(lambda: new_student(window))
    le_new_id.setValidator(QIntValidator(le_new_id))

    # 删除学生
    btn_del = window.findChild(ToolButton, 'del')
    btn_del.setIcon(fIcon.DELETE)
    btn_del.clicked.connect(lambda: table.removeRow(table.currentRow()))


def new_student(window):
    """新增学生
    
    :param window: 设置窗口实例
    """
    le_new_name = window.findChild(LineEdit, 'new_name')
    le_new_id = window.findChild(LineEdit, 'new_id')
    slider_new_weight = window.findChild(Slider, 'new_weight')
    btn_new_active = window.findChild(SwitchButton, 'new_active')
    table = window.findChild(TableWidget, 'student_list')

    if le_new_name.text() == '' or le_new_name.text().isspace() \
            or le_new_id.text() == '':
        return

    row = table.rowCount()
    table.setRowCount(table.rowCount() + 1)
    # 向表格添加新的项目
    table.setItem(row, 1, QTableWidgetItem(le_new_name.text()))
    table.setItem(row, 2, QTableWidgetItem(le_new_id.text()))

    widget_weight = create_weight_slider_widget(slider_new_weight.value())
    table.setCellWidget(row, 3, widget_weight)

    btn_active = CheckBox()
    btn_active.setChecked(btn_new_active.isChecked())
    table.setCellWidget(row, 0, btn_active)

    le_new_name.setText('')
    le_new_id.setText('')
    slider_new_weight.setValue(1)
    btn_new_active.setChecked(True)


def reset_weight(window):
    """重置权重
    
    :param window: 设置窗口实例
    """
    table = window.findChild(TableWidget, 'student_list')
    for row in range(0, table.rowCount()):
        table.cellWidget(row, 3).findChild(Slider, 'slider_weight').setValue(1)
    logger.info("重置了所有学生的权重为 1。")


def reset_active(window):
    """重置 启用
    
    :param window: 设置窗口实例
    """
    table = window.findChild(TableWidget, 'student_list')
    for row in range(0, table.rowCount()):
        table.cellWidget(row, 0).setChecked(True)
    logger.info("重置了所有学生的启用为 True。")


def import_file(window, file_type='excel'):
    """通用文件导入方法
    
    :param window: 设置窗口实例
    :param file_type: 文件类型，支持 'excel' 或 'csv'
    """
    # 打开文件选择对话框
    if file_type.lower() == 'excel':
        file_path, _ = QFileDialog.getOpenFileName(
            window,
            "选择 Excel 文件",
            "",
            "Microsoft Excel 文件 (*.xlsx *.xls)"
        )
    else:
        file_path, _ = QFileDialog.getOpenFileName(
            window,
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
                window
            )
            return

        # 更新表格显示
        table = window.findChild(TableWidget, 'student_list')
        table.setRowCount(len(students['students']))

        for row, student in enumerate(students['students']):
            table.setItem(row, 1, QTableWidgetItem(student['name']))
            table.setItem(row, 2, QTableWidgetItem(str(student['id'])))

            # 初始化第 2, 3 row 的 cellwidget
            widget_weight = create_weight_slider_widget(student.get('weight', 1))
            table.setCellWidget(row, 3, widget_weight)
            
            btn_active = CheckBox()
            if student['active']:
                btn_active.setChecked(True)
            else:
                btn_active.setChecked(False)
            table.setCellWidget(row, 0, btn_active)

        # 显示成功提示
        btn_import = window.findChild(PushButton, 'import_excel')
        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title='导入成功',
            content=f"导入了 {len(students['students'])} 条学生记录。",
            target=btn_import,
            parent=window,
            isClosable=False,
            aniType=FlyoutAnimationType.PULL_UP
        )
        logger.info(f'从 {file_type} 文件导入了 {len(students["students"])} 条学生记录')

    except Exception as e:
        MessageBox(
            "导入错误",
            f"请确保文件格式正确。它应该包含 weight，name，id 和 active 列。",
            window
        )
        logger.error(f'从文件导入时发生错误: {str(e)}')


def save_students(window):
    """保存学生设置
    
    :param window: 设置窗口实例
    """
    table = window.findChild(TableWidget, 'student_list')
    students = [{} for _ in range(table.rowCount())]

    for row in range(0, table.rowCount()):
        # logger.debug(f"正在保存学生信息。第 {row} 行。")
        name = table.item(row, 1).text()
        id_ = int(table.item(row, 2).text())
        weight = table.cellWidget(row, 3).findChild(Slider, 'slider_weight').value()
        is_active = table.cellWidget(row, 0).isChecked()
        students[row] = {"name": name, "id": id_, "weight": weight, "active": is_active}

    conf.write_conf(students=students)
    btn_save = window.findChild(PushButton, 'save_student')
    Flyout.create(
        icon=InfoBarIcon.SUCCESS,
        title='学生信息已保存',
        content="学生信息已保存至 students.json。",
        target=btn_save,
        parent=window,
        isClosable=False,
        aniType=FlyoutAnimationType.PULL_UP
    )
    logger.info('学生信息已保存')