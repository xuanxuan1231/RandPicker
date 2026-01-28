import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import RinUI

Item {
    anchors.fill: parent

    ColumnLayout {
        anchors.fill: parent

        InfoBar {
            id: notConnectedInfo

            closable: false
            severity: Severity.Error
            text: qsTr("不能使用 ClassIsland 的通知和规则。我们正继续尝试连接。")
            title: qsTr("未连接")
            visible: SettingsService.getConnectivityStatus("classisland") === "NotConnected"
        }
        InfoBar {
            id: notConnectedTip

            closable: false
            text: qsTr("请确保您已启动 ClassIsland v2，且安装了“RandPicker”插件。\n如果故障仍然存在，请联系我们。")
            title: qsTr("排障")
            visible: notConnectedInfo.visible

            customContent: [
                Hyperlink {
                    text: qsTr("更多排障指南")

                    onClicked: {
                        Qt.openUrlExternally("https://randpicker2.netlify.app/");
                    }
                },
                Hyperlink {
                    text: "ClassIsland"

                    onClicked: {
                        Qt.openUrlExternally("classisland://app/settings/classisland.plugins");
                    }
                }
            ]
        }
        InfoBar {
            id: connectedInfo

            closable: false
            severity: Severity.Success
            text: qsTr("通知和规则可以正常使用。")
            title: qsTr("已连接")
            visible: SettingsService.getConnectivityStatus("classisland") === "Connected"

            customContent: [
                Hyperlink {
                    text: qsTr("测试通知")

                    onClicked: {
                        NotificationManager.sendTest("classisland");
                    }
                }
            ]
        }
        InfoBar {
            id: notRunningInfo

            closable: false
            severity: Severity.Warning
            text: qsTr("因为重连失败频率太高，RandPicker 自发停止了重连。")
            title: qsTr("重连已停止")
            visible: SettingsService.getConnectivityStatus("classisland") === "NotRunning"
        }
        InfoBar {
            id: notRunningTip

            closable: false
            severity: Severity.Info
            text: qsTr("检查是否在 ClassIsland 中安装并加载了“RandPicker”插件，然后重新启动 RandPicker。")
            title: qsTr("排障")
            visible: notRunningInfo.visible

            customContent: [
                Hyperlink {
                    text: qsTr("ClassIsland 插件市场")

                    onClicked: {
                        Qt.openUrlExternally("classisland://app/settings/classisland.plugins");
                    }
                },
                Hyperlink {
                    text: qsTr("重新启动")

                    onClicked: {
                        AppMain.restart();
                    }
                }
            ]
        }
        SettingCard {
            Layout.fillWidth: true
            description: qsTr("启用后，RandPicker 的通知将通过 ClassIsland 发送。")
            title: qsTr("启用通知")

            Switch {
                checked: SettingsConfig.getNotifyOptionStatus("classisland")

                Component.onCompleted: {
                    checked = SettingsConfig.getNotifyOptionStatus("classisland");
                }
                onCheckedChanged: SettingsConfig.setNotifyOptionStatus("classisland", checked)
            }
        }
        SettingCard {
            Layout.fillWidth: true
            description: qsTr("设置 ClassIsland 通知遮罩的显示时长。")
            title: qsTr("遮罩 (Mask) 显示时长")

            SpinBox {
                from: 0
                to: 60
                value: SettingsConfig.getCiMaskDuration("classisland")

                Component.onCompleted: {
                    value = SettingsConfig.getCiMaskDuration("classisland");
                }
                onValueChanged: SettingsConfig.setCiMaskDuration("classisland", value)
            }
            Text {
                text: qsTr("秒")
            }
        }
        SettingCard {
            Layout.fillWidth: true
            description: qsTr("设置 ClassIsland 通知正文的显示方式。")
            title: qsTr("正文 (Overlay) 显示方式")

            ComboBox {
                model: ListModel {
                    id: overlayTypeModel
                    ListElement {
                        text: qsTr("简单")
                        value: "simple"
                    }
                    ListElement {
                        text: qsTr("滚动")
                        value: "rolling"
                    }
                    ListElement {
                        text: qsTr("自动检测")
                        value: "auto"
                    }
                }
                // 强制设置 text 为文字属性
                textRole: "text"


                currentIndex: SettingsConfig.getCiOverlayTypeIndex()

                Component.onCompleted: {
                    currentIndex = SettingsConfig.getCiOverlayTypeIndex();
                }

                onCurrentIndexChanged: {
                    SettingsConfig.setCiOverlayType(overlayTypeModel.get(currentIndex).value);
                }

            }
        }
        SettingCard {
            Layout.fillWidth: true
            description: qsTr("设置 ClassIsland 设置正文的显示时长。")
            title: qsTr("正文 (Overlay) 显示时长")

            SpinBox {
                from: 0
                to: 60
                value: SettingsConfig.getCiOverlayDuration()

                Component.onCompleted: {
                    value = SettingsConfig.getCiOverlayDuration();
                }
                onValueChanged: SettingsConfig.setCiOverlayDuration(value)
            }
            Text {
                text: qsTr("秒")
            }
        }
    }
    Connections {
        function onConnectivityUpdated(method, connectivity) {
            if (method === "classisland") {
                notConnectedInfo.visible = connectivity === "NotConnected";
                connectedInfo.visible = connectivity === "Connected";
                notRunningInfo.visible = connectivity === "NotRunning";
            }
        }

        target: SettingsService
    }
}