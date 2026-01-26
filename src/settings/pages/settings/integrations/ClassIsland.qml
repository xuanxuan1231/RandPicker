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
            visible: SettingsService.getConnectivityStatus("classisland") === "NotConnected"
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
            visible: SettingsService.getConnectivityStatus("classisland") === "Connected"
            closable: false
        }
        
        InfoBar {
            id: notRunningInfo
            severity: Severity.Warning
            title: qsTr("重连已停止")
            text: qsTr("因为重连失败频率太高，RandPicker 自发停止了重连。")
            visible: SettingsService.getConnectivityStatus("classisland") === "NotRunning"
            closable: false
        }
        InfoBar {
            id: notRunningTip
            severity: Severity.Info
            title: qsTr("排障")
            text: qsTr("检查是否在 ClassIsland 中安装并加载了“RandPicker”插件，然后重新启动 RandPicker。")
            visible: notRunningInfo.visible
            closable: false

            customContent: [
                Hyperlink {
                    text: qsTr("ClassIsland 插件市场")
                    onClicked: {
                        Qt.openUrlExternally("classisland://app/settings/classisland.plugins")
                    }
                },
                Hyperlink {
                    text: qsTr("重新启动")
                    onClicked: {
                        AppMain.restart()
                    }
                }
            ]
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

        SettingCard {
            Layout.fillWidth: true
            title: qsTr("遮罩显示时长")
            description: qsTr("设置 ClassIsland 设置遮罩的显示时长。")

            SpinBox {
                from: 0
                to: 60
                value: SettingsConfig.getMaskDuration("classisland")
                Component.onCompleted: {
                        value = SettingsConfig.getMaskDuration("classisland")
                }
                onValueChanged: SettingsConfig.setMaskDuration("classisland", value)
            }

            Text {
                text: qsTr("秒")
            }
        }
    }
    Connections {
        target: SettingsService

        function onConnectivityUpdated(method, connectivity) {
            if (method === "classisland") {
                notConnectedInfo.visible = connectivity === "NotConnected"
                connectedInfo.visible = connectivity === "Connected"
                notRunningInfo.visible = connectivity === "NotRunning"
            }
        }
    }
}