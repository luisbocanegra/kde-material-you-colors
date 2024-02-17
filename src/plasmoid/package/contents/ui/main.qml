import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.plasma.core as PlasmaCore
import org.kde.plasma.plasmoid

PlasmoidItem {
    id: main

    signal togglePauseMode()
    signal updatePauseMode()

    property bool doSettingsReload: false
    property bool pauseModeMain: true
    property bool lastPauseState: true
    property bool inTray: (plasmoid.containmentDisplayHints & PlasmaCore.Types.ContainmentDrawsPlasmoidHeading)
    property bool trayExpanded: (expanded && inTray )
    property string pauseBtnIcon: pauseModeMain ? 'media-playback-start' : 'media-playback-pause'
    property string pauseBtnText: pauseModeMain ? 'Resume automatic theming' : 'Pause automatic theming'

    compactRepresentation: CompactRepresentation {
        anchors.fill: parent
    }

    fullRepresentation: FullRepresentation {
        id: fullRepresentationComponent
        parentMain: main
    }

    // MouseArea {
    //     id: mouseArea
    //     anchors.fill: parent
    //     hoverEnabled: true
    //     onClicked: {
    //         main.expanded = !main.expanded
    //     }
    // }

    function action_pauseBackend() {
        console.log("action_pauseBackend called")
        togglePauseMode()
    }

    // Component.onCompleted: function() {
    //     Plasmoid.setAction('pauseBackend', pauseBtnText , pauseBtnIcon)
    // }

    Plasmoid.contextualActions: [
        PlasmaCore.Action {
            id: pauseAction
            text: pauseBtnText
            checkable: false
            icon.name: pauseBtnIcon
            // cheched:
            onTriggered: {
                togglePauseMode()
            }
        }
    ]

    Timer {
        interval: trayExpanded ? 100 : 1000
        running: true
        repeat: true
        id: startMe
        onTriggered: function() {
            if (pauseModeMain !== lastPauseState) {
                // Plasmoid.removeAction('pauseBackend')
                // Plasmoid.setAction('pauseBackend', pauseBtnText , pauseBtnIcon)
                pauseAction.text = pauseBtnText
                pauseAction.icon.name = pauseBtnIcon
            }
            lastPauseState = pauseModeMain
        }
    }
}
