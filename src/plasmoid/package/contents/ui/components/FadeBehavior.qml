// https://doc.qt.io/qt-5/qml-qtquick-behavior.html#targetProperty-prop
import QtQuick 2.15

Behavior {
    id: root
    property Item fadeTarget: targetProperty.object
    property int duration
    SequentialAnimation {
        NumberAnimation {
            target: root.fadeTarget
            property: "opacity"
            to: 0
            duration: root.duration
            easing.type: Easing.InQuad
        }
        PropertyAction { } // actually change the controlled property between the 2 other animations
        NumberAnimation {
            target: root.fadeTarget
            property: "opacity"
            to: 1
            duration: root.duration
            easing.type: Easing.OutQuad
        }
    }
}
