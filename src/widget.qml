import QtQuick
import QtQuick.Layouts
import QtQuick.Window as QQW
import QtQuick.Window
import RinUI
import "./components"

QQW.Window {
    id: widget

    property int itemCount: 5
    property int snapThreshold: 50  // 吸附阈值（接近边缘50px时触发）
    property int visibleMargin: 10  // 屏幕内保留的可见像素
    property int screenPadding: 10  // 恢复到屏幕内时的边距
    property bool pendingPositionSave: false
    property bool positionApplied: false

    width: 75
    height: 157
    visible: true
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Widget | Qt.X11BypassWindowManagerHint
    color: "transparent"
    title: qsTr("RandPicker Widget")
    opacity: positionApplied ? 1 : 0

    // 位置动画
    ParallelAnimation {
        id: positionAnimation
        NumberAnimation {
            id: xAnimation
            target: widget
            property: "x"
            duration: 300
            easing.type: Easing.InOutQuad
        }
        NumberAnimation {
            id: yAnimation
            target: widget
            property: "y"
            duration: 300
            easing.type: Easing.InOutQuad
        }
        onStopped: {
            if (pendingPositionSave) {
                pendingPositionSave = false
                widget.savePosition()
            }
        }
    }

    // 带动画移动到指定位置
    function animateTo(newX, newY) {
        positionAnimation.stop()
        xAnimation.to = newX
        yAnimation.to = newY
        positionAnimation.start()
    }

    function getDefaultPosition() {
        return [Math.round((Screen.width - widget.width) / 2),
            Math.round((Screen.height - widget.height) / 2)]
    }

    function applySavedPosition() {
        if (positionApplied) {
            return
        }

        if (!SettingsConfig) {
            var fallback = getDefaultPosition()
            widget.x = fallback[0]
            widget.y = fallback[1]
            positionApplied = true
            return
        }

        var pos = SettingsConfig.getWidgetPosition()
        if (pos && pos.length === 2 && pos[0] != null && pos[1] != null) {
            widget.x = pos[0]
            widget.y = pos[1]
        } else {
            var defaultPos = getDefaultPosition()
            widget.x = defaultPos[0]
            widget.y = defaultPos[1]
        }
        positionApplied = true
    }

    function savePosition() {
        if (!SettingsConfig) {
            return
        }
        SettingsConfig.setWidgetPosition(Math.round(widget.x), Math.round(widget.y))
    }

    // 自动吸附到屏幕外（靠近边缘时移出屏幕，只保留10px可见）
    function snapToEdge() {
        var newX = widget.x
        var newY = widget.y
        var shouldSnap = false

        // 检查水平方向
        if (widget.x < snapThreshold) {
            newX = -widget.width + visibleMargin
            shouldSnap = true
        } else if (widget.x + widget.width > Screen.width - snapThreshold) {
            newX = Screen.width - visibleMargin
            shouldSnap = true
        }

        // 检查垂直方向
        if (widget.y < snapThreshold) {
            newY = -widget.height + visibleMargin
            shouldSnap = true
        } else if (widget.y + widget.height > Screen.height - snapThreshold) {
            newY = Screen.height - visibleMargin
            shouldSnap = true
        }

        if (shouldSnap) {
            animateTo(newX, newY)
            return true
        }
        return false
    }

    // 检查浮窗是否在屏幕外，如果在屏幕外则移回屏幕内
    function bringToScreen() {
        var newX = widget.x
        var newY = widget.y
        var isOutside = false

        // 检查水平方向
        if (widget.x + widget.width <= visibleMargin) {
            newX = screenPadding
            isOutside = true
        } else if (widget.x >= Screen.width - visibleMargin) {
            newX = Screen.width - widget.width - screenPadding
            isOutside = true
        }

        // 检查垂直方向
        if (widget.y + widget.height <= visibleMargin) {
            newY = screenPadding
            isOutside = true
        } else if (widget.y >= Screen.height - visibleMargin) {
            newY = Screen.height - widget.height - screenPadding
            isOutside = true
        }

        if (isOutside) {
            animateTo(newX, newY)
            return true
        }
        return false
    }

    MouseArea {
        id: dragArea
        anchors.fill: parent
        property point dragStartPos: Qt.point(0, 0)
        property bool isDragging: false

        onPressed: (mouse) => {
            dragStartPos = Qt.point(mouse.x, mouse.y)
            isDragging = false
            pendingPositionSave = false
            positionAnimation.stop()  // 停止可能正在进行的动画
        }

        onPositionChanged: (mouse) => {
            if (pressed) {
                var delta = Qt.point(mouse.x - dragStartPos.x, mouse.y - dragStartPos.y)
                widget.x += delta.x
                widget.y += delta.y
                isDragging = true
            }
        }

        onReleased: {
            if (isDragging) {
                var animated = widget.snapToEdge()
                if (animated) {
                    pendingPositionSave = true
                } else {
                    widget.savePosition()
                }
            } else {
                widget.bringToScreen()
            }
        }
    }

    Rectangle {
        anchors.fill: parent
        radius: 12
        color: Colors.get("backgroundColor")
        border.color: Colors.get("windowBorderColor")
        border.width: 1
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 5
        z: 1

        // 计数器和加减按钮
        RowLayout {
            Layout.fillWidth: true

            Text {
                text: itemCount
                color: Colors.get("textColor")
                font.pixelSize: 12
                font.bold: true
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            RowLayout {
                Layout.alignment: Qt.AlignRight
                spacing: 1

                Button {
                    flat: true
                    text: "+"
                    Layout.preferredWidth: 16
                    Layout.preferredHeight: 22
                    font.pixelSize: 12
                    enabled: itemCount < 99
                    onClicked: itemCount++
                }

                Button {
                    flat: true
                    text: "-"
                    Layout.preferredWidth: 16
                    Layout.preferredHeight: 22
                    font.pixelSize: 12
                    enabled: itemCount > 1
                    onClicked: itemCount--
                }
            }
        }

        // 功能按钮组
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 10

            IconButton {
                id: pickButton
                text: "人"
                iconName: "ic_fluent_people_20_regular"
                onClicked: ChoiceMaker.choosePeople(itemCount, true)
            }

            IconButton {
                id: itemButton
                text: "组"
                iconName: "ic_fluent_group_20_regular"
                onClicked: console.log(" [TODO] 抽组")
            }
        }
    }

    Item {
        id: watermark
        anchors {
            left: parent.left
            bottom: parent.bottom
            leftMargin: 8
            bottomMargin: 8
        }
        width: watermarkColumn.implicitWidth
        height: watermarkColumn.implicitHeight
        enabled: false
        z: 114514
        visible: VersionInfo.getAvailability()

        Column {
            id: watermarkColumn
            spacing: 1
            Text {
                text: qsTr("开发预览")
                color: Colors.get("textColor")
                opacity: 0.7
                font.pixelSize: 10
                font.bold: true
            }
            Text {
                text: "JellyCat"
                color: Colors.get("textColor")
                opacity: 0.67
                font.pixelSize: 9
            }
        }
    }

    Component.onCompleted: Qt.callLater(applySavedPosition)
    onVisibleChanged: {
        if (visible) {
            Qt.callLater(applySavedPosition)
        }
    }
}
