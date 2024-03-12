import QtQuick
import org.kde.kirigami as Kirigami
import org.kde.ksvg as KSvg
import org.kde.plasma.core as PlasmaCore

Item {
    anchors.centerIn: parent
    property string customIcon: ""
    anchors.fill: parent

    Kirigami.Icon {
        anchors.centerIn: parent
        width: Math.min(parent.height, parent.width)
        height: width
        source: customIcon || Qt.resolvedUrl("../../icons/icon.svg")
        active: compact.containsMouse
        isMask: true
        color: Kirigami.Theme.textColor
        opacity: 1
    }
}
