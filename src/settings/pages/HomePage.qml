import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI
import "../../components"

FluentPage {
    id: homePage

    property var selectedStudents: []
    property int stuId: -1
    property string stuName: ""

    title: qsTr("主页")

    RowLayout {
        id: rootLayout

        Layout.fillHeight: true
        Layout.fillWidth: true
        height: parent.height
        spacing: 12
        width: parent.width

        ScrollView {
            id: resultScroll

            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.preferredWidth: rootLayout.width * 0.8
            clip: true

            Column {
                id: resultColumn

                spacing: 12
                width: resultScroll.availableWidth

                Repeater {
                    model: homePage.selectedStudents

                    delegate: ItemShow {
                        Layout.fillWidth: true
                        stuAvatar: modelData.avatar
                        stuName: modelData.name
                        stuProperties: modelData.properties
                        width: resultColumn.width
                    }
                }
                Text {
                    color: "#888"
                    font.pixelSize: 16
                    text: qsTr("尚未抽选")
                    visible: homePage.selectedStudents.length === 0
                }
            }
        }
        ColumnLayout {
            Layout.alignment: Qt.AlignTop
            Layout.fillHeight: true
            Layout.preferredWidth: rootLayout.width * 0.2
            spacing: 12

            RowLayout {
                ToolButton {
                    Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft
                    icon.name: "ic_fluent_arrow_up_20_regular"

                    onClicked: {
                        if (parseInt(stuCount.text) < 99) {
                            stuCount.text = (parseInt(stuCount.text) + 1).toString();
                        }
                    }
                }
                Text {
                    id: stuCount

                    Layout.fillWidth: true
                    font.bold: true
                    font.pixelSize: 36
                    horizontalAlignment: Text.AlignHCenter
                    text: "1"
                }
                ToolButton {
                    Layout.alignment: Qt.AlignVCenter | Qt.AlignRight
                    icon.name: "ic_fluent_arrow_down_20_regular"

                    onClicked: {
                        if (parseInt(stuCount.text) > 1) {
                            stuCount.text = (parseInt(stuCount.text) - 1).toString();
                        }
                    }
                }
            }
            RowLayout {
                Layout.fillWidth: true
                spacing: 6

                ToggleButton {
                    id: memoryToggle
                    checked: ChoiceMaker.memoryEnabled
                    text: qsTr("记忆")
                    Layout.preferredWidth: 40
                    Layout.preferredHeight: 36
                    font.pixelSize: 12
                    visible: SettingsConfig.showMemoryRow
                    onClicked: ChoiceMaker.setMemoryEnabled(!ChoiceMaker.memoryEnabled)
                }

                ToolButton {
                    icon.name: "ic_fluent_arrow_sync_20_regular"
                    icon.width: 20
                    icon.height: 20
                    Layout.preferredWidth: 36
                    Layout.preferredHeight: 36
                    visible: SettingsConfig.showMemoryRow
                    onClicked: ChoiceMaker.resetMemory()
                    ToolTip {
                        delay: 500
                        text: qsTr("重置记忆")
                        visible: parent.hovered
                    }
                }
            }
            Button {
                id: generalPick

                Layout.fillWidth: true
                font.bold: true
                highlighted: true
                implicitHeight: 48
                text: qsTr("开始抽选")

                onClicked: {
                    const result = ChoiceMaker.choosePeople(stuCount.text.toString(), false);
                    homePage.selectedStudents = result && result.length ? result : [];
                }
            }
            Button {
                Layout.fillWidth: true
                implicitHeight: 40
                text: qsTr("重置")

                onClicked: {
                    homePage.selectedStudents = [];
                }
            }
        }
    }
}