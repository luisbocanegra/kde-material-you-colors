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
        spacing: 2
        anchors.fill: parent

        Text {
            text: root.customName !== "" ? `${root.customName}` : `${root.role}`
            color: root.scheme[root.onRole]
            font.bold: true
            font.pixelSize: Kirigami.Theme.defaultFont.pixelSize
            elide: Text.ElideRight
            Layout.fillWidth: true
        }

        Text {
            text: `${root.onRole}`
            color: root.scheme[root.onRole]
            font.pixelSize: Kirigami.Theme.smallFont.pixelSize
            visible: root.customName === ""
            elide: Text.ElideRight
            Layout.fillWidth: true
        }
    }
}


