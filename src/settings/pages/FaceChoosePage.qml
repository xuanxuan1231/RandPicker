import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI

FluentPage {
    id: faceChoosePage

    property bool cameraActive: false
    property var cameraIds: []
    property var cameraNames: []
    property var detectedFaces: []
    property int frameCounter: 0

    function refreshCameras() {
        var cams = FaceChooser.getAvailableCameras();
        var names = [];
        var ids = [];
        for (var i = 0; i < cams.length; i++) {
            names.push(cams[i].name);
            ids.push(cams[i].id);
        }
        cameraNames = names;
        cameraIds = ids;
        if (names.length > 0) {
            cameraSelector.currentIndex = 0;
        }
    }

    title: qsTr("人脸抽选")

    Component.onCompleted: {
        refreshCameras();
    }
    Component.onDestruction: {
        if (cameraActive) {
            FaceChooser.stopCamera();
        }
    }

    // 帧定时器：定时刷新摄像头画面
    Timer {
        id: frameTimer

        interval: 50
        repeat: true
        running: cameraActive

        onTriggered: {
            faceChoosePage.frameCounter++;
        }
    }

    // 摄像头状态信号处理
    Connections {
        function onCameraStatusChanged(status) {
            if (status === "running") {
                cameraActive = true;
            } else {
                cameraActive = false;
            }
        }

        target: FaceChooser
    }
    ColumnLayout {
        Layout.fillHeight: true
        Layout.fillWidth: true
        spacing: 16

        // ── 摄像头预览区域 ──
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 380
            color: "#1a1a1a"
            radius: 8

            Image {
                id: cameraPreview

                anchors.centerIn: parent
                cache: false
                fillMode: Image.PreserveAspectFit
                height: parent.height
                source: cameraActive ? "image://camera/frame?" + faceChoosePage.frameCounter : ""
                visible: cameraActive
                width: parent.width
            }
            ColumnLayout {
                anchors.centerIn: parent
                spacing: 8
                visible: !cameraActive

                Text {
                    Layout.alignment: Qt.AlignHCenter
                    font.pixelSize: 48
                    text: "📷"
                }
                Text {
                    Layout.alignment: Qt.AlignHCenter
                    color: "#aaaaaa"
                    font.pixelSize: 16
                    text: qsTr("摄像头未启动")
                }
            }
        }

        // ── 控制区域 ──
        RowLayout {
            Layout.fillWidth: true
            spacing: 12

            // 摄像头选择
            ColumnLayout {
                spacing: 4

                Text {
                    color: "#888"
                    font.pixelSize: 12
                    text: qsTr("选择摄像头")
                }
                ComboBox {
                    id: cameraSelector

                    Layout.preferredWidth: 180
                    enabled: !cameraActive
                    model: cameraNames

                    onCurrentIndexChanged: {
                        if (currentIndex >= 0 && currentIndex < cameraIds.length) {
                            FaceChooser.switchCamera(cameraIds[currentIndex].toString());
                        }
                    }
                }
            }

            // 抽选人数
            ColumnLayout {
                spacing: 4

                Text {
                    color: "#888"
                    font.pixelSize: 12
                    text: qsTr("抽选人数")
                }
                RowLayout {
                    spacing: 4

                    ToolButton {
                        icon.name: "ic_fluent_subtract_20_regular"

                        onClicked: {
                            var val = parseInt(faceCountInput.text);
                            if (val > 1)
                                faceCountInput.text = (val - 1).toString();
                        }
                    }
                    TextField {
                        id: faceCountInput

                        Layout.preferredWidth: 50
                        horizontalAlignment: Text.AlignHCenter
                        text: "1"

                        validator: IntValidator {
                            bottom: 1
                            top: 99
                        }
                    }
                    ToolButton {
                        icon.name: "ic_fluent_add_20_regular"

                        onClicked: {
                            var val = parseInt(faceCountInput.text);
                            if (val < 99)
                                faceCountInput.text = (val + 1).toString();
                        }
                    }
                }
            }
            Item {
                Layout.fillWidth: true
            }

            // 刷新摄像头列表
            Button {
                enabled: !cameraActive
                icon.name: "ic_fluent_arrow_sync_20_regular"
                text: qsTr("刷新")

                onClicked: refreshCameras()
            }
        }

        // ── 操作按钮 ──
        RowLayout {
            Layout.fillWidth: true
            spacing: 12

            Button {
                id: toggleCameraBtn

                Layout.fillWidth: true
                enabled: cameraActive || cameraIds.length > 0
                highlighted: !cameraActive
                icon.name: cameraActive ? "ic_fluent_video_off_20_regular" : "ic_fluent_video_20_regular"
                implicitHeight: 44
                text: cameraActive ? qsTr("关闭摄像头") : qsTr("开启摄像头")

                onClicked: {
                    if (cameraActive) {
                        FaceChooser.stopCamera();
                    } else {
                        FaceChooser.startCamera();
                    }
                }
            }
            Button {
                id: captureBtn

                Layout.fillWidth: true
                enabled: cameraActive
                highlighted: true
                icon.name: "ic_fluent_camera_20_regular"
                implicitHeight: 44
                text: qsTr("拍照并抽选")

                onClicked: {
                    var count = parseInt(faceCountInput.text) || 1;
                    var results = FaceChooser.captureAndDetect(count);
                    if (results && results.length > 0) {
                        faceChoosePage.detectedFaces = results;
                        faceResultDialog.open();
                    } else {
                        noFaceDialog.open();
                    }
                }
            }
        }
    }

    // ── 人脸结果 Dialog ──
    Dialog {
        id: faceResultDialog

        anchors.centerIn: parent
        modal: true
        standardButtons: Dialog.Ok
        title: qsTr("抽选结果 - 选中 %1 张人脸").arg(faceChoosePage.detectedFaces.length)
        width: Math.min(faceChoosePage.width * 0.85, 700)

        contentItem: ColumnLayout {
            spacing: 16

            GridLayout {
                Layout.fillWidth: true
                columnSpacing: 12
                columns: Math.max(1, Math.min(3, faceChoosePage.detectedFaces.length))
                rowSpacing: 12

                Repeater {
                    model: faceChoosePage.detectedFaces

                    delegate: Rectangle {
                        Layout.fillWidth: true
                        border.color: "#3399ff"
                        border.width: 2
                        color: "transparent"
                        implicitHeight: delegateColumn.implicitHeight + 16
                        radius: 8

                        ColumnLayout {
                            id: delegateColumn

                            anchors.left: parent.left
                            anchors.margins: 8
                            anchors.right: parent.right
                            anchors.top: parent.top
                            spacing: 8

                            Image {
                                id: faceImage

                                Layout.fillWidth: true
                                Layout.preferredHeight: 160
                                cache: false
                                fillMode: Image.PreserveAspectFit
                                source: modelData.path
                            }
                            Text {
                                id: faceLabel

                                Layout.alignment: Qt.AlignHCenter
                                color: "#3399ff"
                                font.bold: true
                                font.pixelSize: 14
                                text: qsTr("人脸 %1").arg(modelData.index + 1)
                            }
                        }
                    }
                }
            }
        }

        onClosed: {
            // 可选：关闭后清理
        }
    }

    // ── 未检测到人脸 Dialog ──
    Dialog {
        id: noFaceDialog

        anchors.centerIn: parent
        modal: true
        standardButtons: Dialog.Ok
        title: qsTr("提示")
        width: 350

        contentItem: ColumnLayout {
            spacing: 12

            Text {
                Layout.fillWidth: true
                font.pixelSize: 14
                text: qsTr("未检测到人脸。请确保画面中有可识别的人脸，然后重试。")
                wrapMode: Text.Wrap
            }
        }
    }
}
