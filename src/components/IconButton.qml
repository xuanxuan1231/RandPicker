import QtQuick
import QtQuick.Layouts
import RinUI

Button {
    id: root

    property string iconName: ""

    Layout.fillWidth: true
    Layout.preferredHeight: 50

    contentItem: Column {
        anchors.centerIn: parent
        spacing: 2

        Icon {
            anchors.horizontalCenter: parent.horizontalCenter
            color: Colors.get("textColor")
            name: root.iconName
            visible: root.iconName !== ""
            size: 20
        }
        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            color: Colors.get("textColor")
            font.pixelSize: 12
            text: root.text
        }
    }
}
