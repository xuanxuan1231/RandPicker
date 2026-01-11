import QtQuick
import QtQuick.Layouts
import QtQuick.Window as QQW
import RinUI

QQW.Window {
    id: widget

    property int itemCount: 5

    width: 75
    height: 105
    visible: true
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Widget | Qt.X11BypassWindowManagerHint
    color: "transparent"
    title: qsTr("RandPicker Widget")

    Rectangle {
        anchors.fill: parent
        radius: 12
        color: Colors.get("backgroundColor")
        border.color: Colors.get("windowBorderColor")
        border.width: 1
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 6
        spacing: 5

        RowLayout {
            Text {
                text: itemCount
                font.pixelSize: 12
                font.bold: true
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            RowLayout {
                Layout.alignment: Qt.AlignRight
                Layout.fillWidth: true
                spacing: 1
                Button {
                    flat: true
                    text: "+"
                    Layout.preferredWidth: 16
                    Layout.preferredHeight: 22
                    font.pixelSize: 12
                    onClicked: {
                        if (itemCount < 99) {
                            itemCount += 1;
                        }
                    }
                }
                Button {
                    flat: true
                    text: "-"
                    Layout.preferredWidth: 16
                    Layout.preferredHeight: 22
                    font.pixelSize: 12
                    onClicked: {
                        if (itemCount > 1) {
                            itemCount -= 1;
                        }
                    }
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 6

            Button {
                id: pickButton

                text: "人"
                Layout.preferredHeight: 26
                font.pixelSize: 12
                Layout.fillWidth: true
                onClicked: {
                    ChoiceMaker.choosePeople(itemCount);
                }
            }

            Button {
                id: itemButton

                text: "组"
                Layout.preferredHeight: 26
                font.pixelSize: 12
                Layout.fillWidth: true
                onClicked: {
                    console.log("抽组");
                }
            }

        }

    }

}
