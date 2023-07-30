// This is a modified version of https://invent.kde.org/frameworks/kdeclarative/-/blob/master/src/qmlcontrols/kquickcontrols/ColorButton.qml to make it look more like a button

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.3

Button {
    id: colorButton
    /**
     * The user selected color
     */
    property alias color: colorDialog.color

    /**
     * Title to show in the dialog
     */
    property alias dialogTitle: colorDialog.title

    /**
     * Allow the user to configure an alpha value
     */
    property alias showAlphaChannel: colorDialog.showAlphaChannel

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
        onAccepted: colorButton.accepted(color)
        showAlphaChannel: colorButton.showAlphaChannel ? true : undefined
    }

    onClicked: {
        // colorDialog.color = colorButton.color
        colorDialog.open()
    }
}
