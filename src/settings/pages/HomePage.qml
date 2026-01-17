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
        width: 350
        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel

        property var allProps: ({})
        property var propNames: []

        onOpened: {
            allProps = StudentsConfig.getAllAvailableProperties();
            propNames = Object.keys(allProps);
            propNameCombo.model = propNames;
            updateValueModel();
        }

        function updateValueModel() {
            if (propNameCombo.currentText && allProps[propNameCombo.currentText]) {
                propValueCombo.model = allProps[propNameCombo.currentText];
            } else {
                propValueCombo.model = [];
            }
        }

        ColumnLayout {
            width: parent.width
            spacing: 15

            Label {
                text: qsTr("选择筛选属性:")
                font.bold: true
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 10
                Label { text: qsTr("属性名:") }
                ComboBox {
                    id: propNameCombo
                    Layout.fillWidth: true
                    onCurrentTextChanged: advancedDialog.updateValueModel()
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 10
                Label { text: qsTr("属性值:") }
                ComboBox {
                    id: propValueCombo
                    Layout.fillWidth: true
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 10
                Label { text: qsTr("筛选模式:") }
                ComboBox {
                    id: filterModeCombo
                    Layout.fillWidth: true
                    model: [qsTr("包含 (符合条件)"), qsTr("排除 (不符合条件)")]
                }
            }
            
            Label {
                text: filterModeCombo.currentIndex === 0 ? qsTr("提示: 系统将只从具有该属性值的学生中进行抽选") : qsTr("提示: 系统将从不具有该属性值的学生中进行抽选")
                font.pixelSize: 11
                color: "gray"
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
            }
        }

        onAccepted: {
            if (propNameCombo.currentText && propValueCombo.currentText) {
                let filters = [{"name": propNameCombo.currentText, "value": propValueCombo.currentText}];
                let exclude = filterModeCombo.currentIndex === 1;
                const result = ChoiceMaker.advancedChoose(parseInt(stuCount.text), filters, false, exclude);
                homePage.selectedStudents = result && result.length ? result : [];
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