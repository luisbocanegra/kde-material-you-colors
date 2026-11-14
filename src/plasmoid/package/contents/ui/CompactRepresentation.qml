import QtQuick
import org.kde.kirigami as Kirigami
import org.kde.plasma.core as PlasmaCore
import org.kde.plasma.plasmoid

MouseArea {
    id: compact
    anchors.fill: parent
    property bool isPanelVertical: Plasmoid.formFactor === PlasmaCore.Types.Vertical
    property real itemSize: Math.min(compact.height, compact.width)
    property string icon
    property bool onDesktop
    property bool wasExpanded
    property bool canExpand

    Kirigami.Icon {
        anchors.centerIn: parent
        width: Kirigami.Units.iconSizes.roundedIconSize(Math.min(parent.width, parent.height))
        height: width
        source: compact.icon
    }

    onPressed: {
        compact.wasExpanded = main.expanded;
    }
    onClicked: {
        main.expanded = !compact.wasExpanded;
    }
}
