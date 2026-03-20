import QtQuick
import QtQuick.Layouts
import QtQuick.Window as QQW
import QtQuick.Window
import RinUI
import "./components"

QQW.Window {


    id: widget

    property int itemCount: 5
    property bool pendingPositionSave: false
    property bool positionApplied: false
    property int screenPadding: 10  // 恢复到屏幕内时的边距
    property int snapThreshold: 50  // 吸附阈值（接近边缘50px时触发）
    property int visibleMargin: 10  // 屏幕内保留的可见像素
    property real baseWidgetWidth: 75
    property real widgetScale: SettingsConfig ? SettingsConfig.widgetScale : 1.0

    // 带动画移动到指定位置
    function animateTo(newX, newY) {
        positionAnimation.stop();
        xAnimation.to = newX;
        yAnimation.to = newY;
        positionAnimation.start();
    }
    function applySavedPosition() {
        if (positionApplied) {
            return;
        }

        if (!SettingsConfig) {
            var fallback = getDefaultPosition();
            widget.x = fallback[0];
            widget.y = fallback[1];
            positionApplied = true;
            return;
        }

        var pos = SettingsConfig.getWidgetPosition();
        if (pos && pos.length === 2 && pos[0] != null && pos[1] != null) {
            widget.x = pos[0];
            widget.y = pos[1];
        } else {
            var defaultPos = getDefaultPosition();
            widget.x = defaultPos[0];
            widget.y = defaultPos[1];
        }
        positionApplied = true;
    }

    // 检查浮窗是否在屏幕外，如果在屏幕外则移回屏幕内
    function bringToScreen() {
        var newX = widget.x;
        var newY = widget.y;
        var isOutside = false;

        // 检查水平方向
        if (widget.x + widget.width <= visibleMargin) {
            newX = screenPadding;
            isOutside = true;
        } else if (widget.x >= Screen.width - visibleMargin) {
            newX = Screen.width - widget.width - screenPadding;
            isOutside = true;
        }

        // 检查垂直方向
        if (widget.y + widget.height <= visibleMargin) {
            newY = screenPadding;
            isOutside = true;
        } else if (widget.y >= Screen.height - visibleMargin) {
            newY = Screen.height - widget.height - screenPadding;
            isOutside = true;
        }

        if (isOutside) {
            animateTo(newX, newY);
            return true;
        }
        return false;
    }
    function getDefaultPosition() {
        return [Math.round((Screen.width - widget.width) / 2), Math.round((Screen.height - widget.height) / 2)];
    }
    function savePosition() {
        if (!SettingsConfig) {
            return;
        }
        SettingsConfig.setWidgetPosition(Math.round(widget.x), Math.round(widget.y));
    }

    // 自动吸附到屏幕外（靠近边缘时移出屏幕，只保留10px可见）
    function snapToEdge() {
        var newX = widget.x;
        var newY = widget.y;
        var shouldSnap = false;

        // 检查水平方向
        if (widget.x < snapThreshold) {
            newX = -widget.width + visibleMargin;
            shouldSnap = true;
        } else if (widget.x + widget.width > Screen.width - snapThreshold) {
            newX = Screen.width - visibleMargin;
            shouldSnap = true;
        }

        // 检查垂直方向
        if (widget.y < snapThreshold) {
            newY = -widget.height + visibleMargin;
            shouldSnap = true;
        } else if (widget.y + widget.height > Screen.height - snapThreshold) {
            newY = Screen.height - visibleMargin;
            shouldSnap = true;
        }

        if (shouldSnap) {
            animateTo(newX, newY);
            return true;
        }
        return false;
    }

    color: "transparent"
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Widget | Qt.X11BypassWindowManagerHint
    height: Math.round(scaledContent.height * widgetScale)
    opacity: positionApplied ? 1 : 0
    title: qsTr("RandPicker")
    visible: true
    width: Math.round(scaledContent.width * widgetScale)

    Component.onCompleted: Qt.callLater(applySavedPosition)
    onVisibleChanged: {
        if (visible) {
            Qt.callLater(applySavedPosition);
        }
    }

    // 位置动画
    ParallelAnimation {
        id: positionAnimation

        onStopped: {
            if (pendingPositionSave) {
                pendingPositionSave = false;
                widget.savePosition();
            }
        }

        NumberAnimation {
            id: xAnimation

            duration: 300
            easing.type: Easing.InOutQuad
            property: "x"
            target: widget
        }
        NumberAnimation {
            id: yAnimation

            duration: 300
            easing.type: Easing.InOutQuad
            property: "y"
            target: widget
        }
    }
    MouseArea {
        id: dragArea

        property point dragStartPos: Qt.point(0, 0)
        property bool isDragging: false

        anchors.fill: parent

        onPositionChanged: mouse => {
            if (pressed) {
                var delta = Qt.point(mouse.x - dragStartPos.x, mouse.y - dragStartPos.y);
                widget.x += delta.x;
                widget.y += delta.y;
                isDragging = true;
            }
        }
        onPressed: mouse => {
            dragStartPos = Qt.point(mouse.x, mouse.y);
            isDragging = false;
            pendingPositionSave = false;
            positionAnimation.stop();  // 停止可能正在进行的动画
        }
        onReleased: {
            if (isDragging) {
                var animated = widget.snapToEdge();
                if (animated) {
                    pendingPositionSave = true;
                } else {
                    widget.savePosition();
                }
            } else {
                widget.bringToScreen();
            }
        }
    }
    Item {
        id: scaledContent

        height: mainLayout.implicitHeight + 20
        width: baseWidgetWidth

        transform: Scale {
            origin.x: 0
            origin.y: 0
            xScale: widget.widgetScale
            yScale: widget.widgetScale
        }

        Rectangle {
            anchors.fill: parent
            border.color: Colors.get("windowBorderColor")
            border.width: 1
            color: Colors.get("backgroundColor")
            radius: 12
        }
        ColumnLayout {
            id: mainLayout

            anchors.fill: parent
            anchors.margins: 10
            spacing: 5
            z: 1

        // 计数器和加减按钮
        RowLayout {
            Layout.fillWidth: true

            Text {
                Layout.fillWidth: true
                color: Colors.get("textColor")
                font.bold: true
                font.pixelSize: 12
                horizontalAlignment: Text.AlignHCenter
                text: itemCount
                verticalAlignment: Text.AlignVCenter
            }
            RowLayout {
                Layout.alignment: Qt.AlignRight
                spacing: 1

                Button {
                    Layout.preferredHeight: 22
                    Layout.preferredWidth: 16
                    enabled: itemCount < 99
                    flat: true
                    font.pixelSize: 12
                    text: "+"

                    onClicked: itemCount++
                }
                Button {
                    Layout.preferredHeight: 22
                    Layout.preferredWidth: 16
                    enabled: itemCount > 1
                    flat: true
                    font.pixelSize: 12
                    text: "-"

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

                iconName: "ic_fluent_people_20_regular"
                text: "人"
                visible: SettingsConfig.showDrawButton

                onClicked: ChoiceMaker.choosePeople(itemCount, true)
            }
            IconButton {
                id: itemButton

                iconName: "ic_fluent_group_20_regular"
                text: "组"
                visible: SettingsConfig.showGroupButton

                onClicked: console.log(" [TODO] 抽组")
            }
            RowLayout {
                Layout.fillWidth: true
                spacing: 6
                visible: SettingsConfig.showMemoryRow

                ToggleButton {
                    id: memoryToggle
                    property int textSize: 12
                    text: "记忆"
                    checked: ChoiceMaker.memoryEnabled
                    onClicked: ChoiceMaker.memoryEnabled = !ChoiceMaker.memoryEnabled

                    Component.onCompleted: contentItem.children[0].children[1].font.pixelSize = textSize

                    Layout.preferredHeight: Math.max((contentItem && contentItem.children && contentItem.children[0] &&
                        contentItem.children[0].children && contentItem.children[0].children[1]
                        ? contentItem.children[0].children[1].height : textSize) + 8, 22)

                    Layout.preferredWidth: Math.max(((contentItem && contentItem.children && contentItem.children[0])
                        ? contentItem.children[0].implicitWidth : textSize * 3) + 12, 32)
                }

                ToolButton {
                    id: memoryReset
                    flat: true
                    icon.name: "ic_fluent_arrow_sync_20_regular"
                    property int iconSize: 12
                    size: iconSize
                    Layout.preferredHeight: iconSize
                    Layout.preferredWidth: iconSize
                    onClicked: ChoiceMaker.resetMemory()
                }
            }
            IconButton {
                id: settingsButton

                Layout.preferredHeight: 25
                iconName: ""
                text: "···"
                visible: SettingsConfig.showMoreButton

                onClicked: AppMain.open_settings()
            }
            
        }
        }
        Item {
            id: watermark

        enabled: false
        height: watermarkColumn.implicitHeight
        visible: VersionInfo ? VersionInfo.getAvailability() : false
        width: watermarkColumn.implicitWidth
        z: 114514

            anchors {
                bottom: parent.bottom
                bottomMargin: 8
                left: parent.left
                leftMargin: 8
            }
            Column {
                id: watermarkColumn

            spacing: 1

                Text {
                    color: Colors.get("textColor")
                    font.bold: true
                    font.pixelSize: 10
                    opacity: 0.7
                    text: qsTr("开发预览")
                }
                Text {
                    color: Colors.get("textColor")
                    font.pixelSize: 9
                    opacity: 0.67
                    text: "JellyCat"
                }
            }
        }
    }
}
