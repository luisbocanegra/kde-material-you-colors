import QtQuick 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.15
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.plasma.extras 2.0 as PlasmaExtras
import org.kde.plasma.plasmoid 2.0
import org.kde.plasma.components 3.0 as PlasmaComponents3

Item {
    id:root

    // Allow full view on the desktop
    Plasmoid.preferredRepresentation: plasmoid.location ===
                                    PlasmaCore.Types.Floating ?
                                    Plasmoid.fullRepresentation :
                                    Plasmoid.compactRepresentation

    property bool doSettingsReload: false

    Plasmoid.fullRepresentation: FullRepresentation {
        doSettingsReload: root.doSettingsReload
    }

    function reloadConfig() {
        console.log("RELOAD");
        doSettingsReload = true
        doSettingsReload = false
    }

    function action_reloadConfig() {
        reloadConfig()
    }


    Component.onCompleted: function() {
        Plasmoid.setAction('reloadConfig', i18n("Reload configuration file"), 'view-refresh');
        Plasmoid.removeAction("configure"); // May find an use for it in the future idk
    }
}
