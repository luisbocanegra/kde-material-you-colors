import QtQuick 2.0
import org.kde.kirigami as Kirigami
import org.kde.plasma.core 2.0 as PlasmaCore
import QtQuick.Layouts 1.1
import org.kde.plasma.plasmoid 2.0
import "components" as Components

Item {
    id: compact

    property bool isVertical: plasmoid.formFactor === PlasmaCore.Types.Vertical

    Layout.minimumWidth: Kirigami.Units.iconSizes.small
    Layout.minimumHeight: Kirigami.Units.iconSizes.small

    Layout.preferredWidth: compact.height
    Layout.preferredHeight: compact.width
    property bool wasExpanded


    Components.PlasmoidIcon {
        width: isVertical ? compact.height : compact.width
        customIcon: plasmoid.configuration.icon
    }

    MouseArea {
        anchors.fill: parent
        onPressed: wasExpanded = main.expanded
        onClicked: main.expanded = !wasExpanded
    }
}
