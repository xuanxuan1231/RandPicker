import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import RinUI

FluentPage {
    id: aboutPage
    title: qsTr("关于 RandPicker")


    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 12

        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 12

            Image {
                id: appIcon
                width: 80
                height: 80
                fillMode: Image.PreserveAspectFit
                Component.onCompleted: {
                    source = "qrc:/icons/randpicker.png"
                }
                visible: appIcon.source !== ""
            }

            ColumnLayout {
                spacing: 2
                Text {
                    text: qsTr("RandPicker")
                    font.pixelSize: 24
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                }
                Text {
                    text: qsTr("版本 %1").arg("1.0.0")
                    color: "#666666"
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                }
            }
        }
    }

}