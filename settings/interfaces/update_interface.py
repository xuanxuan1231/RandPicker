"""RandPicker 更新界面。

此模块提供更新界面的实现。
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from loguru import logger
from qfluentwidgets import PushButton, PrimaryPushButton, BodyLabel, TitleLabel, ComboBox, InfoBar, InfoBarPosition

import conf
import update
from ..components.table_widget import UpdateConfirmBox
from .base_interface import SettingsInterface


def setup_update_interface(window):
    """设置更新页面
    
    :param window: 设置窗口实例
    """
    global APP_VERSION, UPDATER_VERSION
    from ..settings_window import APP_VERSION, UPDATER_VERSION

    caption_app = window.updateInterface.caption_app
    caption_app.setText(f"当前版本：{APP_VERSION}。没有获取到最新版本。")

    if UPDATER_VERSION:
        caption_updater = window.updateInterface.caption_updater
        caption_updater.setText(f"当前版本：{UPDATER_VERSION}。没有获取到最新版本。")

    btn_check_app = window.updateInterface.check_app
    btn_check_app.clicked.connect(lambda: check_update_app(window))
    btn_check_updater = window.updateInterface.check_updater
    btn_check_updater.clicked.connect(lambda: check_update_updater(window))

    btn_update_app = window.updateInterface.update_app
    btn_update_app.setEnabled(False)
    btn_update_app.clicked.connect(lambda: update_app(window))
    btn_update_updater = window.updateInterface.update_updater
    btn_update_updater.setEnabled(False)
    btn_update_updater.clicked.connect(lambda: update_updater(window))

    combo_origin_app = window.updateInterface.app_origin
    combo_origin_app.addItems(['GitHub', 'OSS (不可用)'])
    combo_origin_app.setCurrentIndex(int(conf.ini.get('Update', 'app')))
    combo_origin_app.currentIndexChanged.connect(lambda index: conf.ini.write('Update', 'app', str(index)))

    combo_origin_updater = window.updateInterface.updater_origin
    combo_origin_updater.addItems(['GitHub', 'OSS (不可用)'])
    combo_origin_updater.setCurrentIndex(int(conf.ini.get('Update', 'updater')))
    combo_origin_updater.currentIndexChanged.connect(lambda index: conf.ini.write('Update', 'updater', str(index)))


def check_update_app(window):
    """检查应用更新

    :param window: 设置窗口实例
    """
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
            parent=window
        )
        return

    InfoBar.success(
        title='检查更新成功',
        content="RandPicker 有新更新" if not updates['is_latest'] else "RandPicker 已是最新版本",
        orient=Qt.Orientation.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=2000,
        parent=window
    )
    caption_app = window.updateInterface.caption_app
    title_app = window.updateInterface.title_app
    btn_update_app = window.updateInterface.update_app
    caption_app.setText(f"当前版本：{APP_VERSION}。最新版本：{updates['version']}。")
    if updates['is_latest']:
        title_app.setText('已是最新版本。')
        btn_update_app.setEnabled(False)
    else:
        title_app.setText('有可用更新。')
        btn_update_app.setEnabled(True)


def check_update_updater(window):
    """检查更新器更新

    :param window: 设置窗口实例
    """
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
            parent=window
        )
        return

    InfoBar.success(
        title='检查更新成功',
        content="更新助理有新更新" if not updates['is_latest'] else "更新助理已是最新版本",
        orient=Qt.Orientation.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=2000,
        parent=window
    )
    caption_updater = window.updateInterface.caption_updater
    title_updater = window.updateInterface.title_updater
    btn_update_updater = window.updateInterface.update_updater
    caption_updater.setText(f"当前版本：{UPDATER_VERSION}。最新版本：{updates['version']}。")
    if updates['is_latest']:
        title_updater.setText('已是最新版本。')
        btn_update_updater.setEnabled(False)
    else:
        title_updater.setText('有可用更新。')
        btn_update_updater.setEnabled(True)


def update_app(window):
    """更新应用

    :param window: 设置窗口实例
    """
    w = UpdateConfirmBox(window, app=True)
    w.exec()


def update_updater(window):
    """更新更新器

    :param window: 设置窗口实例
    """
    from ..settings_window import UPDATER_VERSION
    w = UpdateConfirmBox(window, app=False)
    w.exec()
    UPDATER_VERSION = str(update.UPDATER_VERSION)
    check_update_updater(window)