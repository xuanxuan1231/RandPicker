import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI

Clip {
    id: resultPropertyClip

    property string propertyName: ""
    property string propertyValue: ""

    width: parent.width
    implicitHeight: 62
    height: implicitHeight

    backgroundColor: Theme.currentTheme.colors.controlColor
    radius: 8
    borderColor: Theme.currentTheme.colors.controlBorderColor
    borderWidth: 1

    RowLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        ColumnLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft
            spacing: 3
            Text {
                text: propertyName
                font.bold: true
                color: Theme.currentTheme.colors.textColor
                font.pixelSize: 15
            }
            Text {
                text: propertyValue
                color: Theme.currentTheme.colors.textSecondaryColor
                font.pixelSize: 12
            }
        }
        Icon {
            icon: "ic_fluent_add_20_regular"
            Layout.alignment: Qt.AlignVCenter | Qt.AlignRight
        }
    }
}

