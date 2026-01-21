import QtQuick
import QtQuick.Layouts
import RinUI

FluentPage {
    id: notificationSettingsPage

    title: qsTr("通知和集成")

    ColumnLayout {
        Layout.fillHeight: true
        Layout.fillWidth: true

        SettingCard {
            Layout.fillWidth: true
            description: qsTr("如果自定义的通知方案都不可用，将回退到系统原生通知方案。")
            title: qsTr("启用备选通知方案")

            Switch {
                checked: SettingsConfig.getNotifyFallback()
                onCheckedChanged: SettingsConfig.setNotifyFallback(checked)
            }
        }
        Segmented {
            id: segmented

            Layout.fillWidth: true
            enabled: true
            width: parent.width

            Repeater {
                id: rep

                model: [
                    {
                        "name": qsTr("RandPicker"),
                        "value": "randpicker",
                        "page": Qt.resolvedUrl("integrations/RandPicker.qml")
                    },
                    {
                        "name": qsTr("系统原生"),
                        "value": "native",
                        "page": Qt.resolvedUrl("integrations/Native.qml")
                    },
                    {
                        "name": qsTr("ClassIsland"),
                        "value": "classisland",
                        "page": Qt.resolvedUrl("integrations/ClassIsland.qml")
                    },
                    {
                        "name": qsTr("Class Widgets"),
                        "value": "classwidgets",
                        "page": Qt.resolvedUrl("integrations/ClassWidgets.qml")
                    }
                ]

                Component.onCompleted: {
                    // 选中第一个可用项
                    for (var i = 0; i < rep.count; i++) {
                        if (segmented.itemAt(i).enabled) {
                            segmented.currentIndex = i;
                            break;
                        }
                    }
                }

                SegmentedItem {
                    enabled: SettingsService.getNotifyAvailability(modelData.value)
                    //icon.name: modelData.icon
                    text: modelData.name
                }
            }
        }
        Loader {
            Layout.fillHeight: true
            Layout.fillWidth: true
            source: rep.model[segmented.currentIndex].page
        }
    }
}