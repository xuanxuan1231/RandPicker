"""RandPicker 表格组件。

此模块提供表格和卡片组件的实现，包括分组卡片、分组编辑框和更新确认框等。
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QAbstractItemView, QGridLayout, \
    QListWidgetItem, QButtonGroup, QLayoutItem
from loguru import logger
from qfluentwidgets import CardWidget, SubtitleLabel, TransparentDropDownToolButton, RoundMenu, Action, \
    ListWidget, CheckBox, MessageBoxBase, StrongBodyLabel, CaptionLabel, LineEdit, TitleLabel, BodyLabel, \
    RadioButton, FluentIcon as fIcon

import conf
import update


class GroupCard(CardWidget):
    """分组卡片
    
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
        """设置分组"""
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
        """删除分组"""
        self.action_del.setEnabled(False)
        self.action_undo_del.setEnabled(True)

        self.titleLabel.setText(self.title + ' (删除)')
        self.isDeleted = True

    def undo_del_group(self):
        """撤销删除分组"""
        self.action_del.setEnabled(True)
        self.action_undo_del.setEnabled(False)

        self.titleLabel.setText(self.title)
        self.isDeleted = False


class GroupEditBox(MessageBoxBase):
    """分组编辑框
    
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
        """保存分组"""
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
        """验证输入"""
        if self.nameLineEdit.text() != '' and not self.nameLineEdit.text().isspace():
            return True
        self.captionLabel_name.setTextColor(QColor(255, 0, 0))
        return False


class GroupEnablePolicyBox(MessageBoxBase):
    """分组启用策略框
    
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
        """保存分组启用策略"""
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


class UpdateConfirmBox(MessageBoxBase):
    """更新确认框
    
    :param parent: 父控件。
    :type parent: QWidget | None
    :param app: 是否更新应用程序。
    :type app: bool
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
                          'RandPicker 不会被关闭，但会暂时停止响应。正常情况下，停止响应不会超过 40 秒。\n' \
                          '如果停止响应的时间过长，请检查您的网络环境。'
            
        self.titleLabel = TitleLabel(self.title, self)
        self.contentLabel = BodyLabel(self.content, self)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.contentLabel)

        self.yesButton.clicked.connect(self.update)

    def update(self):
        """执行更新"""
        self.yesButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
        if self.app:
            update.update_app()
        else:
            update.update_updater(parent=self)
        self.close()