import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI

FluentPage {
    id: appearanceSettingsPage

    title: qsTr("外观 & 行为")

    ColumnLayout {
        Layout.fillWidth: true

        Text {
            Layout.alignment: Qt.AlignLeft
            Layout.fillWidth: true
            font.bold: true
            font.pixelSize: 18
            text: qsTr("基本")
        }

        SettingExpander {
            Layout.fillWidth: true
            icon.name: "ic_fluent_window_shield_20_regular"
            title: qsTr("使用管理员权限")
            description: qsTr("使用管理员权限运行后，可以使用 UI Access 超级置顶。\n仅对 Windows 有效。")

            SettingItem {
                title: qsTr("使用管理员权限重新启动")

                Row {
                    spacing: 8
                    anchors.verticalCenter: parent ? parent.verticalCenter : undefined

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        visible: Qt.platform.os === "windows" && AppMain.isAdmin
                        color: Theme.currentTheme.colors.textSecondaryColor
                        text: qsTr("当前已以管理员身份运行")
                    }

                    Button {
                        text: qsTr("立即重新启动")
                        enabled: Qt.platform.os === "windows" && !AppMain.isAdmin
                        onClicked: {
                            AppMain.restartAsAdmin();
                        }
                    }

                }

            }

            content: CheckBox {
                text: qsTr("使用管理员权限启动")
                checked: SettingsConfig.getRunAsAdmin()
                onCheckedChanged: {
                    if (checked === SettingsConfig.getRunAsAdmin())
                        return;

                    SettingsConfig.setRunAsAdmin(checked);
                }
                enabled: Qt.platform.os === "windows"
            }

        }

    }

    ColumnLayout {
        Layout.fillWidth: true

        Text {
            Layout.alignment: Qt.AlignLeft
            Layout.fillWidth: true
            font.bold: true
            font.pixelSize: 18
            text: qsTr("外观")
        }

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_dark_theme_20_regular"
            title: qsTr("主题")
            description: qsTr("选择应用的主题")

            ComboBox {
                id: themeComboBox

                Layout.preferredWidth: 120
                model: [qsTr("跟随系统"), qsTr("浅色"), qsTr("深色")]
                // Theme.getTheme() 返回 "Light" "Dark" "Auto"
                // Theme.setTheme(Theme.mode.Light/Dark/Auto)
                currentIndex: {
                    var t = Theme.getTheme();
                    if (t === "Auto")
                        return 0;

                    if (t === "Light")
                        return 1;

                    if (t === "Dark")
                        return 2;

                    return 0;
                }
                onCurrentIndexChanged: {
                    if (currentIndex === 0)
                        Theme.setTheme(Theme.mode.Auto);
                    else if (currentIndex === 1)
                        Theme.setTheme(Theme.mode.Light);
                    else if (currentIndex === 2)
                        Theme.setTheme(Theme.mode.Dark);
                }
            }

        }

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_color_20_regular"
            title: qsTr("主题色")
            description: qsTr("选择应用的主题色")

            Row {
                spacing: 3

                Rectangle {
                    id: themeColorRect

                    width: 40
                    height: colorButton.implicitHeight
                    radius: 4
                    color: Theme.getThemeColor()
                }

                Button {
                    id: colorButton

                    text: qsTr("选择颜色")
                    onClicked: colorPickerDialog.open()
                }

            }

        }

    }

    ColumnLayout {
        Layout.fillWidth: true

        Text {
            Layout.alignment: Qt.AlignLeft
            Layout.fillWidth: true
            font.bold: true
            font.pixelSize: 18
            text: qsTr("浮窗")
        }

        SettingCard {
            Layout.fillWidth: true
            title: qsTr("缩放")
            description: qsTr("设置浮窗整体的缩放大小。不影响主界面。")

            RowLayout {
                Layout.preferredWidth: parent.width * 0.4
                spacing: 8

                Text {
                    color: Theme.currentTheme.colors.textSecondaryColor
                    font.pixelSize: 12
                    text: "60%"
                }

                Slider {
                    id: widgetScaleSlider

                    Layout.fillWidth: true
                    from: 0.6
                    stepSize: 0.05
                    to: 2
                    value: SettingsConfig.getWidgetScale()
                    onMoved: {
                        SettingsConfig.setWidgetScale(value);
                    }
                }

                Connections {
                    function onWidgetScaleChanged() {
                        if (!widgetScaleSlider.pressed)
                            widgetScaleSlider.value = SettingsConfig.getWidgetScale();

                    }

                    target: SettingsConfig
                }

                Text {
                    color: Theme.currentTheme.colors.textColor
                    font.pixelSize: 12
                    text: Math.round(widgetScaleSlider.value * 100) + "%"
                }

                ToolButton {
                    flat: true
                    icon.name: "ic_fluent_arrow_reset_20_regular"
                    visible: Math.abs(widgetScaleSlider.value - 1) > 0.001
                    onClicked: {
                        SettingsConfig.setWidgetScale(1);
                    }

                    ToolTip {
                        delay: 500
                        text: qsTr("重置为 100%")
                        visible: parent.hovered
                    }

                }

                Text {
                    color: Theme.currentTheme.colors.textSecondaryColor
                    font.pixelSize: 12
                    text: "200%"
                }

            }

        }

        SettingExpander {
            Layout.fillWidth: true
            title: qsTr("显示内容")
            description: qsTr("设置浮窗中显示的按钮和选项。")

            SettingItem {
                title: qsTr("显示“抽人”按钮")

                Switch {
                    checked: SettingsConfig.showDrawButton
                    onCheckedChanged: {
                        if (checked !== SettingsConfig.showDrawButton)
                            SettingsConfig.setShowDrawButton(checked);

                    }
                }

            }

            SettingItem {
                title: qsTr("显示“抽组”按钮")

                Switch {
                    checked: SettingsConfig.showGroupButton
                    onCheckedChanged: {
                        if (checked !== SettingsConfig.showGroupButton)
                            SettingsConfig.setShowGroupButton(checked);

                    }
                }

            }

            SettingItem {
                title: qsTr("显示“更多”按钮")

                Switch {
                    checked: SettingsConfig.showMoreButton
                    onCheckedChanged: {
                        if (checked !== SettingsConfig.showMoreButton)
                            SettingsConfig.setShowMoreButton(checked);

                    }
                }

            }

            SettingItem {
                title: qsTr("显示“记忆”设置")

                Switch {
                    checked: SettingsConfig.showMemoryRow
                    onCheckedChanged: {
                        if (checked !== SettingsConfig.showMemoryRow)
                            SettingsConfig.setShowMemoryRow(checked);

                    }
                }

            }

        }

    }

    Dialog {
        id: colorPickerDialog

        title: qsTr("为 RandPicker 选择主题色")
        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel
        Component.onCompleted: {
            colorPicker.color = Theme.getThemeColor();
        }
        onAccepted: {
            Theme.setThemeColor(colorPicker.color);
            themeColorRect.color = Theme.getThemeColor();
        }

        ColorPicker {
            id: colorPicker
        }

    }

}
