import QtQuick 2.0
import org.kde.plasma.core 2.0 as PlasmaCore
import QtQuick.Layouts 1.1
import org.kde.plasma.plasmoid 2.0
import "components" as Components

Item {
    id: root

    property bool isVertical: plasmoid.formFactor === PlasmaCore.Types.Vertical

    Layout.minimumWidth: PlasmaCore.Units.iconSizes.small
    Layout.minimumHeight: PlasmaCore.Units.iconSizes.small

    Layout.preferredWidth: root.height
    Layout.preferredHeight: root.width


    Components.PlasmoidIcon {
        width: isVertical ? root.height : root.width
        customIcon: plasmoid.configuration.icon
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onClicked: plasmoid.expanded = !plasmoid.expanded
    }

    // Rectangle {
    //     anchors.fill: parent
    //     color: "red"
    //     opacity: 0.1
    // }
}
