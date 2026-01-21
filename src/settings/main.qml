import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI

FluentWindow {
    id: root
    title: qsTr("RandPicker 设置")
    width: 900
    height: 600

    minimumWidth: 500
    minimumHeight: 400
    visible: true

    navigationItems: [
        {
            title: qsTr("主页"),
            icon: "ic_fluent_home_20_regular",
            page: Qt.resolvedUrl("pages/HomePage.qml"),
            position: Position.Top
        },
        {
            title: qsTr("抽取预览"),
            icon: "ic_fluent_eye_20_regular",
            page: Qt.resolvedUrl("pages/PreviewPage.qml"),
            position: Position.Top
        },
        {
            title: qsTr("学生管理"),
            icon: "ic_fluent_home_20_regular",
            page: Qt.resolvedUrl("pages/stuconfig/StudentManage.qml")
        },
        {
            title: qsTr("小组管理"),
            icon: "ic_fluent_people_team_20_regular",
            page: Qt.resolvedUrl("pages/stuconfig/GroupManage.qml")
        },
        {
            title:qsTr("配置管理"),
            icon: "ic_fluent_dismiss_20_regular",
            page: Qt.resolvedUrl("pages/stuconfig/FileManage.qml"),
        },
        {
            title: qsTr("应用设置"),
            icon: "ic_fluent_settings_20_regular",
            page: Qt.resolvedUrl("pages/SettingsPage.qml"),
            position: Position.Bottom,
            subItems: [
                {
                    title: qsTr("外观"),
                    icon: "ic_fluent_color_line_20_regular",
                    page: Qt.resolvedUrl("pages/settings/Appearance.qml")
                },
                {
                    title: qsTr("通知"),
                    icon: "ic_fluent_notification_20_regular",
                    page: Qt.resolvedUrl("pages/settings/Notification.qml")
                }
            ]
        },
        {
            title: qsTr("关于 RandPicker"),
            icon: "ic_fluent_info_20_regular",
            page: Qt.resolvedUrl("pages/AboutPage.qml"),
            position: Position.Bottom
        }
    ]

    navigationView.navigationBar.minimumExpandWidth: width + 1
    navigationView.navigationBar.collapsed: true
}