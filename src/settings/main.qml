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

    property string branch: GitInfo.getBranchName()
    property string commitHash: GitInfo.getCommitHash()

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

    Item {
        id: watermark
        z: 999
        anchors {
            left: parent.left
            bottom: parent.bottom
            leftMargin: 12
            bottomMargin: 12
        }
        width: watermarkColumn.implicitWidth
        height: watermarkColumn.implicitHeight
        enabled: false // ensure it never intercepts input
        visible: GitInfo.getAvailability()

        Column {
            id: watermarkColumn
            spacing: 2
            Text {
                text: qsTr("开发预览")
                color: Colors.get("textColor")
                font.pixelSize: 14
                font.bold: true
                lineHeight: 1.1
                lineHeightMode: Text.ProportionalHeight
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignLeft
            }
            Text {
                text: "RandPicker 2.0 (Codename: JellyCat)"
                color: Colors.get("textColor")
                opacity: 0.75
                font.pixelSize: 11
                lineHeight: 1.1
                lineHeightMode: Text.ProportionalHeight
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignLeft
            }
            Text {
                text: qsTr("您正位于 %1 分支的 %2 提交。").arg(branch).arg(commitHash)
                color: Colors.get("textColor")
                opacity: 0.65
                font.pixelSize: 11
                lineHeight: 1.1
                lineHeightMode: Text.ProportionalHeight
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignLeft
            }
        }
    }
}