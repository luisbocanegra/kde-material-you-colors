import QtQuick
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Rectangle {
    id: root
    property string role
    property string onRole
    property string customName
    property var scheme
    Layout.fillWidth: true
    implicitHeight: col.implicitHeight + Kirigami.Units.mediumSpacing
    color: scheme[root.role]
    ColumnLayout {
        id: col
        spacing: 0
        anchors.fill: parent

        RowLayout {
            Layout.leftMargin: Kirigami.Units.smallSpacing
            Layout.rightMargin: Kirigami.Units.smallSpacing
            Text {
                text: root.customName !== "" ? `${root.customName}` : `${root.role}`
                color: root.scheme[root.onRole]
                font.bold: true
                font.pixelSize: Kirigami.Theme.defaultFont.pixelSize
                elide: Text.ElideRight
                Layout.fillWidth: true
            }
            Text {
                text: `${root.scheme[root.role]}`
                color: root.scheme[root.onRole]
                font.pixelSize: Kirigami.Theme.smallFont.pixelSize
                Layout.alignment: Qt.AlignRight
                opacity: 0.7
                font.family: "monospace"
            }
        }

        RowLayout {
            Layout.leftMargin: Kirigami.Units.smallSpacing
            Layout.rightMargin: Kirigami.Units.smallSpacing
            Text {
                text: `${root.onRole}`
                color: root.scheme[root.onRole]
                font.pixelSize: Kirigami.Theme.smallFont.pixelSize
                opacity: root.customName === ""
                Layout.fillWidth: true
                elide: Text.ElideRight
            }
            Text {
                text: `${root.scheme[root.onRole]}`
                color: root.scheme[root.onRole]
                font.pixelSize: Kirigami.Theme.smallFont.pixelSize
                Layout.alignment: Qt.AlignRight
                opacity: 0.7
                font.family: "monospace"
            }
        }
    }
}
