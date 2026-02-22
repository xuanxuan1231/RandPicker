import QtQuick
import QtQuick.Layouts
import RinUI

Button {
    id: root

    property string iconName: ""

    Layout.fillWidth: true
    Layout.preferredHeight: 50

    contentItem: Column {
        spacing: 2
        anchors.centerIn: parent

        Icon {
            name: root.iconName
            size: 20
            anchors.horizontalCenter: parent.horizontalCenter
            color: Colors.get("textColor")
        }

        Text {
            text: root.text
            color: Colors.get("textColor")
            font.pixelSize: 12
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
