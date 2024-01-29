import QtQuick 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.15
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.plasma.extras 2.0 as PlasmaExtras
import org.kde.plasma.plasmoid 2.0
import org.kde.plasma.components 3.0 as PlasmaComponents3

Item {
    id:main

    // Allow full view on the desktop
    Plasmoid.preferredRepresentation: plasmoid.location ===
                                    PlasmaCore.Types.Floating ?
                                    Plasmoid.fullRepresentation :
                                    Plasmoid.compactRepresentation

    Plasmoid.compactRepresentation: CompactRepresentation {
        anchors.fill: parent
    }

    signal togglePauseMode()
    signal updatePauseMode()

    property bool doSettingsReload: false
    property bool pauseModeMain: true
    property bool lastPauseState: true
    property bool expanded: plasmoid.expanded
    property bool inTray: (plasmoid.containmentDisplayHints & PlasmaCore.Types.ContainmentDrawsPlasmoidHeading)
    property bool trayExpanded: (expanded && inTray)
    property string pauseBtnIcon: pauseModeMain ? 'media-playback-start' : 'media-playback-pause'
    property string pauseBtnText: pauseModeMain ? 'Resume automatic theming' : 'Pause automatic theming'

    Plasmoid.fullRepresentation: FullRepresentation {
        id: fullRepresentationComponent
        parentMain: main
    }

    function action_pauseBackend() {
        console.log("action_pauseBackend called")
        togglePauseMode()
    }

    Component.onCompleted: function() {
        Plasmoid.setAction('pauseBackend', pauseBtnText , pauseBtnIcon)
    }

    Timer {
        interval: trayExpanded ? 100 : 1000
        running: true
        repeat: true
        id: startMe
        onTriggered: function() {
            if (pauseModeMain !== lastPauseState) {
                Plasmoid.removeAction('pauseBackend')
                Plasmoid.setAction('pauseBackend', pauseBtnText , pauseBtnIcon)
            }
            lastPauseState = pauseModeMain
        }
    }
}
