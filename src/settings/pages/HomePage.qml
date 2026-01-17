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

    Dialog {
        id: advancedDialog
        title: qsTr("高级抽选设置")
        anchors.centerIn: parent
        width: 300
        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel

        ColumnLayout {
            width: parent.width
            spacing: 10

            Label {
                text: qsTr("筛选属性 (JSON 格式):")
            }

            TextArea {
                id: filterInput
                Layout.fillWidth: true
                placeholderText: '[{"name":"bar","value":"foo"}]'
                wrapMode: TextEdit.Wrap
                selectByMouse: true
                font.family: "Monospace"
                implicitHeight: 100
                text: "[]"
            }
            
            Label {
                text: qsTr("提示: 输入属性名和对应的值进行筛选")
                font.pixelSize: 10
                color: "gray"
            }
        }

        onAccepted: {
            try {
                let filters = JSON.parse(filterInput.text);
                const result = ChoiceMaker.advancedChoose(parseInt(stuCount.text), filters, false);
                homePage.selectedStudents = result && result.length ? result : [];
            } catch (e) {
                console.error("JSON 解析错误: " + e);
            }
        }
    }

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
                    icon.name: "ic_fluent_arrow_up_20_regular"
                    onClicked: {
                        if (parseInt(stuCount.text) < 99) {
                            stuCount.text = (parseInt(stuCount.text) + 1).toString();
                        }
                    }
                    Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft
                }
                Text {
                    id: stuCount
                    Layout.fillWidth: true
                    horizontalAlignment: Text.AlignHCenter

                    font.pixelSize: 36
                    font.bold: true
                    text: "1"

                }
                ToolButton {
                    icon.name: "ic_fluent_arrow_down_20_regular"

                    onClicked: {
                        if (parseInt(stuCount.text) > 1) {
                            stuCount.text = (parseInt(stuCount.text) - 1).toString();
                        }
                    }

                    Layout.alignment: Qt.AlignVCenter | Qt.AlignRight
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
                text: qsTr("高级抽选")

                onClicked: {
                    advancedDialog.open();
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