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

                fillMode: Image.PreserveAspectFit
                height: 80
                visible: appIcon.source !== ""
                width: 80

                Component.onCompleted: {
                    source = "qrc:/icons/randpicker.png";
                }
            }
            ColumnLayout {
                spacing: 2

                Text {
                    font.bold: true
                    font.pixelSize: 24
                    horizontalAlignment: Text.AlignHCenter
                    text: qsTr("RandPicker")
                }
                Text {
                    color: "#666666"
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                    text: qsTr("版本 %1").arg("1.0.0")
                }
            }
        }
    }
}