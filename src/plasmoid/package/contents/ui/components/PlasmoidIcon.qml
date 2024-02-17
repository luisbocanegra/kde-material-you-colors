import QtQuick
import org.kde.kirigami as Kirigami
import org.kde.ksvg as KSvg

Item {
    anchors.centerIn: parent
    property string customIcon: ""
    KSvg.SvgItem {
        id: svgItem
        opacity: 1
        width: parent.width
        height: width
        property int sourceIndex: 0
        anchors.centerIn: parent
        visible: customIcon == ""
        smooth: true
        svg: KSvg.Svg {
            id: svg
            colorSet: Kirigami.Theme.colorSet
            imagePath: Qt.resolvedUrl("../../icons/icon.svg")
        }
    }

    Kirigami.Icon {
        anchors.centerIn: parent
        width: parent.width
        height: width
        visible: customIcon != ""
        source: customIcon
        smooth: true
    }
}
