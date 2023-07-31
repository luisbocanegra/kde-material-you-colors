import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.0
import org.kde.kirigami 2.20 as Kirigami
import Qt.labs.settings 1.0
ColumnLayout {
    id:root
    signal configurationChanged
    anchors.fill: parent
    ColumnLayout {
        Layout.alignment: Qt.AlignTop
        Text {
            id:notice_text
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop
            text: 'This page is a work in progress, if you want to configure other options like, wallpaper plugin to use, transparency, enable Konsole Profile theming, configure a command to be executed when colors change and more check the <strong>Configuration file</strong> section on the project repo.'
            wrapMode: Text.WordWrap
            color: Kirigami.Theme.textColor
        }

        Button {
            text: "View Configuration file section on GitHub repo"
            Layout.alignment: Qt.AlignTop
            ToolTip.delay: 1000
            ToolTip.visible: hovered
            ToolTip.text: "https://github.com/luisbocanegra/kde-material-you-colors#configuration-file"
            onClicked: Qt.openUrlExternally(ToolTip.text)
        }
    }
}
