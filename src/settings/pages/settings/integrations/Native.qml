import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import RinUI
import "../../../../components"

Item {
    implicitHeight: childrenRect.height
    ColumnLayout {
        width: parent.width

        InfoBar {
            id: connectedInfo

            closable: false
            severity: Severity.Success
            text: qsTr("原生通知可在您的系统上正常工作。")
            title: qsTr("可用")

            // TODO)) 检查可用性
            visible: true

            customContent: [
                Hyperlink {
                    text: qsTr("测试通知")

                    onClicked: {
                        NotificationManager.sendTest("native");
                    }
                }
            ]
        }

        InfoBar {
            id: connectedTip

            closable: false
            text: qsTr("如果您没有收到通知，请检查系统的通知设置，确保\n· 勿扰模式已关闭，\n· 允许 RandPicker 发送通知。")
            title: qsTr("看不到通知？")
            visible: connectedInfo.visible
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

        SettingCard {
            id: notifyFormatSettingCard

            Layout.fillWidth: true
            title: qsTr("编辑通知格式")

            Icon {
                icon: "ic_fluent_open_20_regular"
                size: 20
            }

            TapHandler {
                parent: notifyFormatSettingCard

                onTapped: notifyFormatEditDialog.open()
            }
        }
    }

    NotifyFormatEditDialog {
        id: notifyFormatEditDialog
        notifyOption: "native"
    }
}