import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI

FluentPage {
    id: faceChoosePage

    property var detectedFaces: []
    property bool cameraActive: false
    property int frameCounter: 0
    property var cameraNames: []
    property var cameraIds: []

    title: qsTr("人脸抽选")

    Component.onCompleted: {
        refreshCameras();
    }
    Component.onDestruction: {
        if (cameraActive) {
            FaceChooser.stopCamera();
        }
    }

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

    // 帧定时器：定时刷新摄像头画面
    Timer {
        id: frameTimer
        interval: 50
        repeat: true
        running: cameraActive

        onTriggered: {
            faceChoosePage.frameCounter++;
            cameraPreview.source = "";
            cameraPreview.source = "image://camera/frame?" + faceChoosePage.frameCounter;
        }
    }

    // 摄像头状态信号处理
    Connections {
        target: FaceChooser
        function onCameraStatusChanged(status) {
            if (status === "running") {
                cameraActive = true;
            } else {
                cameraActive = false;
            }
        }
    }

    ColumnLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true
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
                width: parent.width
                height: parent.height
                fillMode: Image.PreserveAspectFit
                cache: false
                source: cameraActive ? "image://camera/frame?0" : ""
                visible: cameraActive
            }

            ColumnLayout {
                anchors.centerIn: parent
                visible: !cameraActive
                spacing: 8

                Text {
                    Layout.alignment: Qt.AlignHCenter
                    text: "📷"
                    font.pixelSize: 48
                }
                Text {
                    Layout.alignment: Qt.AlignHCenter
                    text: qsTr("摄像头未启动")
                    font.pixelSize: 16
                    color: "#aaaaaa"
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
                    text: qsTr("选择摄像头")
                    font.pixelSize: 12
                    color: "#888"
                }
                ComboBox {
                    id: cameraSelector
                    Layout.preferredWidth: 180
                    model: cameraNames
                    enabled: !cameraActive

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
                    text: qsTr("抽选人数")
                    font.pixelSize: 12
                    color: "#888"
                }
                RowLayout {
                    spacing: 4

                    ToolButton {
                        icon.name: "ic_fluent_subtract_20_regular"
                        onClicked: {
                            var val = parseInt(faceCountInput.text);
                            if (val > 1) faceCountInput.text = (val - 1).toString();
                        }
                    }
                    TextField {
                        id: faceCountInput
                        Layout.preferredWidth: 50
                        horizontalAlignment: Text.AlignHCenter
                        text: "1"
                        validator: IntValidator { bottom: 1; top: 99 }
                    }
                    ToolButton {
                        icon.name: "ic_fluent_add_20_regular"
                        onClicked: {
                            var val = parseInt(faceCountInput.text);
                            if (val < 99) faceCountInput.text = (val + 1).toString();
                        }
                    }
                }
            }

            Item { Layout.fillWidth: true }

            // 刷新摄像头列表
            Button {
                text: qsTr("刷新")
                icon.name: "ic_fluent_arrow_sync_20_regular"
                enabled: !cameraActive
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
                implicitHeight: 44
                highlighted: !cameraActive
                enabled: cameraActive || cameraIds.length > 0
                text: cameraActive ? qsTr("关闭摄像头") : qsTr("开启摄像头")
                icon.name: cameraActive ? "ic_fluent_video_off_20_regular" : "ic_fluent_video_20_regular"

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
                implicitHeight: 44
                highlighted: true
                enabled: cameraActive
                text: qsTr("拍照并抽选")
                icon.name: "ic_fluent_camera_20_regular"

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
        width: Math.min(faceChoosePage.width * 0.85, 700)
        modal: true
        title: qsTr("抽选结果 - 选中 %1 张人脸").arg(faceChoosePage.detectedFaces.length)
        standardButtons: Dialog.Ok

        contentItem: ColumnLayout {
            spacing: 16

            GridLayout {
                Layout.fillWidth: true
                columns: Math.max(1, Math.min(3, faceChoosePage.detectedFaces.length))
                columnSpacing: 12
                rowSpacing: 12

                Repeater {
                    model: faceChoosePage.detectedFaces

                    delegate: Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: faceImage.paintedHeight + faceLabel.implicitHeight + 24
                        color: "transparent"
                        radius: 8
                        border.color: "#3399ff"
                        border.width: 2

                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 8
                            spacing: 8

                            Image {
                                id: faceImage
                                Layout.fillWidth: true
                                Layout.preferredHeight: 160
                                fillMode: Image.PreserveAspectFit
                                source: modelData.path
                                cache: false
                            }
                            Text {
                                id: faceLabel
                                Layout.alignment: Qt.AlignHCenter
                                text: qsTr("人脸 %1").arg(modelData.index + 1)
                                font.pixelSize: 14
                                font.bold: true
                                color: "#3399ff"
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
        width: 350
        modal: true
        title: qsTr("提示")
        standardButtons: Dialog.Ok

        contentItem: ColumnLayout {
            spacing: 12

            Text {
                Layout.fillWidth: true
                text: qsTr("未检测到人脸。请确保画面中有可识别的人脸，然后重试。")
                font.pixelSize: 14
                wrapMode: Text.Wrap
            }
        }
    }
}
