"""RandPicker 设置模块。

此模块提供RandPicker的设置功能，包括学生编辑、分组编辑、界面设置和更新等功能。
"""

from .settings_window import Settings, open_settings, cleanup_settings, settings, restart, share

__all__ = ['Settings', 'open_settings', 'cleanup_settings', 'settings', 'restart', 'share']