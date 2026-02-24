import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI

Clip {
    id: resultPropertyClip

    property string propertyName: ""
    property string propertyValue: ""

    backgroundColor: Theme.currentTheme.colors.controlColor
    borderColor: Theme.currentTheme.colors.controlBorderColor
    borderWidth: 1
    height: implicitHeight
    implicitHeight: 62
    radius: 8
    width: parent.width

    RowLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        ColumnLayout {
            Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft
            Layout.fillWidth: true
            spacing: 3

            Text {
                color: Theme.currentTheme.colors.textColor
                font.bold: true
                font.pixelSize: 15
                text: propertyName
            }
            Text {
                color: Theme.currentTheme.colors.textSecondaryColor
                font.pixelSize: 12
                text: propertyValue
            }
        }
        Icon {
            Layout.alignment: Qt.AlignVCenter | Qt.AlignRight
            icon: "ic_fluent_add_20_regular"
        }
    }
}

