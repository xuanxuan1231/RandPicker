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
            text: qsTr("不能使用 ClassIsland 的通知和规则。我们正继续尝试连接。")
            visible: !SettingsService.getConnectivityStatus("classisland")
            closable: false
        }

        InfoBar {
            id: notConnectedTip
            title: qsTr("排障")
            text: qsTr("请确保您已启动 ClassIsland v2，且安装了“RandPicker”插件。\n如果故障仍然存在，请联系我们。")
            visible: notConnectedInfo.visible
            closable: false
            customContent: [
                Hyperlink {
                    text: qsTr("更多排障指南")
                    onClicked: {
                        Qt.openUrlExternally("https://randpicker2.netlify.app/")
                    }
                },
                Hyperlink {
                    text: "ClassIsland"
                    onClicked: {
                        Qt.openUrlExternally("classisland://app/settings/classisland.plugins")
                    }
                }
            ]
        }
        
        InfoBar {
            id: connectedInfo
            severity: Severity.Success
            title: qsTr("已连接")
            text: qsTr("通知和规则可以正常使用。")
            visible: SettingsService.getConnectivityStatus("classisland")
            closable: false
        }
        
        InfoBar {
            id: unknownInfo
            severity: Severity.Warning
            title: qsTr("未知状态")
            text: qsTr("在获取集成状态时出现问题。这不是你的错，也不是我们的。")
            visible: false
            closable: false
        }

        SettingCard {
            Layout.fillWidth: true
            title: qsTr("启用通知")
            description: qsTr("启用后，RandPicker 的通知将通过 ClassIsland 发送。")

            Switch {
                checked: SettingsConfig.getNotifyOptionStatus("classisland")
                Component.onCompleted: {
                        checked = SettingsConfig.getNotifyOptionStatus("classisland")
                }
                onCheckedChanged: SettingsConfig.setNotifyOptionStatus("classisland", checked)
            }
        }
    }
    Connections {
        target: SettingsService

        function onConnectivityUpdated(method, connectivity) {
            if (method === "classisland") {
                notConnectedInfo.visible = !connectivity
                connectedInfo.visible = connectivity
                unknownInfo.visible = false
            }
        }
    }
}