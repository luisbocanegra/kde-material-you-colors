import QtQuick 2.0
import org.kde.plasma.plasmoid 2.0
import org.kde.plasma.core 2.0 as PlasmaCore

import "."
Item {
    id:root
    // Always display the compact view.
    // Never show the full popup view even if there is space for it.
    Plasmoid.switchWidth: PlasmaCore.Units.gridUnit * 14
    Plasmoid.switchHeight: PlasmaCore.Units.gridUnit * 10

    Plasmoid.preferredRepresentation: Plasmoid.compactRepresentation

    Plasmoid.fullRepresentation: FullRepresentation {}
}
