import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.0
import org.kde.kirigami 2.20 as Kirigami
import org.kde.kquickcontrols 2.0 as KQControls
import Qt.labs.settings 1.0
ColumnLayout {
    KQControls.ColorButton {
        id: colorButton
        Layout.alignment: Qt.AlignRight
        showAlphaChannel: false
        height: 30
        // width: 10
        implicitWidth: 40 + 8*2
        implicitHeight: 40 + 8*2
    }
}
