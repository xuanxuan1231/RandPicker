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
            page: Qt.resolvedUrl("pages/HomePage.qml")
        }
    ]

    navigationView.navigationBar.minimumExpandWidth: width + 1
    navigationView.navigationBar.collapsed: true
}