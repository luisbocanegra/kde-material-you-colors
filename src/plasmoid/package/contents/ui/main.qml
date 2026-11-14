pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.plasma.core as PlasmaCore
import org.kde.plasma.plasmoid

PlasmoidItem {
    id: main

    signal togglePauseMode
    signal updatePauseMode

    property bool doSettingsReload: false
    property bool pauseModeMain: true
    property bool lastPauseState: true
    property bool inTray: (plasmoid.containmentDisplayHints & PlasmaCore.Types.ContainmentDrawsPlasmoidHeading)
    property bool trayExpanded: (expanded && inTray)
    property string pauseBtnIcon: pauseModeMain ? 'media-playback-start' : 'media-playback-pause'
    property string pauseBtnText: pauseModeMain ? 'Resume automatic theming' : 'Pause automatic theming'
    readonly property bool hideWidget: Plasmoid.configuration.hideWidget
    property bool onDesktop: Plasmoid.location === PlasmaCore.Types.Floating
    property bool inEditMode: Plasmoid.containment?.corona?.editMode ?? false

    function updateWidgetStatus() {
        Plasmoid.status = main.hideWidget ? PlasmaCore.Types.HiddenStatus : PlasmaCore.Types.ActiveStatus;
    }
    onHideWidgetChanged: {
        updateWidgetStatus();
    }
    Component.onCompleted: updateWidgetStatus()
    compactRepresentation: CompactRepresentation {
        icon: Plasmoid.configuration.icon || Qt.resolvedUrl("../icons/icon.svg")
        anchors.fill: parent
    }

    fullRepresentation: FullRepresentation {
        id: fullRepresentationComponent
        parentMain: main
        visible: !main.hideWidget || !main.onDesktop
    }

    Plasmoid.backgroundHints: {
        if (main.inEditMode || !hideWidget || !main.onDesktop) {
            return PlasmaCore.Types.DefaultBackground;
        } else {
            return PlasmaCore.Types.NoBackground;
        }
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
        console.log("action_pauseBackend called");
        togglePauseMode();
    }

    // Component.onCompleted: function() {
    //     Plasmoid.setAction('pauseBackend', pauseBtnText , pauseBtnIcon)
    // }

    PlasmaCore.Action {
        id: hideWidgetAction
        text: (Plasmoid.configuration.hideWidget ? i18n("Show") : i18n("Hide")) + " widget"
        icon.name: "visibility-symbolic"
        onTriggered: {
            Plasmoid.configuration.hideWidget = !Plasmoid.configuration.hideWidget;
            Plasmoid.configuration.writeConfig();
        }
        visible: !main.inTray
    }

    PlasmaCore.Action {
        id: pauseAction
        text: pauseBtnText
        checkable: false
        icon.name: pauseBtnIcon
        // cheched:
        onTriggered: {
            togglePauseMode();
        }
    }

    Plasmoid.contextualActions: [hideWidgetAction, pauseAction]

    Timer {
        id: startMe
        interval: trayExpanded ? 100 : 1000
        running: true
        repeat: true
        onTriggered: function () {
            if (pauseModeMain !== lastPauseState) {
                // Plasmoid.removeAction('pauseBackend')
                // Plasmoid.setAction('pauseBackend', pauseBtnText , pauseBtnIcon)
                pauseAction.text = pauseBtnText;
                pauseAction.icon.name = pauseBtnIcon;
            }
            lastPauseState = pauseModeMain;
        }
    }
}
