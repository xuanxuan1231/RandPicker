import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import RinUI

FluentPage {
    id: studentManagePage

    // 当前正在编辑的学生 GUID
    property string editingGuid: ""

    // FluentPage 内部布局常量（用于精确计算剩余高度）
    readonly property int pageContainerTopMargin: 18
    readonly property int pageContainerSpacing: 14

    // 学生列表模型（从写缓冲读取）
    property var studentsModel: []

    // 截断文本辅助
    function ellipsis(text, maxLen) {
        if (!text)
            return "";
        return text.length > maxLen ? text.substring(0, maxLen) + "…" : text;
    }

    // 跨平台本地文件路径转 URL
    function localFileUrl(path) {
        if (!path)
            return "";
        // Linux/macOS: /home/... → file:///home/...
        // Windows:     C:/...    → file:///C:/...
        if (path.charAt(0) === "/")
            return "file://" + path;
        return "file:///" + path;
    }
    function refreshStudents() {
        studentsModel = StudentsConfig.get_write_students();
    }

    title: qsTr("学生信息管理")

    // 禁用 FluentPage 内部 Flickable 滚动，让表格自行处理
    Component.onCompleted: {
        refreshStudents();
        // 遍历子项找到 Flickable 并禁用其交互式滚动
        for (var i = 0; i < studentManagePage.children.length; i++) {
            var child = studentManagePage.children[i];
            if (child.hasOwnProperty("flickableDirection") && child.hasOwnProperty("interactive")) {
                child.interactive = false;
                child.ScrollBar.vertical.policy = ScrollBar.AlwaysOff;
                break;
            }
        }
    }

    // ── 顶部操作栏 ──
    RowLayout {
        id: toolbarRow

        Layout.fillWidth: true
        spacing: 8

        Button {
            highlighted: true
            icon.name: "ic_fluent_add_20_regular"
            text: qsTr("添加学生")

            onClicked: {
                StudentsConfig.add_student("新学生", 1, true);
                refreshStudents();
            }
        }
        Item {
            Layout.fillWidth: true
        }
        Button {
            icon.name: "ic_fluent_arrow_sync_20_regular"
            text: qsTr("刷新")

            onClicked: {
                if (StudentsConfig.has_unsaved_changes()) {
                    discardConfirmDialog.open();
                } else {
                    StudentsConfig.reload_config();
                    refreshStudents();
                }
            }
        }
        Button {
            icon.name: "ic_fluent_save_20_regular"
            text: qsTr("保存")

            onClicked: {
                StudentsConfig.save_config();
                refreshStudents();
            }
        }
    }

    // ── 表格区域 ──
    Frame {
        // 精确计算剩余高度，使表格填满页面而非触发外层滚动
        Layout.fillWidth: true
        Layout.minimumHeight: 200
        Layout.preferredHeight: studentManagePage.height - (studentManagePage.header ? studentManagePage.header.height : 0) - studentManagePage.bottomPadding - pageContainerTopMargin - toolbarRow.height - pageContainerSpacing
        hoverable: false

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 0
            spacing: 0

            // 表头
            Rectangle {
                Layout.fillWidth: true
                color: Theme.currentTheme.colors.subtleColor
                implicitHeight: headerRow.implicitHeight + 16
                radius: Theme.currentTheme.appearance.smallRadius

                RowLayout {
                    id: headerRow

                    anchors.fill: parent
                    anchors.leftMargin: 12
                    anchors.rightMargin: 12
                    spacing: 4

                    Text {
                        Layout.preferredWidth: 100
                        color: Theme.currentTheme.colors.textSecondaryColor
                        font.pixelSize: 12
                        text: qsTr("姓名")
                    }
                    Text {
                        Layout.preferredWidth: 60
                        color: Theme.currentTheme.colors.textSecondaryColor
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        text: qsTr("权重")
                    }
                    Text {
                        Layout.preferredWidth: 50
                        color: Theme.currentTheme.colors.textSecondaryColor
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        text: qsTr("启用")
                    }
                    Text {
                        Layout.preferredWidth: 120
                        color: Theme.currentTheme.colors.textSecondaryColor
                        font.pixelSize: 12
                        text: qsTr("头像")
                    }
                    Text {
                        Layout.fillWidth: true
                        color: Theme.currentTheme.colors.textSecondaryColor
                        font.pixelSize: 12
                        text: qsTr("附加属性")
                    }
                    Text {
                        Layout.preferredWidth: 100
                        color: Theme.currentTheme.colors.textSecondaryColor
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        text: qsTr("操作")
                    }
                }
            }

            // 分割线
            Rectangle {
                Layout.fillWidth: true
                color: Theme.currentTheme.colors.dividerBorderColor
                height: 1
            }

            // 数据行
            ListView {
                id: studentListView

                Layout.fillHeight: true
                Layout.fillWidth: true
                clip: true
                model: studentManagePage.studentsModel

                delegate: Item {
                    required property int index
                    required property var modelData

                    height: rowLayout.implicitHeight + 12
                    width: studentListView.width

                    Rectangle {
                        anchors.fill: parent
                        color: rowMouseArea.containsMouse ? Theme.currentTheme.colors.subtleColor : "transparent"
                        radius: Theme.currentTheme.appearance.smallRadius

                        MouseArea {
                            id: rowMouseArea

                            anchors.fill: parent
                            hoverEnabled: true

                            // 不拦截子控件的事件
                            onClicked: mouse => mouse.accepted = false
                            onPressed: mouse => mouse.accepted = false
                        }
                    }
                    RowLayout {
                        id: rowLayout

                        anchors.left: parent.left
                        anchors.leftMargin: 12
                        anchors.right: parent.right
                        anchors.rightMargin: 12
                        anchors.verticalCenter: parent.verticalCenter
                        spacing: 4

                        // 姓名
                        Text {
                            Layout.preferredWidth: 100
                            color: Theme.currentTheme.colors.textColor
                            elide: Text.ElideRight
                            font.pixelSize: 14
                            text: modelData.name || ""
                        }

                        // 权重
                        Text {
                            Layout.preferredWidth: 60
                            color: Theme.currentTheme.colors.textColor
                            font.pixelSize: 14
                            horizontalAlignment: Text.AlignHCenter
                            text: modelData.weight !== undefined ? modelData.weight.toString() : "1"
                        }

                        // 启用
                        Item {
                            Layout.preferredWidth: 50
                            implicitHeight: enabledIcon.height

                            Icon {
                                id: enabledIcon

                                anchors.centerIn: parent
                                color: modelData.enabled ? Theme.currentTheme.colors.primaryColor : Theme.currentTheme.colors.textSecondaryColor
                                icon: modelData.enabled ? "ic_fluent_checkmark_circle_20_filled" : "ic_fluent_dismiss_circle_20_regular"
                                size: 18
                            }
                        }

                        // 头像
                        Item {
                            Layout.preferredWidth: 120
                            implicitHeight: Math.max(avatarImg.visible ? avatarImg.height : 0, avatarText.implicitHeight)

                            Image {
                                id: avatarImg

                                anchors.verticalCenter: parent.verticalCenter
                                fillMode: Image.PreserveAspectFit
                                height: 28
                                source: modelData.avatar ? localFileUrl(modelData.avatar) : ""
                                visible: modelData.avatar && status === Image.Ready
                                width: 28
                            }
                            Text {
                                id: avatarText

                                anchors.left: avatarImg.visible ? avatarImg.right : parent.left
                                anchors.leftMargin: avatarImg.visible ? 6 : 0
                                anchors.right: parent.right
                                anchors.verticalCenter: parent.verticalCenter
                                color: modelData.avatar ? Theme.currentTheme.colors.textColor : Theme.currentTheme.colors.textSecondaryColor
                                elide: Text.ElideMiddle
                                font.pixelSize: 12
                                text: modelData.avatar ? ellipsis(modelData.avatar, 12) : qsTr("未设置")
                                visible: !avatarImg.visible || modelData.avatar
                            }
                        }

                        // 附加属性
                        Text {
                            Layout.fillWidth: true
                            color: Theme.currentTheme.colors.textSecondaryColor
                            elide: Text.ElideRight
                            font.pixelSize: 12
                            text: {
                                var props = modelData.properties;
                                if (!props || props.length === 0)
                                    return qsTr("无");
                                var parts = [];
                                for (var i = 0; i < props.length; i++)
                                    parts.push(props[i].name + ": " + props[i].value);
                                return parts.join(", ");
                            }
                        }

                        // 操作按钮
                        RowLayout {
                            Layout.preferredWidth: 100
                            spacing: 2

                            ToolButton {
                                icon.name: "ic_fluent_edit_20_regular"

                                onClicked: {
                                    studentManagePage.editingGuid = modelData.id;
                                    if (editDialog.loadStudent(modelData.id))
                                        editDialog.open();
                                }

                                ToolTip {
                                    delay: 500
                                    text: qsTr("编辑")
                                    visible: parent.hovered
                                }
                            }
                            ToolButton {
                                icon.name: "ic_fluent_delete_20_regular"

                                onClicked: {
                                    deleteConfirmDialog.deletingGuid = modelData.id;
                                    deleteConfirmDialog.deletingName = modelData.name || "";
                                    deleteConfirmDialog.open();
                                }

                                ToolTip {
                                    delay: 500
                                    text: qsTr("删除")
                                    visible: parent.hovered
                                }
                            }
                        }
                    }
                }
            }

            // 空状态提示
            Text {
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 20
                color: Theme.currentTheme.colors.textSecondaryColor
                font.pixelSize: 14
                text: qsTr("暂无学生数据")
                visible: studentManagePage.studentsModel.length === 0
            }
        }
    }

    // ── 丢弃更改确认 Dialog ──
    Dialog {
        id: discardConfirmDialog

        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel
        title: qsTr("丢弃更改")
        width: 400

        onAccepted: {
            StudentsConfig.reload_config();
            studentManagePage.refreshStudents();
        }

        Text {
            Layout.fillWidth: true
            color: Theme.currentTheme.colors.textColor
            font.pixelSize: 14
            text: qsTr("您有未保存的更改。刷新将丢弃所有更改并从磁盘重新加载，确定继续吗？")
            wrapMode: Text.Wrap
        }
    }

    // ── 删除确认 Dialog ──
    Dialog {
        id: deleteConfirmDialog

        property string deletingGuid: ""
        property string deletingName: ""

        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel
        title: qsTr("确认删除")
        width: 400

        onAccepted: {
            StudentsConfig.remove_student(deletingGuid);
            studentManagePage.refreshStudents();
        }

        Text {
            Layout.fillWidth: true
            color: Theme.currentTheme.colors.textColor
            font.pixelSize: 14
            text: qsTr("确定要删除学生「%1」吗？此操作在保存前可通过重载恢复。").arg(deleteConfirmDialog.deletingName)
            wrapMode: Text.Wrap
        }
    }

    // ── 编辑学生 Dialog ──
    Dialog {
        id: editDialog

        // 编辑副本的附加属性
        property var editProperties: []

        function loadStudent(guid) {
            var stu = StudentsConfig.get_write_student(guid);
            if (!stu || !stu.id) {
                console.warn("loadStudent: 找不到 GUID", guid);
                studentManagePage.Window.window.floatLayer.createInfoBar({
                    title: qsTr("加载失败"),
                    text: qsTr("无法加载该学生的数据，请重试。"),
                    severity: Severity.Error,
                    timeout: 3000,
                    position: Position.Top
                });
                return false;
            }
            editNameField.text = stu.name || "";
            editWeightSlider.value = stu.weight !== undefined ? stu.weight : 1;
            editEnabledSwitch.checked = stu.enabled !== undefined ? stu.enabled : true;
            editAvatarField.text = stu.avatar || "";
            // 深拷贝附加属性
            var props = stu.properties || [];
            var copy = [];
            for (var i = 0; i < props.length; i++)
                copy.push({
                    name: props[i].name || "",
                    value: props[i].value || ""
                });
            editDialog.editProperties = copy;
            return true;
        }

        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel
        title: qsTr("编辑学生信息")
        width: 520

        onAccepted: {
            // 清理输入并写回缓冲区
            var trimmedName = editNameField.text.trim();
            var trimmedAvatar = editAvatarField.text.trim();
            StudentsConfig.update_student(studentManagePage.editingGuid, trimmedName, parseFloat(editWeightSlider.value.toFixed(1)), editEnabledSwitch.checked, trimmedAvatar);
            StudentsConfig.update_student_properties(studentManagePage.editingGuid, editDialog.editProperties);
            studentManagePage.refreshStudents();
        }

        Flickable {
            Layout.fillWidth: true
            Layout.preferredHeight: Math.min(dialogContent.implicitHeight, 480)
            boundsBehavior: Flickable.StopAtBounds
            clip: true
            contentHeight: dialogContent.implicitHeight
            contentWidth: width

            ScrollBar.vertical: ScrollBar {
            }

            ColumnLayout {
                id: dialogContent

                spacing: 4
                width: parent.width

                // GUID（只读）
                SettingCard {
                    Layout.fillWidth: true
                    description: studentManagePage.editingGuid
                    title: qsTr("GUID")
                }

                // 姓名
                SettingCard {
                    Layout.fillWidth: true
                    description: qsTr("学生显示名称")
                    title: qsTr("姓名")

                    TextField {
                        id: editNameField

                        implicitWidth: 180
                        placeholderText: qsTr("请输入姓名")
                    }
                }

                // 权重
                SettingCard {
                    Layout.fillWidth: true
                    description: qsTr("抽选权重，越高越容易被选中")
                    title: qsTr("权重")

                    ToolButton {
                        color: "#0078d4"
                        flat: true
                        icon.name: "ic_fluent_arrow_hook_up_left_20_regular"
                        visible: Math.abs(editWeightSlider.value - 1.0) > 0.01

                        onClicked: {
                            editWeightSlider.value = 1.0;
                        }

                        ToolTip {
                            delay: 500
                            text: qsTr("重置为默认值")
                            visible: parent.hovered
                        }
                    }
                    Text {
                        color: Theme.currentTheme.colors.textColor
                        font.pixelSize: 14
                        text: editWeightSlider.value.toFixed(1)
                        verticalAlignment: Text.AlignVCenter
                    }
                    Slider {
                        id: editWeightSlider

                        from: 0
                        stepSize: 0.1
                        to: 2
                        value: 1
                    }
                }

                // 启用
                SettingCard {
                    Layout.fillWidth: true
                    description: qsTr("是否参与抽选")
                    title: qsTr("启用")

                    Switch {
                        id: editEnabledSwitch

                        checked: true
                    }
                }

                // 头像（SettingExpander）
                SettingExpander {
                    Layout.fillWidth: true
                    description: qsTr("学生头像图片路径")
                    title: qsTr("头像")

                    action: RowLayout {
                        spacing: 8

                        Image {
                            Layout.preferredHeight: 28
                            Layout.preferredWidth: 28
                            fillMode: Image.PreserveAspectFit
                            source: editAvatarField.text ? localFileUrl(editAvatarField.text) : ""
                            visible: editAvatarField.text && status === Image.Ready
                        }
                        Text {
                            Layout.maximumWidth: 160
                            color: Theme.currentTheme.colors.textSecondaryColor
                            elide: Text.ElideMiddle
                            font.pixelSize: 12
                            text: editAvatarField.text || qsTr("未设置")
                            verticalAlignment: Text.AlignVCenter
                        }
                    }

                    SettingItem {
                        Layout.fillWidth: true
                        description: qsTr("输入路径或点击按钮选择文件")
                        title: qsTr("头像路径")

                        RowLayout {
                            spacing: 8

                            TextField {
                                id: editAvatarField

                                implicitWidth: 220
                                placeholderText: qsTr("图片路径")
                            }
                            Button {
                                text: qsTr("浏览…")

                                onClicked: avatarFileDialog.open()
                            }
                        }
                    }
                    SettingItem {
                        Layout.fillWidth: true
                        title: qsTr("预览")
                        visible: editAvatarField.text !== ""

                        Image {
                            Layout.maximumHeight: 96
                            Layout.maximumWidth: 96
                            fillMode: Image.PreserveAspectFit
                            source: editAvatarField.text ? localFileUrl(editAvatarField.text) : ""
                            visible: status === Image.Ready
                        }
                    }
                }

                // 附加属性
                SettingExpander {
                    id: propsExpander

                    Layout.fillWidth: true
                    description: qsTr("共 %1 项").arg(editDialog.editProperties.length)
                    title: qsTr("附加属性")

                    action: RowLayout {
                        Button {
                            text: qsTr("添加")

                            onClicked: {
                                var arr = editDialog.editProperties.slice();
                                arr.push({
                                    name: "",
                                    value: ""
                                });
                                editDialog.editProperties = arr;
                            }
                        }
                    }

                    // 属性列表
                    Repeater {
                        model: editDialog.editProperties

                        SettingItem {
                            required property int index
                            required property var modelData

                            Layout.fillWidth: true
                            title: qsTr("属性 %1").arg(index + 1)

                            RowLayout {
                                spacing: 8

                                TextField {
                                    implicitWidth: 100
                                    placeholderText: qsTr("属性名")
                                    text: modelData.name

                                    onEditingFinished: {
                                        if (index >= 0 && index < editDialog.editProperties.length && editDialog.editProperties[index].name !== text) {
                                            var arr = editDialog.editProperties.slice();
                                            arr[index] = {
                                                name: text,
                                                value: arr[index].value
                                            };
                                            editDialog.editProperties = arr;
                                        }
                                    }
                                }
                                TextField {
                                    implicitWidth: 120
                                    placeholderText: qsTr("属性值")
                                    text: modelData.value

                                    onEditingFinished: {
                                        if (index >= 0 && index < editDialog.editProperties.length && editDialog.editProperties[index].value !== text) {
                                            var arr = editDialog.editProperties.slice();
                                            arr[index] = {
                                                name: arr[index].name,
                                                value: text
                                            };
                                            editDialog.editProperties = arr;
                                        }
                                    }
                                }
                                ToolButton {
                                    icon.name: "ic_fluent_delete_20_regular"

                                    onClicked: {
                                        var arr = editDialog.editProperties.slice();
                                        arr.splice(index, 1);
                                        editDialog.editProperties = arr;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // ── 文件选择对话框 ──
    FileDialog {
        id: avatarFileDialog

        nameFilters: [qsTr("图片文件 (*.png *.jpg *.jpeg *.bmp *.svg)"), qsTr("所有文件 (*)")]
        title: qsTr("选择头像图片")

        onAccepted: {
            var path = selectedFile.toString();
            // 移除 file:// 前缀
            if (Qt.platform.os === "windows") {
                path = path.replace(/^file:\/\/\//, "");
            } else {
                path = path.replace(/^file:\/\//, "");
            }
            editAvatarField.text = decodeURIComponent(path);
        }
    }
}
