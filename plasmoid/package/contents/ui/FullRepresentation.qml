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
    Layout.minimumWidth: Plasmoid.switchWidth
    Layout.minimumHeight: Plasmoid.switchHeight

    Layout.preferredWidth: PlasmaCore.Units.gridUnit * 26
    Layout.preferredHeight: PlasmaCore.Units.gridUnit * 50
    
    Layout.maximumWidth: mainLayout.implicitWidth //PlasmaCore.Units.gridUnit * 50
    Layout.maximumHeight: mainLayout.implicitHeight + PlasmaCore.Units.gridUnit * 4 //PlasmaCore.Units.gridUnit * 60

    readonly property int controlSize: PlasmaCore.Units.iconSizes.medium
    
    property var colorPickerHeight: 36
    property var colorPickerWidth: 48
    property var slideWidth: 250

    property var materialYouData: null
    property var wallpaperPreview: null

    property string configPath
    property string cmd_type: ""

    property alias colorsFromWallpaper: settings.color

    property alias textColorsFromWallpaper: settings.custom_colors_list

    onMaterialYouDataChanged: {
        if (materialYouData !== null) {
            // console.log("@@@ WALLPAPER @@@",materialYouData.pywal.dark.wallpaper)
            // imagePreview.source = materialYouData.pywal.dark.wallpaper
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
                //executable.exec(currentBrightnessCommand(monitor_name),"")
                // console.log("Current brightness -> "+monitor_name +" -> "+stdout)
                configPath = stdout.replace('\n', '').trim()
            }

            // // update monitors list
            // if (cmd_type == "updateMonitors") {
            //     main.mon_list = stdout.split('\n')
            //     items.clear()
            //     if (main.mon_list.length > 0) {
            //         for (var i = 0; i < main.mon_list.length; ++i) {
            //             if ( main.mon_list[i] != "") {
            //                 items.append({"name": main.mon_list[i]})
            //             }
            //         }
            //     }
            //     // set default monitor
            //     if (monitor_name === '') {
            //         monitor_name = main.mon_list[0]
            //         executable.exec(currentBrightnessCommand(monitor_name),"updateCurrentBrightness")
            //     }
            //     console.log(mon_list_Command())
            // }
            // if (cmd_type == "setBrightness") {
            //     console.log(changeBrightnessCommand(monitor_name,currentBrightness));
            // }
        }
    }


    // read settings file
    // save relevant configs with _last suffix
    // to recover them after reenable
    Settings {
        fileName: configPath //+"" //FolderListModel.homePath()+"/.config/kde-material-you-colors/config.conf"
        category: "CUSTOM"
        id: settings
        property int monitor: 0
        // property string plugin: "org.kde.image"
        // property string file

        property string color
        property string color_last

        property string custom_colors_list
        property string custom_colors_list_last

        property bool light: false
        property int ncolor: 0

        // property string iconslight: "Breeze"
        // property string iconsdark: "Breeze"
        
        property bool pywal:false
        property bool pywal_light: false

        property real light_blend_multiplier: 1.0
        property real dark_blend_multiplier: 1.0

        property real light_saturation_multiplier: 1.0
        property real dark_saturation_multiplier: 1.0

        property real light_brightness_multiplier: 1.0
        property real dark_brightness_multiplier: 1.0

        // property string on_change_hook

        // property bool sierra_breeze_buttons_color: false
        // property string konsole_profile
        // property int konsole_opacity: 100

        // property int titlebar_opacity: 100

        // property int toolbar_opacity: 100

        // property bool klassy_windeco_outline: false

        // property string darker_window_list

        // property bool use_startup_delay:false

        // property int startup_delay

    }

    function updateStoredColors() {
        var colors = [];
        for (var i = 0; i < colorButtonRepeater.count; i++) {
            var colorBtn = colorButtonRepeater.itemAt(i);
            colors.push(colorBtn.color.toString());
        }
        settings.custom_colors_list = colors.join(" ");
        settings.custom_colors_list_last = colors.join(" ");
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


    ColumnLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true
        // Layout.preferredWidth: 50
        // Layout.preferredHeight: 50
        // Layout.preferredWidth: parent.width
        anchors {
            fill: parent
            leftMargin: PlasmaCore.Units.mediumSpacing
            rightMargin: PlasmaCore.Units.mediumSpacing
        }
        id: mainLayout
        
        PlasmaExtras.Heading {
            level: 1
            text: "Colors source"
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
                checked: colorsFromWallpaper==""
                onCheckedChanged: {
                    settings.color = checked?"":settings.color_last
                    updateStoredColors()
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
                text: "Source color"
                // Layout.alignment: Qt.AlignHCenter|Qt.AlignVCenter
                // Layout.preferredHeight: PlasmaCore.Units.gridUnit * 2
                Layout.fillWidth: true
            }

            // Single color
            Components.CustomColorButton { // Components.Custom
                id: colorButton
                Layout.alignment: Qt.AlignHCenter
                visible: settings.color!==""
                showAlphaChannel: false
                dialogTitle: "Choose source color"
                Layout.preferredHeight: colorPickerHeight
                Layout.preferredWidth: colorPickerWidth
                // color:"red"
                color: "#ff0000"
                onAccepted: {
                    settings.color = colorButton.color.toString()
                    settings.color_last = settings.color
                }
            }

            // multiple colors
            // TODO: center rows
            GridLayout { //PlasmaComponents3.ScrollView
                visible: settings.color===""
                // Layout.alignment: Qt.AlignTop | Qt.AlignHCenter
                // Layout.alignment: Qt.AlignHCenter
                // Layout.preferredWidth: mainLayout.width - PlasmaCore.Units.gridUnit
                // Layout.preferredHeight: PlasmaCore.Units.gridUnit
                columns: 12
                // Layout.preferredHeight: colorPickerHeight * .75
                //RowLayout {
                    //spacing: PlasmaCore.Units.gridUnit / 2
                    Layout.alignment: Qt.AlignHCenter
                    // Layout.preferredWidth: mainLayout.width
                    
                    Repeater {
                        id: circleRepeater
                        model: materialYouData ? Object.keys(materialYouData.best) : []
                        delegate: Item {
                            Layout.preferredWidth: colorPickerHeight * .75
                            Layout.preferredHeight: colorPickerHeight * .75

                            Rectangle {
                                anchors.fill: parent
                                radius: parent.height
                                color: materialYouData.best[index]
                                border.width: 3
                                border.color: settings.ncolor==index?Kirigami.Theme.textColor:materialYouData.best[index]
                            }

                            // Label {
                            //     anchors.centerIn: parent
                            //     text: index
                            //     font.pixelSize: 12
                            //     // style: Text.Outline
                            //     // styleColor: "black"
                            //     color: "white"
                            //     horizontalAlignment: TextInput.AlignHCenter
                            //     verticalAlignment: TextInput.AlignVCenter
                            // }

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
                                    var hoverColor = Kirigami.ColorUtils.linearInterpolation(Kirigami.Theme.backgroundColor, materialYouData.best[index], .5)
                                    //var hoverColor = Kirigami.ColorUtils.adjustColor(materialYouData.best[index], {"value": -80})
                                    circleRepeater.itemAt(index).children[0].color = hoverColor
                                }

                                onExited: {
                                    circleRepeater.itemAt(index).children[0].color = materialYouData.best[index]
                                }

                                onClicked: {
                                    console.log("SELECTED COLOR:",materialYouData.best[index])
                                    settings.ncolor = index

                                    for (let i=0; i < circleRepeater.count; i++) {
                                        if (i == settings.ncolor){
                                            circleRepeater.itemAt(i).children[0].border.color = Kirigami.Theme.textColor
                                        } else {
                                            circleRepeater.itemAt(i).children[0].border.color = materialYouData.best[i]
                                        }
                                    }
                                }
                            }
                        }
                    }
                //}
            }
        }


        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: Kirigami.ColorUtils.linearInterpolation(Kirigami.Theme.backgroundColor, Kirigami.Theme.textColor, 0.12)
        }

        // CUSTOM COLOR LIST
        ColumnLayout{

            PlasmaExtras.Heading {
                level: 1
                text: "Text colors"
                // Layout.alignment: Qt.AlignHCenter|Qt.AlignVCenter
                // Layout.preferredHeight: PlasmaCore.Units.gridUnit * 2
                // Layout.fillWidth: true
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
                checked: textColorsFromWallpaper==""
                Layout.fillWidth: true
                onCheckedChanged: {
                    settings.custom_colors_list = checked?"":settings.custom_colors_list_last
                    // updateStoredColors()
                }
            }
        }

        
        RowLayout {
            Layout.preferredWidth: mainLayout.width

            // Label {
            //     text: "Text colors"
            //     Layout.alignment: Qt.AlignHCenter
            //     Layout.fillWidth: true
            //     // width: parent.width
            // }



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
                        Layout.preferredHeight: colorPickerHeight
                        Layout.preferredWidth: colorPickerWidth
                        
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
                        Layout.preferredWidth: colorPickerHeight * .75
                        Layout.preferredHeight: colorPickerHeight * .75

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
        }


        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: Kirigami.ColorUtils.linearInterpolation(Kirigami.Theme.backgroundColor, Kirigami.Theme.textColor, 0.12)
        }


        // DARK MODE
        RowLayout {
            Label {
                text: "Dark mode"
                Layout.alignment: Qt.AlignLeft
            }

            CheckBox {
                id: darkMode
                checked: !settings.light

                onCheckedChanged: {
                    settings.light = !checked
                }
            }
        }


        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: Kirigami.ColorUtils.linearInterpolation(Kirigami.Theme.backgroundColor, Kirigami.Theme.textColor, 0.12)
        }


        // PYWAL
        RowLayout {
            Label {
                text: "Apply colors to pywal"
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
            color: Kirigami.ColorUtils.linearInterpolation(Kirigami.Theme.backgroundColor, Kirigami.Theme.textColor, 0.12)
        }


        // Dark blend
        RowLayout {
            width: parent.width
            Layout.fillWidth: true
            Label {
                text: "Dark blend multiplier"
                Layout.alignment: Qt.AlignLeft
                Layout.fillWidth: true
            }

            Slider {
                id: darkBlend
                value: settings.dark_blend_multiplier
                from: 0
                to: 4.0
                stepSize: 0.2
                Layout.preferredWidth: slideWidth
                onValueChanged: {
                    settings.dark_blend_multiplier = Math.round(value * 10) / 10
                }
            }

            TextField {
                id: darkBlendManual
                Layout.preferredWidth: colorPickerWidth
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


        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: Kirigami.ColorUtils.linearInterpolation(Kirigami.Theme.backgroundColor, Kirigami.Theme.textColor, 0.12)
        }


        // Light blend
        RowLayout {
            width: parent.width
            Layout.fillWidth: true
            Label {
                text: "Light blend multiplier"
                Layout.alignment: Qt.AlignLeft
                Layout.fillWidth: true
            }

            Slider {
                id: lightBlend
                value: settings.light_blend_multiplier
                from: 0
                to: 4.0
                stepSize: 0.2
                Layout.preferredWidth: slideWidth
                onValueChanged: {
                    settings.light_blend_multiplier = Math.round(value * 10) / 10
                }
            }

            TextField {
                id: lightBlendManual
                Layout.preferredWidth: colorPickerWidth
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


        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: Kirigami.ColorUtils.linearInterpolation(Kirigami.Theme.backgroundColor, Kirigami.Theme.textColor, 0.12)
        }


        // Dark Saturation
        RowLayout {
            width: parent.width
            Layout.fillWidth: true
            Label {
                text: "Dark saturation multiplier"
                Layout.alignment: Qt.AlignLeft
                Layout.fillWidth: true
            }

            Slider {
                id: darkSat
                value: settings.dark_saturation_multiplier
                from: 0
                to: 4.0
                stepSize: 0.2
                Layout.preferredWidth: slideWidth
                onValueChanged: {
                    settings.dark_saturation_multiplier = Math.round(value * 10) / 10
                }
            }

            TextField {
                id: darkSatManual
                Layout.preferredWidth: colorPickerWidth
                topPadding: 10
                bottomPadding: 10
                leftPadding: 10
                rightPadding: 10
                placeholderText: "0-4"
                horizontalAlignment: TextInput.AlignHCenter
                text: parseFloat(settings.dark_saturation_multiplier)
                // Layout.fillWidth: true
                validator: DoubleValidator {
                    bottom: 0.0
                    top: 4.0
                    decimals: 1
                    notation: DoubleValidator.StandardNotation
                }

                onAccepted: {
                    settings.dark_saturation_multiplier = parseFloat(text)
                }
            }
        }


        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: Kirigami.ColorUtils.linearInterpolation(Kirigami.Theme.backgroundColor, Kirigami.Theme.textColor, 0.12)
        }


        // Monitor number
        RowLayout {
            width: parent.width
            Layout.fillWidth: true
            Label {
                text: "Monitor/Screen number"
                Layout.alignment: Qt.AlignLeft
                Layout.fillWidth: true
            }

            TextField {
                id: monitorNumber
                Layout.preferredWidth: colorPickerWidth
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
                }
            }
        }

        Component.onCompleted: {
            loadMaterialYouData()
            // console.log("Home directory: " + FolderListModel.homePath())
            executable.exec('echo ${HOME}/.config/kde-material-you-colors/config.conf',"getConfigPath")
            //configPath
            // settings.sync()
            // settings.color = checked?"":settings.color_last
            statupTimer.start()
        }

        // onMaterialYouDataChanged: {
        //     console.log("CHANGED:",materialYouData.keys);
        // }

        // PlasmaComponents3.ScrollView {
        //     visible: settings.color===""
        //     ScrollBar.horizontal.policy: ScrollBar.AlwaysOn
        //     ScrollBar.vertical.policy: ScrollBar.AlwaysOff
        //     Layout.fillWidth: true
        //     Layout.preferredHeight: colorPickerHeight * .75
        //     RowLayout {
        //         spacing: PlasmaCore.Units.gridUnit / 2
        //         Repeater {
        //             id: circleRepeater
        //             model: materialYouData ? Object.keys(materialYouData.best) : []
        //             delegate: Item {
        //                 Layout.preferredWidth: colorPickerHeight * .75
        //                 Layout.preferredHeight: colorPickerHeight * .75

        //                 Rectangle {
        //                     anchors.fill: parent
        //                     radius: parent.height
        //                     color: materialYouData.best[index]
        //                     border.width: 3
        //                     border.color: settings.ncolor==index?Kirigami.Theme.textColor:materialYouData.best[index]
        //                 }

        //                 // Label {
        //                 //     anchors.centerIn: parent
        //                 //     text: index
        //                 //     font.pixelSize: 12
        //                 //     // style: Text.Outline
        //                 //     // styleColor: "black"
        //                 //     color: "white"
        //                 //     horizontalAlignment: TextInput.AlignHCenter
        //                 //     verticalAlignment: TextInput.AlignVCenter
        //                 // }

        //                 // DropShadow {
        //                 //     anchors.fill: circleRepeater.itemAt(index).children[1]
        //                 //     source: circleRepeater.itemAt(index).children[1]
        //                 //     verticalOffset: 1
        //                 //     radius: 3
        //                 //     // samples: 5
        //                 //     color: "#80000000"
        //                 // }
                        
        //                 MouseArea {
        //                     anchors.fill: parent
        //                     hoverEnabled: true

        //                     onEntered: {
        //                         var hoverColor = Kirigami.ColorUtils.linearInterpolation(Kirigami.Theme.backgroundColor, materialYouData.best[index], .5)
        //                         //var hoverColor = Kirigami.ColorUtils.adjustColor(materialYouData.best[index], {"value": -80})
        //                         circleRepeater.itemAt(index).children[0].color = hoverColor
        //                     }

        //                     onExited: {
        //                         circleRepeater.itemAt(index).children[0].color = materialYouData.best[index]
        //                     }

        //                     onClicked: {
        //                         console.log("SELECTED COLOR:",materialYouData.best[index])
        //                         settings.ncolor = index

        //                         for (let i=0; i < circleRepeater.count; i++) {
        //                             if (i == settings.ncolor){
        //                                 circleRepeater.itemAt(i).children[0].border.color = Kirigami.Theme.textColor
        //                             } else {
        //                                 circleRepeater.itemAt(i).children[0].border.color = materialYouData.best[i]
        //                             }
        //                         }
        //                     }
        //                 }
        //             }
        //         }
        //     }
        // }

        Timer {
            interval: 500;
            running: true;
            repeat: true;
            onTriggered: {
                loadMaterialYouData()
                console.log("@@@@@@@@ config", configPath);
            }
        }

        Timer {
            id: statupTimer
            interval: 500
            repeat: false
            onTriggered: {
                if (settings.color_last===""){
                    settings.color_last="#ff0000"
                    colorButton.color = "#ff0000"
                } else {
                    colorButton.color = settings.color_last
                }

                if (settings.custom_colors_list!=="") {
                    settings.custom_colors_list_last = settings.custom_colors_list
                }
            }
        }
    }
}

