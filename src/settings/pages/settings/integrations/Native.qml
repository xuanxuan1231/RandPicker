import QtQuick
import QtQuick.Layouts
import RinUI

Item {
    anchors.fill: parent
    ColumnLayout {
        anchors.fill: parent
        spacing: 8
        SettingCard {
            Layout.fillWidth: true
            title: qsTr("启用通知")
            description: qsTr("启用后，RandPicker 的通知将通过系统发送。")

            Switch {
                checked: SettingsConfig.getNotifyOptionStatus("native")
                Component.onCompleted: {
                        checked = SettingsConfig.getNotifyOptionStatus("native")
                }
                onCheckedChanged: SettingsConfig.setNotifyOptionStatus("native", checked)
            }
        }
    }
}