import QtQuick 2.9
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.15
import org.kde.plasma.core 2.0 as PlasmaCore
ColumnLayout {
    id:root
    anchors.fill: parent

    Layout.preferredWidth: 560 * PlasmaCore.Units.devicePixelRatio
    Layout.preferredHeight: loader.height + button.height + root.spacing
    spacing: 2

    // TODO: put in heading
    Button {
        id:button
        text: "Reload configuration"
        icon.name: "view-refresh"
        onClicked: {
            loader.source = ""
            loader.source = "FullRepMain.qml"
        }
    }

    Loader {
        id: loader
        Layout.fillWidth: true
        Layout.fillHeight: true
        source: "FullRepMain.qml"

        // TODO: reload when config changes
        // onLoaded: {
        //     item.reloadUI.connect(function() {
        //         loader.source = ""
        //             loader.source = "FullRepMain.qml"
        //             console.log("RELOAD REQUEST SERVED");
        //     })
        // }
    }
}
