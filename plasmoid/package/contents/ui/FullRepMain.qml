import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.0
import org.kde.kirigami 2.20 as Kirigami
import org.kde.kquickcontrols 2.0
import org.kde.plasma.core 2.0 as PlasmaCore
import Qt.labs.folderlistmodel 2.15
import Qt.labs.settings 1.0
import QtGraphicalEffects 1.12
import org.kde.plasma.components 3.0 as PlasmaComponents3
import org.kde.plasma.extras 2.0 as PlasmaExtras
import org.kde.plasma.plasmoid 2.0
import "components" as Components

PlasmaExtras.Representation {
    id: expandedRepresentation

    property var controlHeight: 36 * PlasmaCore.Units.devicePixelRatio
    property var controlWidth: 48 * PlasmaCore.Units.devicePixelRatio

    property var materialYouData: null
    property var wallpaperPreview: null

    property string configPath
    property string cmd_type: ""

    property bool backendRunning: true
    property string checkBackendCommand: 'ps -C "kde-material-you-colors" -F --no-headers'

    property bool plasmoidExpanded: plasmoid.expanded ||
                                    plasmoid.location === PlasmaCore.Types.Floating ||
                                    plasmoid.location === PlasmaCore.Types.Desktop

    property var scrollVisible: mainLayout.height>expandedRepresentation.height

    property var dividerColor: Kirigami.Theme.textColor
    property var dividerOpacity: 0.1

    //TODO: figure out a reliable way to detect config changes
    signal reloadUI()

    onMaterialYouDataChanged: {
        if (materialYouData !== null) {
            // console.log("@@@ WALLPAPER @@@",materialYouData.pywal.dark.wallpaper)
            // imagePreview.source = materialYouData.pywal.dark.wallpaper
            updateStoredColors()
        }
    }

    PlasmaCore.DataSource {
        id: executable
        engine: "executable"
        connectedSources: []

        onNewData: {
            var exitCode = data["exit code"]
            var exitStatus = data["exit status"]
            var stdout = data["stdout"]
            var stderr = data["stderr"]
            exited(sourceName, exitCode, exitStatus, stdout, stderr)
            disconnectSource(sourceName) // cmd finished
        }

            function exec(cmd,type) {
                cmd_type = type
                executable.connectSource(cmd)
        }

        signal exited(string cmd, int exitCode, int exitStatus, string stdout, string stderr)
    }

    Connections {
        target: executable
        function onExited(cmd, exitCode, exitStatus, stdout, stderr) {
            console.log("COMMAND TYPE",cmd_type)
            // update current brightness
            if (cmd_type == "getConfigPath") {
                configPath = stdout.replace('\n', '').trim()
            }
        }
    }


    PlasmaCore.DataSource {
        id: checkBackend
        engine: "executable"
        connectedSources: []

        onNewData: {
            var exitCode = data["exit code"]
            var exitStatus = data["exit status"]
            var stdout = data["stdout"]
            var stderr = data["stderr"]
            exited(sourceName, exitCode, exitStatus, stdout, stderr)
            disconnectSource(sourceName) // cmd finished
        }

            function exec(cmd) {
                checkBackend.connectSource(cmd)
        }

        signal exited(string cmd, int exitCode, int exitStatus, string stdout, string stderr)
    }


    Connections {
        target: checkBackend
        function onExited(cmd, exitCode, exitStatus, stdout, stderr) {
            backendRunning = stdout.replace('\n', '').trim().length>0
        }
    }

    // read settings file
    // save relevant configs with _last suffix to recover them after reenable
    Settings {
        fileName: configPath
        category: "CUSTOM"
        id: settings
        property int monitor: 0

        property string color
        property string color_last

        property string custom_colors_list
        property string custom_colors_list_last

        property bool light: false
        property int ncolor: 0

        property bool pywal:false
        property bool pywal_light: false

        property real light_blend_multiplier: 1.0
        property real dark_blend_multiplier: 1.0

        property real light_saturation_multiplier: 1.0
        property real dark_saturation_multiplier: 1.0

        property real light_brightness_multiplier: 1.0
        property real dark_brightness_multiplier: 1.0

        property bool gui_global_dark_mode: false

        property bool plasma_follows_scheme: true
        property bool pywal_follows_scheme: true
    }

    function updateStoredColors() {
        var colors = [];
        for (var i = 0; i < colorButtonRepeater.count; i++) {
            var colorBtn = colorButtonRepeater.itemAt(i);
            colors.push(colorBtn.color.toString());
        }
        // do not re-enable custom colors if is disabled
        if (customColorsCheckbox.checked) {
            settings.custom_colors_list = ""
        } else {
            settings.custom_colors_list = colors.join(" ");
            settings.custom_colors_list_last = colors.join(" ");
        }
    }

    function loadMaterialYouData() {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                materialYouData = JSON.parse(xhr.responseText);
                //console.log("Data:", materialYouData);
                //console.log("KEYS:",Object.keys(materialYouData));
                // console.log("DUMP:",JSON.stringify(materialYouData, null, 2));
            }
        }
        xhr.open("GET","file:///tmp/kde-material-you-colors.json")
        xhr.send()
    }

    PlasmaComponents3.ScrollView {
        anchors {
            fill: parent
            leftMargin: PlasmaCore.Units.gridUnit / 2
            rightMargin: 0
        }
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

    ColumnLayout {
        id: mainLayout
        // HACK check if scrollbar is shown to add/remove fake right marging of
        // ColumnLayout inside ScrollView, ideally it should take the available space
        // but I simply don't know how to do that
        width: expandedRepresentation.width - (scrollVisible?PlasmaCore.Units.gridUnit*1.5:PlasmaCore.Units.gridUnit)

        Kirigami.InlineMessage {
            Layout.fillWidth: true
            type: Kirigami.MessageType.Error
            visible: !backendRunning

            text: qsTr("Backend is not running. This Plasmoid requires <a href=\"https://github.com/luisbocanegra/kde-material-you-colors\">kde-material-you-colors</a> to be installed and running to work.")

            onLinkActivated: link => Qt.openUrlExternally(link)

            actions: [
                Kirigami.Action {
                    icon.name: "media-playback-start"
                    text: "Start"
                    onTriggered: {
                        checkBackend.exec("kde-material-you-colors")
                    }
                },
                Kirigami.Action {
                    icon.name: "media-playback-start"
                    text: "Start && enable Autostart"
                    onTriggered: {
                        checkBackend.exec("kde-material-you-colors --autostart;kde-material-you-colors")
                    }
                },
                Kirigami.Action {
                    icon.name: "help-about-symbolic"
                    text: "Install guide"
                    onTriggered: {
                        Qt.openUrlExternally("https://github.com/luisbocanegra/kde-material-you-colors#installing")
                    }
                }
            ]
        }


        PlasmaExtras.Heading {
            level: 1
            text: "Colors source"
            Layout.alignment: Qt.AlignHCenter
            // Layout.alignment: Qt.AlignHCenter|Qt.AlignVCenter
            // Layout.preferredHeight: PlasmaCore.Units.gridUnit * 2
            // Layout.fillWidth: true
        }

        RowLayout {
            Label {
                text: "From Wallpaper"
                Layout.alignment: Qt.AlignHCenter|Qt.AlignVCenter
                // Layout.preferredHeight: PlasmaCore.Units.gridUnit * 2
                // Layout.fillWidth: true
            }
            CheckBox {
                checked: settings.color==""
                onCheckedChanged: {
                    settings.color = checked?"":settings.color_last
                    updateStoredColors()
                }
            }

            Item { implicitWidth: PlasmaCore.Units.gridUnit / 2}

            // Monitor number
            Label {
                visible: settings.color==""
                text: "Monitor/Screen number"
                Layout.alignment: Qt.AlignLeft
                // Layout.fillWidth: true
            }

            TextField {
                id: monitorNumber
                visible: settings.color==""
                Layout.preferredWidth: controlWidth
                topPadding: 10
                bottomPadding: 10
                leftPadding: 10
                rightPadding: 10
                placeholderText: "0-?"
                horizontalAlignment: TextInput.AlignHCenter
                text: parseInt(settings.monitor)
                // Layout.fillWidth: true
                validator: IntValidator {
                    bottom: 0
                }

                onAccepted: {
                    settings.monitor = parseInt(text)
                    // reset color selection
                    settings.ncolor = 0
                }
            }

        }



        // Color selection
        RowLayout {
            Layout.preferredWidth: mainLayout.width
            // height: 100
            // width: parent.width
            // Layout.fillWidth: true

            Label {
                text: "Select color"
                id:selectColorLabel
                // Layout.alignment: Qt.AlignHCenter|Qt.AlignVCenter
                // Layout.preferredHeight: PlasmaCore.Units.gridUnit * 2
                // Layout.fillWidth: true
            }

            // Single color
            Components.CustomColorButton { // Components.Custom
                id: colorButton
                Layout.alignment: Qt.AlignHCenter
                visible: settings.color!==""
                showAlphaChannel: false
                dialogTitle: "Choose source color"
                Layout.preferredHeight: controlHeight
                Layout.preferredWidth: controlWidth
                color: settings.color?settings.color:settings.color_last
                onAccepted: {
                    settings.color = colorButton.color.toString()
                    settings.color_last = settings.color
                }
            }

            // multiple colors
            // TODO: center rows
            GridLayout { //PlasmaComponents3.ScrollView
                property var gridSpacing: PlasmaCore.Units.mediumSpacing
                visible: settings.color===""
                columns: Math.floor((mainLayout.width - selectColorLabel.width) / (
                    controlHeight * .75 + gridSpacing))
                rowSpacing: gridSpacing
                columnSpacing: gridSpacing

                Layout.alignment: Qt.AlignRight

                Repeater {
                    id: circleRepeater
                    model: materialYouData ? Object.keys(materialYouData.best) : []
                    delegate: Item {
                        Layout.preferredWidth: controlHeight * .75
                        Layout.preferredHeight: controlHeight * .75

                        property string color1: Kirigami.ColorUtils.brightnessForColor(materialYouData.best[index]) === Kirigami.ColorUtils.Dark ? "#ffffff":"#000000"
                        property string hoverColor: Kirigami.ColorUtils.tintWithAlpha(materialYouData.best[index],color1, .18)
                        property string selectColor: Kirigami.ColorUtils.tintWithAlpha(materialYouData.best[index],color1, .7)

                        Rectangle {
                            anchors.fill: parent
                            radius: parent.height

                            color: settings.ncolor==index?circleRepeater.itemAt(index).selectColor:materialYouData.best[index]
                            border.width: parent.width / 4
                            border.color: materialYouData.best[index]
                        }

                        DropShadow {
                            anchors.fill: circleRepeater.itemAt(index).children[0]
                            source: circleRepeater.itemAt(index).children[0]
                            verticalOffset: 0.5
                            radius: 4
                            // samples: 5
                            color: "#80000000"
                        }

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true

                            onEntered: {
                                circleRepeater.itemAt(index).children[0].border.color = circleRepeater.itemAt(index).hoverColor
                                if (index!=settings.ncolor){
                                    circleRepeater.itemAt(index).children[0].color = circleRepeater.itemAt(index).hoverColor
                                }
                            }

                            onExited: {
                                circleRepeater.itemAt(index).children[0].border.color = materialYouData.best[index]
                                if (index!=settings.ncolor){
                                    circleRepeater.itemAt(index).children[0].color = materialYouData.best[index]
                                }
                            }

                            onClicked: {
                                console.log("SELECTED COLOR:",materialYouData.best[index])
                                settings.ncolor = index

                                for (let i=0; i < circleRepeater.count; i++) {
                                    if (i == settings.ncolor){
                                        circleRepeater.itemAt(i).children[0].color = circleRepeater.itemAt(index).selectColor
                                    } else {
                                        circleRepeater.itemAt(i).children[0].color = materialYouData.best[i]
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }


        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: dividerColor
            opacity: dividerOpacity
        }

        // CUSTOM COLOR LIST
        PlasmaExtras.Heading {
            level: 1
            text: "Text colors"
            Layout.alignment: Qt.AlignHCenter
        }

        RowLayout {
            Layout.preferredWidth: mainLayout.width
            // Layout.fillWidth: true
            Label {
                text: "From Wallpaper"
                Layout.alignment: Qt.AlignHCenter|Qt.AlignVCenter
                // Layout.preferredHeight: PlasmaCore.Units.gridUnit * 2

            }
            CheckBox {
                id:customColorsCheckbox
                checked: settings.custom_colors_list==""
                Layout.fillWidth: true
                onCheckedChanged: {
                    settings.custom_colors_list = checked?"":settings.custom_colors_list_last
                }
            }
        }

        Label {
            visible: settings.custom_colors_list !==""
            text: "Tap each button to change color"
            Layout.alignment: Qt.AlignHCenter
            // Layout.fillWidth: true
            // width: parent.width
            opacity: 0.7
        }

        RowLayout {
            Layout.preferredWidth: mainLayout.width

            RowLayout {
                // width: parent.width
                // Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter
                visible: settings.custom_colors_list!==""
                Repeater {
                    model: 7
                    id: colorButtonRepeater
                    delegate: Components.CustomColorButton {
                        showAlphaChannel: false
                        dialogTitle: "Choose custom color"
                        Layout.preferredHeight: controlHeight
                        Layout.preferredWidth: controlWidth

                        color: settings.custom_colors_list.split(" ")[index]

                        onAccepted: updateStoredColors()
                    }
                }
                // Component.onCompleted: updateStoredColors()
            }

            RowLayout {
                // width: parent.width
                // Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter
                visible: settings.custom_colors_list===""
                Repeater {
                    model: materialYouData ? Object.keys(materialYouData.pywal.dark.colors).slice(1,8) : []

                    delegate: Item {
                        Layout.preferredWidth: controlHeight * .75
                        Layout.preferredHeight: controlHeight * .75

                        Rectangle {
                            anchors.fill: parent
                            radius: parent.height
                            color: materialYouData.pywal.dark.colors["color"+(index+1).toString()]
                        }
                    }
                }
            }
        }

        Label {
            text: "Applies to Konsole, Pywal, KSyntaxHighlighting"
            Layout.alignment: Qt.AlignHCenter
            // Layout.fillWidth: true
            // width: parent.width
            opacity: 0.7
        }


        // PYWAL
        RowLayout {
            Label {
                text: "Apply to pywal"
                Layout.alignment: Qt.AlignLeft
            }

            CheckBox {
                id: enablePywal
                checked: settings.pywal

                onCheckedChanged: {
                    settings.pywal = checked
                }
            }
        }


        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: dividerColor
            opacity: dividerOpacity
        }

        // DARK MODE
        PlasmaExtras.Heading {
            level: 1
            text: "Dark mode"
            Layout.alignment: Qt.AlignHCenter
        }

        RowLayout {
            ColumnLayout {
                Label {
                    text: "Plasma"
                    Layout.alignment: Qt.AlignLeft
                }

                ButtonGroup {
                    id: plasmaModeGroup
                }

                RadioButton {
                    id:plasmaEnableDark
                    checked: !settings.light
                    text: qsTr("Enabled")
                    onCheckedChanged: {
                        settings.light = !checked
                    }
                    ButtonGroup.group: plasmaModeGroup
                }

                RadioButton {
                    checked: !plasmaEnableDark.checked && !plasmaFollowScheme.checked//settings.light
                    text: qsTr("Disabled")

                    ButtonGroup.group: plasmaModeGroup
                }

                RadioButton {
                    id: plasmaFollowScheme
                    checked: settings.plasma_follows_scheme
                    text: qsTr("Follow color scheme")
                    onCheckedChanged: {
                            settings.plasma_follows_scheme = checked
                    }
                    ButtonGroup.group: plasmaModeGroup
                }
            }

            Item { Layout.fillWidth: true}

            ColumnLayout {
                Label {
                    text: "Konsole, Pywal, KSyntaxHighlighting"
                    Layout.alignment: Qt.AlignLeft
                }

                ButtonGroup {
                    id: pywalModeGroup
                }

                RadioButton {
                    id:pywalEnableDark
                    checked: !settings.pywal_light
                    text: qsTr("Enabled")
                    onCheckedChanged: {
                        settings.pywal_light = !checked
                    }
                    ButtonGroup.group: pywalModeGroup
                }

                RadioButton {
                    checked: !pywalEnableDark.checked && !pywalFollowScheme.checked//settings.light
                    text: qsTr("Disabled")

                    ButtonGroup.group: pywalModeGroup
                }

                RadioButton {
                    id: pywalFollowScheme
                    checked: settings.pywal_follows_scheme
                    text: qsTr("Follow color scheme")
                    onCheckedChanged: {
                            settings.pywal_follows_scheme = checked
                    }
                    ButtonGroup.group: pywalModeGroup
                }
            }
        }

        Text {
            text: "<i>Follow color scheme</i> applies only for Material You color schemes when changed by you or other programs"
            Layout.alignment: Qt.AlignHCenter
            // Layout.fillWidth: true
            Layout.preferredWidth: parent.width
            opacity: 0.7
            color: Kirigami.Theme.textColor
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
        }

        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: dividerColor
            opacity: dividerOpacity
        }

        PlasmaExtras.Heading {
            level: 1
            text: "Color amount"
            Layout.alignment: Qt.AlignHCenter
            // Layout.alignment: Qt.AlignHCenter|Qt.AlignVCenter
            // Layout.preferredHeight: PlasmaCore.Units.gridUnit * 2
            // Layout.fillWidth: true
        }

        // Dark blend
        RowLayout {
            width: parent.width
            Layout.fillWidth: true
            Label {
                text: "Dark blend"
                Layout.alignment: Qt.AlignLeft
                // Layout.fillWidth: true
            }

            Slider {
                id: darkBlend
                value: settings.dark_blend_multiplier
                from: 0
                to: 4.0
                stepSize: 0.2
                Layout.fillWidth: true
                onValueChanged: {
                    settings.dark_blend_multiplier = Math.round(value * 10) / 10
                }
            }

            TextField {
                id: darkBlendManual
                Layout.preferredWidth: controlWidth
                topPadding: 10
                bottomPadding: 10
                leftPadding: 10
                rightPadding: 10
                placeholderText: "0-4"
                horizontalAlignment: TextInput.AlignHCenter
                text: parseFloat(settings.dark_blend_multiplier)
                // Layout.fillWidth: true
                validator: DoubleValidator {
                    bottom: 0.0
                    top: 4.0
                    decimals: 1
                    notation: DoubleValidator.StandardNotation
                }

                onAccepted: {
                    settings.dark_blend_multiplier = parseFloat(text)
                }
            }
        }


        // Light blend
        RowLayout {
            width: parent.width
            Layout.fillWidth: true
            Label {
                text: "Light blend"
                Layout.alignment: Qt.AlignLeft
                // Layout.fillWidth: true
            }

            Slider {
                id: lightBlend
                value: settings.light_blend_multiplier
                from: 0
                to: 4.0
                stepSize: 0.2
                Layout.fillWidth: true
                onValueChanged: {
                    settings.light_blend_multiplier = Math.round(value * 10) / 10
                }
            }

            TextField {
                id: lightBlendManual
                Layout.preferredWidth: controlWidth
                topPadding: 10
                bottomPadding: 10
                leftPadding: 10
                rightPadding: 10
                placeholderText: "0-4"
                horizontalAlignment: TextInput.AlignHCenter
                text: parseFloat(settings.light_blend_multiplier)
                // Layout.fillWidth: true
                validator: DoubleValidator {
                    bottom: 0.0
                    top: 4.0
                    decimals: 1
                    notation: DoubleValidator.StandardNotation
                }

                onAccepted: {
                    settings.light_blend_multiplier = parseFloat(text)
                }
            }
        }


        // Rectangle {
        //     Layout.fillWidth: true
        //     height: 1
        //     color: dividerColor
        //     opacity: dividerOpacity
        // }


        // //Dark Saturation
        // RowLayout {
        //     width: parent.width
        //     Layout.fillWidth: true
        //     Label {
        //         text: "Dark saturation"
        //         Layout.alignment: Qt.AlignLeft
        //         // Layout.fillWidth: true
        //     }

        //     Slider {
        //         id: darkSat
        //         value: settings.dark_saturation_multiplier
        //         from: 0
        //         to: 4.0
        //         stepSize: 0.2
        //         Layout.fillWidth: true
        //         onValueChanged: {
        //             settings.dark_saturation_multiplier = Math.round(value * 10) / 10
        //         }
        //     }

        //     TextField {
        //         id: darkSatManual
        //         Layout.preferredWidth: controlWidth
        //         topPadding: 10
        //         bottomPadding: 10
        //         leftPadding: 10
        //         rightPadding: 10
        //         placeholderText: "0-4"
        //         horizontalAlignment: TextInput.AlignHCenter
        //         text: parseFloat(settings.dark_saturation_multiplier)
        //         // Layout.fillWidth: true
        //         validator: DoubleValidator {
        //             bottom: 0.0
        //             top: 4.0
        //             decimals: 1
        //             notation: DoubleValidator.StandardNotation
        //         }

        //         onAccepted: {
        //             settings.dark_saturation_multiplier = parseFloat(text)
        //         }
        //     }
        // }


        // Rectangle {
        //     Layout.fillWidth: true
        //     height: 1
        //     color: dividerColor
        //     opacity: dividerOpacity
        // }

        Component.onCompleted: {
            loadMaterialYouData()
            executable.exec('echo ${HOME}/.config/kde-material-you-colors/config.conf',"getConfigPath")
            checkBackend.exec(checkBackendCommand)
            statupTimer.start()
        }

        Timer {
            interval: 1000;
            running: plasmoidExpanded
            repeat: true;
            onTriggered: {
                loadMaterialYouData()
                checkBackend.exec(checkBackendCommand)
                //console.log("Main H:",mainLayout.height," View H:",expandedRepresentation.height);
            }
        }

        Timer {
            id: statupTimer
            interval: 500
            repeat: false

            onTriggered: {
                console.log("@@@@@ BACKEND RUNNING:", backendRunning)
                console.log("@@@@@ Config file:", settings.fileName);
                // Default colors
                if(settings.color_last==="") {
                    settings.color_last = "#66a3ef"
                }
                if (settings.custom_colors_list_last==="") {
                    settings.custom_colors_list_last = "#d0265c #74e448 #eece4f #66a3ef #532066 #297d81 #ccc1c1"
                }
            }
        }
    }
    }
}
