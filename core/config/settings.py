"""
TODO)) 管理“设置”中的配置
"""

from PySide6.QtCore import QObject
from RinUI import ConfigManager
from pathlib import Path
from .dirs import CONFIG_DIR


class SettingsConfig(ConfigManager, QObject):
    def __init__(self, parent=None):
        self.parent = parent

        ConfigManager.__init__(self, ".", Path(CONFIG_DIR) / "settings.json")
        QObject.__init__(self)