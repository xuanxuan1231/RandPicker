import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import RinUI

Dialog {
    id: root
    property string notifyOption: ""

    // Insert snippet into a TextField at current cursor position (or replace selection)
    function insertAtCursor(field, snippet) {
        if (!field)
            return;

        // Ensure the target field gets focus so cursorPosition/selection are meaningful
        if (field.forceActiveFocus)
            field.forceActiveFocus();

        var start = field.cursorPosition;
        var end = field.cursorPosition;

        // selectionStart/selectionEnd exist on QtQuick Controls TextField
        if (field.selectionStart !== undefined && field.selectionEnd !== undefined) {
            start = Math.min(field.selectionStart, field.selectionEnd);
            end = Math.max(field.selectionStart, field.selectionEnd);
        }

        var t = field.text || "";
        field.text = t.slice(0, start) + snippet + t.slice(end);
        field.cursorPosition = start + snippet.length;
    }

    title: qsTr("为 %1 编辑通知格式").arg(notifyOption)
    standardButtons: Dialog.Ok | Dialog.Cancel

    onOpened: {
        if (notifyOption) {
            var formatData = SettingsConfig.getNotifyFormat(notifyOption);
            if (formatData) {
                titleField.text = formatData.title || "";
                contentField.text = formatData.body || "";

                if (formatData.names) {
                    separatorField.text = formatData.names.separator || ",";
                } else {
                    separatorField.text = ",";
                }

                if (formatData.suffix) {
                    personSuffixField.text = formatData.suffix.person || "";
                    groupSuffixField.text = formatData.suffix.group || "";
                } else {
                    personSuffixField.text = "";
                    groupSuffixField.text = "";
                }
            }
        }
    }

    RowLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true

        ColumnLayout {
            Layout.fillHeight: true
            Layout.preferredWidth: parent.width * 0.6

            Text {
                text: qsTr("标题格式")
                font.bold: true
                font.pixelSize: 14
            }

            TextField {
                id: titleField
                Layout.fillWidth: true
                placeholderText: qsTr("标题格式")
            }

            Text {
                text: qsTr("正文格式")
                font.bold: true
                font.pixelSize: 14
            }

            TextField {
                id: contentField
                Layout.fillWidth: true
                placeholderText: qsTr("正文格式")
            }

            Frame {
                Layout.fillWidth: true
                Layout.fillHeight: true
                ColumnLayout {
                    anchors.fill: parent
                    Text {
                        text: qsTr("属性设置")
                        font.bold: true
                        font.pixelSize: 18
                        Layout.alignment: Qt.AlignLeft
                    }
                    SettingExpander {
                        Layout.fillWidth: true
                        title: "{suffix}"
                        description: qsTr("称呼后缀")
                        expanded: true
                        enabled: false

                        content: Text {
                            text: "1" + personSuffixField.text + "/" + "1" + groupSuffixField.text
                        }

                        SettingItem {
                            title: qsTr("学生")
                            TextField {
                                id: personSuffixField
                                Layout.fillWidth: true
                                placeholderText: qsTr("位同学")
                            }
                        }

                        SettingItem {
                            title: qsTr("小组")
                            TextField {
                                id: groupSuffixField
                                Layout.fillWidth: true
                                placeholderText: qsTr("个小组")
                            }
                        }
                    }

                    SettingExpander {
                        Layout.fillWidth: true
                        title: "{names}"
                        description: qsTr("学生列表格式")
                        expanded: false
                        enabled: false

                        content: Text {
                            text: qsTr("分隔符：%1").arg(separatorField.text)
                        }

                        SettingItem {
                            title: qsTr("分隔符")
                            TextField {
                                id: separatorField
                                Layout.fillWidth: true
                                placeholderText: qsTr(",")
                            }
                        }
                    }
                }
            }
        }

        Frame {
            Layout.fillHeight: true
            Layout.preferredWidth: parent.width * 0.4
            ColumnLayout {
                anchors.fill: parent
                RowLayout {
                    Layout.fillWidth: true
                    Text {
                        text: qsTr("内容填充")
                        font.bold: true
                        font.pixelSize: 18
                        Layout.alignment: Qt.AlignLeft
                    }

                    Item {
                        Layout.fillWidth: true
                    }

                    ComboBox {
                        id: typeComboBox
                        Layout.alignment: Qt.AlignRight
                        Layout.preferredWidth: 75
                        model: [qsTr("标题"), qsTr("正文")]
                        currentIndex: 0
                    }
                }

                ResultPropertyClip {
                    propertyName: qsTr("数量")
                    propertyValue: "{count}"
                    onClicked: {
                        if (typeComboBox.currentIndex === 0) {
                            insertAtCursor(titleField, "{count}");
                        } else {
                            insertAtCursor(contentField, "{count}");
                        }
                    }
                    Layout.fillWidth: true
                }
                ResultPropertyClip {
                    propertyName: qsTr("后缀")
                    propertyValue: "{suffix}"
                    Layout.fillWidth: true
                    onClicked: {
                        if (typeComboBox.currentIndex === 0) {
                            insertAtCursor(titleField, "{suffix}");
                        } else {
                            insertAtCursor(contentField, "{suffix}");
                        }
                    }
                }
                ResultPropertyClip {
                    propertyName: qsTr("学生列表")
                    propertyValue: "{names}"
                    onClicked: {
                        if (typeComboBox.currentIndex === 0) {
                            insertAtCursor(titleField, "{names}");
                        } else {
                            insertAtCursor(contentField, "{names}");
                        }
                    }
                    Layout.fillWidth: true
                }

                Item {
                    Layout.fillHeight: true
                }
            }
        }
    }


    onAccepted: {
        var newFormat = {
            title: titleField.text,
            body: contentField.text,
            names: {
                separator: separatorField.text
            },
            suffix: {
                person: personSuffixField.text,
                group: groupSuffixField.text
            }
        };
        SettingsConfig.setNotifyFormat(notifyOption, newFormat)
    }

}