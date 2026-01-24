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
            page: Qt.resolvedUrl("pages/HomePage.qml")
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