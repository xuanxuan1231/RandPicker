import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI

FluentPage {
    id: notificationSettingsPage

    title: qsTr("通知 & 集成")

    ColumnLayout {
        Layout.fillWidth: true

        SettingCard {
            id: settingCard
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
        Flickable {
            Layout.fillWidth: true
            // 精确计算剩余高度，避免触发 FluentPage 外层滚动
            // FluentPage 内部: container.topMargin=18, spacing=14, bottomPadding=24
            Layout.preferredHeight: notificationSettingsPage.height
                - (notificationSettingsPage.header ? notificationSettingsPage.header.height : 0)
                - notificationSettingsPage.bottomPadding
                - 18   // container topMargin
                - settingCard.height - 14  // settingCard + spacing
                - segmented.height - 14    // segmented + spacing
            Layout.maximumHeight: Layout.preferredHeight
            clip: true
            contentHeight: loader.item ? loader.item.implicitHeight : 0
            boundsBehavior: Flickable.StopAtBounds

            Loader {
                id: loader
                width: parent.width
                source: rep.model[segmented.currentIndex].page
                onLoaded: {
                    if (item) item.width = Qt.binding(function() { return loader.width; });
                }
            }

            ScrollBar.vertical: ScrollBar {}
        }
    }
}
