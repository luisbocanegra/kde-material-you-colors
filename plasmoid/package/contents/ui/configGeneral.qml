import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.0
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kquickcontrolsaddons 2.0 as KQuickAddons
import org.kde.kirigami 2.20 as Kirigami
import Qt.labs.settings 1.0
import "components" as Components
ColumnLayout {
    id:root
    signal configurationChanged
    anchors.fill: parent
    property string cfg_icon: plasmoid.configuration.icon
    property string defaultIconName: ""
    ColumnLayout {
        Layout.alignment: Qt.AlignTop

        RowLayout {
            Label {
                text: "Icon:"
            }

            Button {
                id: iconButton

                implicitWidth: previewFrame.width + PlasmaCore.Units.smallSpacing * 2
                implicitHeight: previewFrame.height + PlasmaCore.Units.smallSpacing * 2
                hoverEnabled: true

                Accessible.name: i18nc("@action:button", "Change Application Launcher's icon")
                Accessible.description: i18nc("@info:whatsthis", "Current icon is %1. Click to open menu to change the current icon or reset to the default icon.", cfg_icon)
                Accessible.role: Accessible.ButtonMenu

                ToolTip.delay: Kirigami.Units.toolTipDelay
                ToolTip.text: i18nc("@info:tooltip", "Icon name is \"%1\"", cfg_icon)
                ToolTip.visible: iconButton.hovered && cfg_icon.length > 0

                KQuickAddons.IconDialog {
                    id: iconDialog
                    onIconNameChanged: cfg_icon = iconName || defaultIconName
                }

                onPressed: iconMenu.opened ? iconMenu.close() : iconMenu.open()

                PlasmaCore.FrameSvgItem {
                    id: previewFrame
                    anchors.centerIn: parent
                    imagePath: plasmoid.formFactor === PlasmaCore.Types.Vertical || plasmoid.formFactor === PlasmaCore.Types.Horizontal
                            ? "widgets/panel-background" : "widgets/background"
                    width: PlasmaCore.Units.iconSizes.large + fixedMargins.left + fixedMargins.right
                    height: PlasmaCore.Units.iconSizes.large + fixedMargins.top + fixedMargins.bottom

                    Components.PlasmoidIcon {
                        width: PlasmaCore.Units.iconSizes.large
                        customIcon: root.cfg_icon
                    }
                }

                Menu {
                    id: iconMenu

                    // Appear below the button
                    y: +parent.height

                    MenuItem {
                        text: i18nc("@item:inmenu Open icon chooser dialog", "Choose…")
                        icon.name: "document-open-folder"
                        Accessible.description: i18nc("@info:whatsthis", "Choose an icon for Application Launcher")
                        onClicked: iconDialog.open()
                    }
                    MenuItem {
                        text: i18nc("@item:inmenu Reset icon to default", "Reset to default icon")
                        icon.name: "edit-clear"
                        enabled: cfg_icon !== defaultIconName
                        onClicked: cfg_icon = defaultIconName
                    }
                }
            }
        }
    }
}
