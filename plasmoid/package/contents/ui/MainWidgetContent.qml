import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.0
import QtGraphicalEffects 1.12

import Qt.labs.platform 1.1
import Qt.labs.settings 1.0

import org.kde.kirigami 2.20 as Kirigami
import org.kde.plasma.extras 2.0 as PlasmaExtras
import org.kde.plasma.core 2.0 as PlasmaCore
import "components" as Components

ColumnLayout {
    property var controlHeight: 36 * PlasmaCore.Units.devicePixelRatio
    property var controlWidth: 48 * PlasmaCore.Units.devicePixelRatio

    property var materialYouData: null
    property var materialYouDataString: null

    property bool plasmoidExpanded: plasmoid.expanded || plasmoid.location === PlasmaCore.Types.Floating


    // read settings file
    // save relevant configs with _last suffix to recover them after reenable
    Settings {
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

        property bool plasma_follows_scheme: true
        property bool pywal_follows_scheme: true

        Component.onCompleted: {
            settings.fileName = StandardPaths.writableLocation(
                    StandardPaths.HomeLocation).toString().substring(7) +
                    "/.config/kde-material-you-colors/config.conf"
        }
    }

    onMaterialYouDataChanged: {
        if (materialYouData!=null && materialYouDataString!=null) {
            if (JSON.stringify(materialYouData) !== materialYouDataString) {
                console.log("@@@ MATERIAL YOU DATA CHANGED @@@");
                console.log(materialYouData,materialYouDataString);
            }
            materialYouDataString = JSON.stringify(materialYouData);
        }
    }

    function saveCustomColorsList() {
        var colors = [];
        for (var i = 0; i < colorPickerRepeater.count; i++) {
            var colorBtn = colorPickerRepeater.itemAt(i);
            colors.push(colorBtn.color.toString());
        }
        // do not re-enable custom colors if is disabled
        if (customTextColorsCheck.checked) {
            settings.custom_colors_list = ""
        } else {
            settings.custom_colors_list = colors.join(" ");
            settings.custom_colors_list_last = colors.join(" ");
        }
    }

    PlasmaCore.DataSource {
        id: readMaterialYouData
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

            function exec() {
                readMaterialYouData.connectSource("cat /tmp/kde-material-you-colors.json")
        }

        signal exited(string cmd, int exitCode, int exitStatus, string stdout, string stderr)
    }

    Connections {
        target: readMaterialYouData
        function onExited(cmd, exitCode, exitStatus, stdout, stderr) {
            materialYouData = JSON.parse(stdout)
        }
    }

    // COLOR SELECTION FROM WALLPAPER OR CUSTOM COLOR
    PlasmaExtras.Heading {
        level: 1
        text: "Colors source"
        Layout.alignment: Qt.AlignHCenter
    }

    RowLayout {
        Label {
            text: "From Wallpaper"
            Layout.alignment: Qt.AlignHCenter|Qt.AlignVCenter
        }

        CheckBox {
            checked: settings.color==""
            onCheckedChanged: {
                settings.color = checked?"":settings.color_last
                //saveCustomColorsList()
            }
        }

        Item { implicitWidth: PlasmaCore.Units.gridUnit / 2}

        // Monitor number when wallpaper colors is enabled
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

        Label {
            text: "Select color"
            id:selectColorLabel
        }

        // Single color picker when color is not empty
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

        // Choose color from wallpaper when colors is not set
        // IDEA: center buttons in separate row maybe?
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
        Layout.preferredWidth: mainLayout.width
        height: 1
        color: dividerColor
        opacity: dividerOpacity
    }

    // TEXT COLORS SECTION
    PlasmaExtras.Heading {
        level: 1
        text: "Text colors"
        Layout.alignment: Qt.AlignHCenter
    }
    // Enable/disable taking text colors from wallpaper
    RowLayout {
        Label {
            id:customTextColorsLabel
            text: "From Wallpaper/color"
            Layout.alignment: Qt.AlignHCenter|Qt.AlignVCenter
        }
        CheckBox {
            id:customTextColorsCheck
            checked: settings.custom_colors_list==""
            onCheckedChanged: {
                settings.custom_colors_list = checked?"":settings.custom_colors_list_last
            }
        }
    }

    // Show color picker buttons when custom_colors_list is not set
    // Hint
    Label {
        visible: settings.custom_colors_list !==""
        text: "Tap each button to change color"
        Layout.alignment: Qt.AlignHCenter
        opacity: 0.7
    }

    // Row of color pickers
    RowLayout {
        Layout.alignment: Qt.AlignHCenter
        visible: settings.custom_colors_list!==""
        Repeater {
            model: 7
            id: colorPickerRepeater
            delegate: Components.CustomColorButton {
                showAlphaChannel: false
                dialogTitle: "Choose custom color"
                Layout.preferredHeight: controlHeight
                Layout.preferredWidth: controlWidth
                property var colorList: settings.custom_colors_list ?
                                        settings.custom_colors_list :
                                        settings.custom_colors_list_last
                color: colorList.split(" ")[index]

                onAccepted: saveCustomColorsList()
            }
        }
        // Component.onCompleted: saveCustomColorsList()
    }

    // Row of non clickable colors from a color or wallpaper
    RowLayout {
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

    Label {
        text: "Applies to Konsole, Pywal, KSyntaxHighlighting"
        Layout.alignment: Qt.AlignHCenter
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
        Layout.preferredWidth: mainLayout.width
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
    // Headings
    RowLayout {
        ColumnLayout {
            Layout.preferredWidth: mainLayout.width / 2

            PlasmaExtras.Heading {
                text: "Plasma"
                Layout.alignment: Qt.AlignHCenter|Qt.AlignVCenter
                Layout.preferredWidth: parent.width
                color: Kirigami.Theme.textColor
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                level: 2
            }
        }

        ColumnLayout {
            Layout.preferredWidth: mainLayout.width/2

            PlasmaExtras.Heading {
                text: "Konsole, Pywal, KSyntaxHighlighting"
                Layout.alignment: Qt.AlignHCenter|Qt.AlignVCenter
                Layout.preferredWidth: parent.width
                color: Kirigami.Theme.textColor
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                level: 2
            }
        }
    }
    // plasma dark
    RowLayout {
        ColumnLayout {
            Layout.preferredWidth: mainLayout.width/2
            Layout.alignment: Qt.AlignBottom

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

        ColumnLayout {
            Layout.preferredWidth: mainLayout.width/2
            Layout.alignment: Qt.AlignTop

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
    // pywal dark
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
        Layout.preferredWidth: mainLayout.width
        height: 1
        color: dividerColor
        opacity: dividerOpacity
    }

    PlasmaExtras.Heading {
        level: 1
        text: "Color amount"
        Layout.alignment: Qt.AlignHCenter
    }

    // Dark blend
    RowLayout {
        width: parent.width
        Layout.fillWidth: true
        Label {
            text: "Dark blend"
            Layout.alignment: Qt.AlignLeft
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


    Component.onCompleted: {
        readMaterialYouData.exec()
        statupTimer.start()

    }

    Timer {
        interval: 1000;
        running: plasmoidExpanded
        repeat: true;
        onTriggered: {
            readMaterialYouData.exec()
            //console.log("Main H:",mainLayout.height," View H:",root.height);
        }
    }

    Timer {
        id: statupTimer
        interval: 500
        repeat: false

        onTriggered: {
            console.log("@@@@@ Config file:", settings.fileName);
            console.log("@@@@@ Settings @@@@@");
            var propertyNames = Object.keys(settings);
            for (var i = 0; i < propertyNames.length; i++) {
                var propertyName = propertyNames[i];
                var propertyValue = settings[propertyName];
                //var propertyValueType = Object.prototype.toString.call(propertyValue)
                var blacklist = ["Changed","objectName","sync","value","setValue"]
                var containsBlacklisted = blacklist.some(function(blacklist){
                    return propertyName.indexOf(blacklist) !== -1
                })
                if (!containsBlacklisted) /*|| propertyValue.indexOf()===-1)*/ {
                    console.log(" ",propertyName + ": " + propertyValue);
                }
            }

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
