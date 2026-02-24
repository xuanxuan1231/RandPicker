import QtQuick
import QtQuick.Layouts
import RinUI

Frame {
    property string stuAvatar: ""
    property string stuName: ""
    property var stuProperties: []

    padding: 16

    contentItem: ColumnLayout {
        Layout.alignment: Qt.AlignTop | Qt.AlignLeft
        Layout.fillHeight: true
        Layout.fillWidth: true
        spacing: 12

        ColumnLayout {
            spacing: 6

            Avatar {
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                size: 64
                source: stuAvatar
                text: stuName !== "" ? stuName : qsTr("无")
            }
            Text {
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                Layout.fillWidth: true
                font.bold: true
                font.pixelSize: 32
                horizontalAlignment: Text.AlignLeft
                text: stuName !== "" ? stuName : qsTr("未抽选")
            }
        }
        ColumnLayout {
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            Layout.fillWidth: true
            spacing: 4
            visible: stuProperties && stuProperties.length > 0

            Repeater {
                model: stuProperties

                delegate: ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 3

                    Text {
                        Layout.alignment: Qt.AlignLeft
                        font.pixelSize: 14
                        text: modelData.name
                    }
                    Text {
                        Layout.alignment: Qt.AlignLeft
                        Layout.fillWidth: true
                        font.pixelSize: 16
                        text: modelData.value
                    }
                }
            }
        }
    }
}