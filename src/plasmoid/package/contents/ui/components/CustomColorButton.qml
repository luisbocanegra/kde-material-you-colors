// This is a modified version of https://invent.kde.org/frameworks/kdeclarative/-/blob/master/src/qmlcontrols/kquickcontrols/ColorButton.qml to make it look more like a button

import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import org.kde.plasma.components as PlasmaComponents3

PlasmaComponents3.Button {
    id: colorButton
    /**
     * The user selected color
     */
    property alias color: colorDialog.selectedColor

    /**
     * Title to show in the dialog
     */
    property alias dialogTitle: colorDialog.title

    /**
     * Allow the user to configure an alpha value
     */
    property bool showAlphaChannel: false

    /**
     * This signal is emitted when the color dialog has been accepted
     *
     * @since 5.61
     */
    signal accepted(color color)

    contentItem: Rectangle {
        anchors.fill: parent
        anchors.margins: 10
        color: colorButton.color
    }

    ColorDialog {
        id: colorDialog
        selectedColor: undefined
        onAccepted: colorButton.accepted(color)
        // showAlphaChannel: colorButton.showAlphaChannel ? true : undefined
    }

        Component {
        id: colorWindowComponent

        Window { // QTBUG-119055 https://invent.kde.org/plasma/kdeplasma-addons/-/commit/797cef06882acdf4257d8c90b8768a74fdef0955
            id: window
            width: Kirigami.Units.gridUnit * 19
            height: Kirigami.Units.gridUnit * 23
            visible: true
            title: Plasmoid.title
            ColorDialog {
                id: colorDialog
                title: Plasmoid.title
                selectedColor: colorButton.color || undefined /* Prevent transparent colors */
                onAccepted: {
                    root.colorPicked(selectedColor);
                    window.destroy();
                }
                onRejected: window.destroy()
            }
            onClosing: destroy()
            Component.onCompleted: colorDialog.open()
        }
    }

    onClicked: {
        // colorDialog.color = colorButton.color
        colorWindowComponent.createObject(colorButton)
    }
}
