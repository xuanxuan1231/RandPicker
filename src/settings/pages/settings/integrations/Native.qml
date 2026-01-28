import QtQuick
import QtQuick.Layouts
import RinUI

Item {
    anchors.fill: parent
    ColumnLayout {
        anchors.fill: parent

        InfoBar {
            id: connectedInfo

            closable: false
            severity: Severity.Success
            text: qsTr("原生通知可在您的系统上正常工作。")
            title: qsTr("通知可用")
            visible: SettingsService.getConnectivityStatus("classisland") === "Connected"

            customContent: [
                Hyperlink {
                    text: qsTr("测试通知")

                    onClicked: {
                        NotificationManager.sendTest("native");
                    }
                }
            ]
        }

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