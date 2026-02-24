import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI

FluentWindow {
    id: root

    property string branch: VersionInfo.getBranchName()
    property string commitHash: VersionInfo.getCommitHash()

    height: 600
    minimumHeight: 400
    minimumWidth: 500
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
            icon: "ic_fluent_people_20_regular",
            page: Qt.resolvedUrl("pages/stuconfig/StudentManage.qml")
        },
        {
            title: qsTr("小组管理"),
            icon: "ic_fluent_people_team_20_regular",
            page: Qt.resolvedUrl("pages/stuconfig/GroupManage.qml")
        },
        {
            title: qsTr("配置管理"),
            icon: "ic_fluent_dismiss_20_regular",
            page: Qt.resolvedUrl("pages/stuconfig/FileManage.qml")
        },
        {
            title: qsTr("应用设置"),
            icon: "ic_fluent_settings_20_regular",
            page: Qt.resolvedUrl("pages/SettingsPage.qml"),
            position: Position.Bottom,
            subItems: [
                {
                    title: qsTr("外观 & 行为"),
                    icon: "ic_fluent_color_line_20_regular",
                    page: Qt.resolvedUrl("pages/settings/Appearance.qml")
                },
                {
                    title: qsTr("通知 & 集成"),
                    icon: "ic_fluent_notification_20_regular",
                    page: Qt.resolvedUrl("pages/settings/Notification.qml")
                },
                {
                    title: qsTr("高级"),
                    icon: "ic_fluent_settings_20_regular",
                    page: Qt.resolvedUrl("pages/settings/Advanced.qml")
                }
            ]
        },
        {
            title: qsTr("关于本产品"),
            icon: "ic_fluent_info_20_regular",
            page: Qt.resolvedUrl("pages/AboutPage.qml"),
            position: Position.Bottom
        }
    ]
    navigationView.navigationBar.collapsed: true
    navigationView.navigationBar.minimumExpandWidth: width + 1
    title: qsTr("RandPicker")
    visible: true
    width: 900

    Item {
        id: watermark

        enabled: false // ensure it never intercepts input
        height: watermarkColumn.implicitHeight
        visible: VersionInfo.getAvailability()
        width: watermarkColumn.implicitWidth
        z: 999

        anchors {
            bottom: parent.bottom
            bottomMargin: 12
            left: parent.left
            leftMargin: 12
        }
        Column {
            id: watermarkColumn

            spacing: 2

            Text {
                color: Colors.get("textColor")
                font.bold: true
                font.pixelSize: 14
                horizontalAlignment: Text.AlignLeft
                lineHeight: 1.1
                lineHeightMode: Text.ProportionalHeight
                text: qsTr("开发预览")
                wrapMode: Text.Wrap
            }
            Text {
                color: Colors.get("textColor")
                font.pixelSize: 11
                horizontalAlignment: Text.AlignLeft
                lineHeight: 1.1
                lineHeightMode: Text.ProportionalHeight
                opacity: 0.75
                text: "RandPicker 2.0 (Codename: JellyCat)"
                wrapMode: Text.Wrap
            }
            Text {
                color: Colors.get("textColor")
                font.pixelSize: 11
                horizontalAlignment: Text.AlignLeft
                lineHeight: 1.1
                lineHeightMode: Text.ProportionalHeight
                opacity: 0.65
                text: qsTr("您正位于 %1 分支的 %2 提交。").arg(branch).arg(commitHash)
                wrapMode: Text.Wrap
            }
        }
    }
}