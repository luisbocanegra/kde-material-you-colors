import QtQuick
import org.kde.kirigami as Kirigami
import org.kde.plasma.core as PlasmaCore
import QtQuick.Layouts
import org.kde.plasma.plasmoid
import "components" as Components

MouseArea {
    id: compact
    hoverEnabled: true
    onPressed: wasExpanded = main.expanded
    onClicked: main.expanded = !wasExpanded

    property bool isVertical: plasmoid.formFactor === PlasmaCore.Types.Vertical
    anchors.fill: parent

    Layout.minimumWidth: Kirigami.Units.iconSizes.small
    Layout.minimumHeight: Kirigami.Units.iconSizes.small

    Layout.preferredWidth: compact.height
    Layout.preferredHeight: compact.width
    property bool wasExpanded

    Components.PlasmoidIcon {
        width: isVertical ? compact.height : compact.width
        customIcon: plasmoid.configuration.icon
    }
}
