import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import RinUI

Dialog {
    id: root
    property string notifyOption: ""

    // Fixed dimensions to prevent dynamic height calculations
    width: 700

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
        spacing: 16

        // Left panel: Format settings
        ColumnLayout {
            Layout.fillHeight: true
            Layout.preferredWidth: parent.width * 0.58
            spacing: 12

            // Title format section
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 6

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
            }

            // Content format section
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 6

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
            }

            // Property settings section - Fixed height, no expander
            Frame {
                Layout.fillWidth: true
                Layout.fillHeight: true

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 8
                    spacing: 12

                    Text {
                        text: qsTr("属性设置")
                        font.bold: true
                        font.pixelSize: 16
                        Layout.alignment: Qt.AlignLeft
                    }

                    ScrollView {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        contentWidth: availableWidth
                        clip: true

                        ColumnLayout {
                            width: parent.width
                            spacing: 12

                            // Suffix settings card
                            Clip {
                                Layout.fillWidth: true
                                implicitHeight: suffixLayout.implicitHeight + 24
                                backgroundColor: Theme.currentTheme.colors.controlColor
                                radius: 6
                                borderColor: Theme.currentTheme.colors.controlBorderColor
                                borderWidth: 1

                                ColumnLayout {
                                    id: suffixLayout
                                    anchors.fill: parent
                                    anchors.margins: 12
                                    spacing: 10

                                    // Header
                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: 8

                                        Text {
                                            text: "{suffix}"
                                            font.bold: true
                                            font.pixelSize: 14
                                            color: Theme.currentTheme.colors.textColor
                                        }

                                        Text {
                                            text: qsTr("称呼后缀")
                                            font.pixelSize: 12
                                            color: Theme.currentTheme.colors.textSecondaryColor
                                        }

                                        Item {
                                            Layout.fillWidth: true
                                        }

                                        Text {
                                            text: "1" + personSuffixField.text + " / " + "1" + groupSuffixField.text
                                            font.pixelSize: 12
                                            color: Theme.currentTheme.colors.textSecondaryColor
                                        }
                                    }

                                    // Divider
                                    Rectangle {
                                        Layout.fillWidth: true
                                        height: 1
                                        color: Theme.currentTheme.colors.dividerColor
                                    }

                                    // Person suffix
                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: 12

                                        Text {
                                            text: qsTr("学生")
                                            font.pixelSize: 13
                                            color: Theme.currentTheme.colors.textColor
                                            Layout.preferredWidth: 50
                                        }

                                        TextField {
                                            id: personSuffixField
                                            Layout.fillWidth: true
                                            placeholderText: qsTr("位同学")
                                        }
                                    }

                                    // Group suffix
                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: 12

                                        Text {
                                            text: qsTr("小组")
                                            font.pixelSize: 13
                                            color: Theme.currentTheme.colors.textColor
                                            Layout.preferredWidth: 50
                                        }

                                        TextField {
                                            id: groupSuffixField
                                            Layout.fillWidth: true
                                            placeholderText: qsTr("个小组")
                                        }
                                    }
                                }
                            }

                            // Names settings card
                            Clip {
                                Layout.fillWidth: true
                                implicitHeight: namesLayout.implicitHeight + 24
                                backgroundColor: Theme.currentTheme.colors.controlColor
                                radius: 6
                                borderColor: Theme.currentTheme.colors.controlBorderColor
                                borderWidth: 1

                                ColumnLayout {
                                    id: namesLayout
                                    anchors.fill: parent
                                    anchors.margins: 12
                                    spacing: 10

                                    // Header
                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: 8

                                        Text {
                                            text: "{names}"
                                            font.bold: true
                                            font.pixelSize: 14
                                            color: Theme.currentTheme.colors.textColor
                                        }

                                        Text {
                                            text: qsTr("学生列表格式")
                                            font.pixelSize: 12
                                            color: Theme.currentTheme.colors.textSecondaryColor
                                        }

                                        Item {
                                            Layout.fillWidth: true
                                        }

                                        Text {
                                            text: qsTr("分隔符：%1").arg(separatorField.text)
                                            font.pixelSize: 12
                                            color: Theme.currentTheme.colors.textSecondaryColor
                                        }
                                    }

                                    // Divider
                                    Rectangle {
                                        Layout.fillWidth: true
                                        height: 1
                                        color: Theme.currentTheme.colors.dividerColor
                                    }

                                    // Separator setting
                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: 12

                                        Text {
                                            text: qsTr("分隔符")
                                            font.pixelSize: 13
                                            color: Theme.currentTheme.colors.textColor
                                            Layout.preferredWidth: 50
                                        }

                                        TextField {
                                            id: separatorField
                                            Layout.fillWidth: true
                                            placeholderText: qsTr(",")
                                        }
                                    }
                                }
                            }

                            Item {
                                Layout.fillHeight: true
                            }
                        }
                    }
                }
            }
        }

        // Right panel: Content fill helpers
        Frame {
            Layout.fillHeight: true
            Layout.preferredWidth: parent.width * 0.38

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 8
                spacing: 12

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 8

                    Text {
                        text: qsTr("内容填充")
                        font.bold: true
                        font.pixelSize: 16
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
