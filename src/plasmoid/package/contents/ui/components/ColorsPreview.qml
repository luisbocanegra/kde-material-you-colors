pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.plasma.extras as PlasmaExtras

ColumnLayout {
    id: r
    property var mdc: ({})
    Layout.alignment: Qt.AlignHCenter
    spacing: Kirigami.Units.mediumSpacing
    readonly property bool light: mdc.light ?? false
    readonly property string theme: light ? "light" : "dark"
    property var scheme: r.mdc.schemes[r.theme]

    PlasmaExtras.Heading {
        level: 4
        text: "Surfaces"
        color: Kirigami.Theme.textColor
        wrapMode: Text.NoWrap
        Layout.alignment: Qt.AlignHCenter
    }

    GridLayout {
        columns: 2
        rows: 7
        columnSpacing: 0
        rowSpacing: 0
        flow: GridLayout.TopToBottom
        Layout.fillWidth: true
        Repeater {
            model: [
                { role: "background", onRole: "onBackground" },
                { role: "surfaceDim", onRole: "onSurface" },
                { role: "surfaceContainerLowest", onRole: "onSurface" },
                { role: "surfaceContainerLow", onRole: "onSurface" },
                { role: "surfaceContainer", onRole: "onSurface" },
                { role: "surfaceContainerHigh", onRole: "onSurface" },
                { role: "surfaceContainerHighest", onRole: "onSurface" },
                { role: "surface", onRole: "onSurface" },
                { role: "surfaceBright", onRole: "onSurface" }
            ]
            delegate: ColorRolePreview {
                required property var modelData
                role: modelData.role
                onRole: modelData.onRole
                scheme: r.scheme
            }
        }
    }

    PlasmaExtras.Heading {
        level: 4
        text: "Content"
        color: Kirigami.Theme.textColor
        wrapMode: Text.NoWrap
        Layout.alignment: Qt.AlignHCenter
    }

    GridLayout {
        columns: 2
        rows: 10
        columnSpacing: 0
        rowSpacing: 0
        flow: GridLayout.TopToBottom
        Repeater {
            model: [
                { role: "primary", onRole: "onPrimary" },
                { role: "primaryContainer", onRole: "onPrimaryContainer" },
                { role: "primaryFixed", onRole: "onPrimaryFixed" },
                { role: "primaryFixed", onRole: "onPrimaryFixedVariant" },
                { role: "primaryFixedDim", onRole: "onPrimaryFixed" },
                { role: "tertiary", onRole: "onTertiary" },
                { role: "tertiaryContainer", onRole: "onTertiaryContainer" },
                { role: "tertiaryFixed", onRole: "onTertiaryFixed" },
                { role: "tertiaryFixed", onRole: "onTertiaryFixedVariant" },
                { role: "tertiaryFixedDim", onRole: "onTertiaryFixed" },
                { role: "secondary", onRole: "onSecondary" },
                { role: "secondaryContainer", onRole: "onSecondaryContainer" },
                { role: "secondaryFixed", onRole: "onSecondaryFixed" },
                { role: "secondaryFixed", onRole: "onSecondaryFixedVariant" },
                { role: "secondaryFixedDim", onRole: "onSecondaryFixed" },
            ]
            delegate: ColorRolePreview {
                required property var modelData
                role: modelData.role
                onRole: modelData.onRole
                scheme: r.scheme
            }
        }
    }

    PlasmaExtras.Heading {
        level: 4
        text: "Inverse"
        color: Kirigami.Theme.textColor
        wrapMode: Text.NoWrap
        Layout.alignment: Qt.AlignHCenter
    }

    GridLayout {
        columns: 2
        columnSpacing: 0
        rowSpacing: 0
        Repeater {
            model: [
                { role: "inverseSurface", onRole: "inverseOnSurface" },
                { role: "inversePrimary", onRole: "onPrimaryContainer" }
            ]
            delegate: ColorRolePreview {
                required property var modelData
                role: modelData.role
                onRole: modelData.onRole
                scheme: r.scheme
            }
        }
    }

    PlasmaExtras.Heading {
        level: 4
        text: "Utility"
        color: Kirigami.Theme.textColor
        wrapMode: Text.NoWrap
        Layout.alignment: Qt.AlignHCenter
    }

    GridLayout {
        columns: 2
        columnSpacing: 0
        rowSpacing: 0
        Repeater {
            model: [
                { role: "error", onRole: "onError" },
                { role: "errorContainer", onRole: "onErrorContainer" },
                { role: "outline", onRole: "onSurface" },
                { role: "outlineVariant", onRole: "onSurface" },
                { role: "shadow", onRole: "onSurface" },
                { role: "scrim", onRole: "onSurface" }
            ]
            delegate: ColorRolePreview {
                required property var modelData
                role: modelData.role
                onRole: modelData.onRole
                scheme: r.scheme
            }
        }
    }

    PlasmaExtras.Heading {
        level: 4
        text: "Custom color-container (color/onColor)"
        color: Kirigami.Theme.textColor
        wrapMode: Text.NoWrap
        Layout.alignment: Qt.AlignHCenter
    }

    GridLayout {
        columns: 2
        columnSpacing: 0
        rowSpacing: 0
        Repeater {
            model: {
                let pairs = []
                for (const key of Object.keys(r.mdc.custom)) {
                    pairs.push({name: key, role: "color", onRole: "onColor"})
                    pairs.push({name: key, role: "container", onRole: "onContainer"})
                }
                return pairs
            }
            delegate: ColorRolePreview {
                required property var modelData
                role: modelData.role
                onRole: modelData.onRole
                scheme: r.mdc.custom[modelData.name][r.theme]
                customName: `${modelData.name}`
            }
        }
    }
}
