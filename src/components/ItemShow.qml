import QtQuick
import QtQuick.Layouts
import RinUI

Frame {
    property string stuName: ""
    property string stuAvatar: ""
    property var stuProperties: []

    padding: 16

    contentItem: ColumnLayout {
        spacing: 12
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.alignment: Qt.AlignTop | Qt.AlignLeft

        ColumnLayout{spacing: 6

        Avatar {
            size: 64
            source: stuAvatar
            text: stuName !== "" ? stuName : qsTr("无")
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
        }

        Text {
            text: stuName !== "" ? stuName : qsTr("未抽选")
            font.bold: true
            font.pixelSize: 32
            horizontalAlignment: Text.AlignLeft
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
        }}

        ColumnLayout {
            spacing: 4
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            visible: stuProperties && stuProperties.length > 0

            Repeater {
                model: stuProperties
                delegate: ColumnLayout {
                    spacing: 3
                    Layout.fillWidth: true

                    Text {
                        text: modelData.name
                        font.pixelSize: 14
                        Layout.alignment: Qt.AlignLeft
                    }

                    Text {
                        text: modelData.value
                        font.pixelSize: 16
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignLeft
                    }
                }
            }
        }
    }
}