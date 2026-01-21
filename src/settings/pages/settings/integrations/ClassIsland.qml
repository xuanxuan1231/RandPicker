import QtQuick
import QtQuick.Layouts
import RinUI

Item {
    anchors.fill: parent
    ColumnLayout {
        anchors.fill: parent
        
        InfoBar {
            id: notConnectedInfo
            severity: Severity.Error
            title: qsTr("未连接")
            text: qsTr("未连接到 ClassIsland v2 集成。将不能使用 ClassIsland 的通知和规则。")
            visible: CiService.getStatus() === "NotConnected"
        }
        
        InfoBar {
            id: connectedInfo
            severity: Severity.Success
            title: qsTr("已连接")
            text: qsTr("已连接到 ClassIsland v2。")
            visible: CiService.getStatus() === "Connected"
        }
        
        InfoBar {
            id: unknownInfo
            severity: Severity.Warning
            title: qsTr("未知状态")
            text: qsTr("在获取集成状态时出现问题。")
            visible: CiService.getStatus() === "Unknown"
        }

        SettingCard {
            Layout.fillWidth: true
            title: qsTr("启用通知")
            description: qsTr("启用后，RandPicker 的通知将通过 ClassIsland 发送。")

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