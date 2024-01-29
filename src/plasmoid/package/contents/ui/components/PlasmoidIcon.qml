import QtQuick 2.15
import org.kde.plasma.core 2.0 as PlasmaCore
import QtQuick.Layouts 1.1

Item {
    anchors.centerIn: parent
    property string customIcon: ""
    PlasmaCore.SvgItem {
        id: svgItem
        opacity: 1
        width: parent.width
        height: width
        property int sourceIndex: 0
        anchors.centerIn: parent
        visible: customIcon == ""
        smooth: true
        svg: PlasmaCore.Svg {
            id: svg
            colorGroup: PlasmaCore.ColorScope.colorGroup
            imagePath: Qt.resolvedUrl("../../icons/icon.svg")
        }
    }

    PlasmaCore.IconItem {
        anchors.centerIn: parent
        width: parent.width
        height: width
        visible: customIcon != ""
        source: customIcon
        smooth: true
    }
}
