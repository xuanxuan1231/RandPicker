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

    standardButtons: Dialog.Ok | Dialog.Cancel
    title: qsTr("为 %1 编辑通知格式").arg(notifyOption)

    // Fixed dimensions to prevent dynamic height calculations
    width: 700

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
        SettingsConfig.setNotifyFormat(notifyOption, newFormat);
    }
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
        Layout.fillHeight: true
        Layout.fillWidth: true
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
                    font.bold: true
                    font.pixelSize: 14
                    text: qsTr("标题格式")
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
                    font.bold: true
                    font.pixelSize: 14
                    text: qsTr("正文格式")
                }
                TextField {
                    id: contentField

                    Layout.fillWidth: true
                    placeholderText: qsTr("正文格式")
                }
            }

            // Property settings section - Fixed height, no expander
            Frame {
                Layout.fillHeight: true
                Layout.fillWidth: true

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 8
                    spacing: 12

                    Text {
                        Layout.alignment: Qt.AlignLeft
                        font.bold: true
                        font.pixelSize: 16
                        text: qsTr("属性设置")
                    }
                    ScrollView {
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                        clip: true
                        contentWidth: availableWidth

                        ColumnLayout {
                            spacing: 12
                            width: parent.width

                            // Suffix settings card
                            Clip {
                                Layout.fillWidth: true
                                backgroundColor: Theme.currentTheme.colors.controlColor
                                borderColor: Theme.currentTheme.colors.controlBorderColor
                                borderWidth: 1
                                implicitHeight: suffixLayout.implicitHeight + 24
                                radius: 6

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
                                            color: Theme.currentTheme.colors.textColor
                                            font.bold: true
                                            font.pixelSize: 14
                                            text: "{suffix}"
                                        }
                                        Text {
                                            color: Theme.currentTheme.colors.textSecondaryColor
                                            font.pixelSize: 12
                                            text: qsTr("称呼后缀")
                                        }
                                        Item {
                                            Layout.fillWidth: true
                                        }
                                        Text {
                                            color: Theme.currentTheme.colors.textSecondaryColor
                                            font.pixelSize: 12
                                            text: "1" + personSuffixField.text + " / " + "1" + groupSuffixField.text
                                        }
                                    }

                                    // Divider
                                    Rectangle {
                                        Layout.fillWidth: true
                                        color: Theme.currentTheme.colors.dividerColor
                                        height: 1
                                    }

                                    // Person suffix
                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: 12

                                        Text {
                                            Layout.preferredWidth: 50
                                            color: Theme.currentTheme.colors.textColor
                                            font.pixelSize: 13
                                            text: qsTr("学生")
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
                                            Layout.preferredWidth: 50
                                            color: Theme.currentTheme.colors.textColor
                                            font.pixelSize: 13
                                            text: qsTr("小组")
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
                                backgroundColor: Theme.currentTheme.colors.controlColor
                                borderColor: Theme.currentTheme.colors.controlBorderColor
                                borderWidth: 1
                                implicitHeight: namesLayout.implicitHeight + 24
                                radius: 6

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
                                            color: Theme.currentTheme.colors.textColor
                                            font.bold: true
                                            font.pixelSize: 14
                                            text: "{names}"
                                        }
                                        Text {
                                            color: Theme.currentTheme.colors.textSecondaryColor
                                            font.pixelSize: 12
                                            text: qsTr("学生列表格式")
                                        }
                                        Item {
                                            Layout.fillWidth: true
                                        }
                                        Text {
                                            color: Theme.currentTheme.colors.textSecondaryColor
                                            font.pixelSize: 12
                                            text: qsTr("分隔符：%1").arg(separatorField.text)
                                        }
                                    }

                                    // Divider
                                    Rectangle {
                                        Layout.fillWidth: true
                                        color: Theme.currentTheme.colors.dividerColor
                                        height: 1
                                    }

                                    // Separator setting
                                    RowLayout {
                                        Layout.fillWidth: true
                                        spacing: 12

                                        Text {
                                            Layout.preferredWidth: 50
                                            color: Theme.currentTheme.colors.textColor
                                            font.pixelSize: 13
                                            text: qsTr("分隔符")
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
                        Layout.alignment: Qt.AlignLeft
                        font.bold: true
                        font.pixelSize: 16
                        text: qsTr("内容填充")
                    }
                    Item {
                        Layout.fillWidth: true
                    }
                    ComboBox {
                        id: typeComboBox

                        Layout.alignment: Qt.AlignRight
                        Layout.preferredWidth: 75
                        currentIndex: 0
                        model: [qsTr("标题"), qsTr("正文")]
                    }
                }
                ResultPropertyClip {
                    Layout.fillWidth: true
                    propertyName: qsTr("数量")
                    propertyValue: "{count}"

                    onClicked: {
                        if (typeComboBox.currentIndex === 0) {
                            insertAtCursor(titleField, "{count}");
                        } else {
                            insertAtCursor(contentField, "{count}");
                        }
                    }
                }
                ResultPropertyClip {
                    Layout.fillWidth: true
                    propertyName: qsTr("后缀")
                    propertyValue: "{suffix}"

                    onClicked: {
                        if (typeComboBox.currentIndex === 0) {
                            insertAtCursor(titleField, "{suffix}");
                        } else {
                            insertAtCursor(contentField, "{suffix}");
                        }
                    }
                }
                ResultPropertyClip {
                    Layout.fillWidth: true
                    propertyName: qsTr("学生列表")
                    propertyValue: "{names}"

                    onClicked: {
                        if (typeComboBox.currentIndex === 0) {
                            insertAtCursor(titleField, "{names}");
                        } else {
                            insertAtCursor(contentField, "{names}");
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
