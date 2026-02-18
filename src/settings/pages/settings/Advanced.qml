import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI

FluentPage {
    id: advancedSettingsPage

    title: qsTr("高级")

    SettingCard {
        Layout.fillWidth: true
        title: qsTr("超级置顶")
        description: qsTr("使用 UI Access 强制置顶窗口。可以使 RandPicker 在绝大部分窗口上方显示。\n需要以管理员权限启动。")

        Switch {
            checked: SettingsConfig.getUIAccessEnabled()
            onCheckedChanged: SettingsConfig.setUIAccessEnabled(checked)
        }
    }
}