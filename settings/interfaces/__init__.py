"""RandPicker 设置界面模块。

此模块包含所有设置界面的实现。
"""

from .about_interface import setup_about_interface
from .group_interface import setup_group_edit_interface, setup_group_enabled, new_group, save_groups
from .student_interface import setup_student_edit_interface, save_students
from .ui_interface import setup_ui_interface, save_ui_settings
from .update_interface import setup_update_interface

__all__ = [
    'setup_about_interface',
    'setup_group_edit_interface', 'setup_group_enabled', 'new_group', 'save_groups',
    'setup_student_edit_interface', 'save_students',
    'setup_ui_interface', 'save_ui_settings',
    'setup_update_interface'
]