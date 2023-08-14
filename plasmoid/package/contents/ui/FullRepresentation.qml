import Qt.labs.platform 1.1
import Qt.labs.settings 1.0
import QtGraphicalEffects 1.12

import QtQuick 2.0
import QtQuick.Dialogs 1.3
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.0

import "components" as Components
import org.kde.kirigami 2.20 as Kirigami
import org.kde.kquickcontrols 2.0
import org.kde.plasma.components 3.0 as PlasmaComponents3
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.plasma.extras 2.0 as PlasmaExtras
import org.kde.plasma.plasmoid 2.0

ColumnLayout {
    id: root
    Layout.minimumWidth: PlasmaCore.Units.gridUnit * 19
    Layout.minimumHeight: PlasmaCore.Units.gridUnit * 19
    Layout.preferredWidth: rootRep.width
    Layout.preferredHeight: rootRep.height

    property bool autoHide: true
    property bool backendRunning: true
    property string homeDir: StandardPaths.writableLocation(
                            StandardPaths.HomeLocation).toString().substring(7)

    property string execName: 'kde-material-you-colors'
    property string execPath: ""
    property string checkBackendCommand: 'ps -C '+execName+' -F --no-headers'
    property string startBackendCommand: execPath
    property string autoStartBackendCommand: execPath + ' --autostart;' + execPath

    property bool onDesktop: plasmoid.location === PlasmaCore.Types.Floating
    property bool plasmoidExpanded: plasmoid.expanded
    property bool autoReloadEnabled: onDesktop || plasmoidExpanded

    // used to trigger reload from parent if true
    property bool doSettingsReload

    // used to trigger a reload if the config file has changed
    property string configPath: homeDir + "/.config/kde-material-you-colors/config.conf"
    property string customConfigPath
    property string checkConfigChangeCommand: "sha1sum " + configPath+" 2> /dev/null"
    property string configSha1

    property bool showAdvanced: false

    // Get a list of installed icon themes as id,name
    // - discard hidden themes
    // - discard cursor themes
    // Non escaped version: find /usr/share/icons ~/.local/share/icons -maxdepth 2 -type f -path '*/icons/*/index.theme' ! -path '*/share/icons' ! -exec grep -q '^Hidden=true' {} \; ! -execdir test -d cursors \; -printf '%p\n' | while read line; do echo "$(basename $(dirname $line)),$(grep '^Name=' $line | sed 's/^Name=//')"; done
    property string getIconThemesCommand: "find /usr/share/icons " +homeDir+"/.local/share/icons -maxdepth 2 -type f -path '*/icons/*/index.theme' ! -path '*/share/icons' ! -exec grep -q '^Hidden=true' {} \\; ! -execdir test -d cursors \\; -printf '%p\\n' | while read line; do echo \"$(basename $(dirname $line)),$(grep '^Name=' $line | sed 's/^Name=//;s/-/ /')\"; done | sort --field-separator=, --key=2n -k2,2"

    ListModel {
        id: iconThemeList
    }

    onPlasmoidExpandedChanged: {
        checkConfigChange.exec(checkConfigChangeCommand)
    }

    onConfigSha1Changed: {
        if (autoReloadEnabled) {
            console.log("@@@@@ RELOADING ID:", plasmoid.id)
            doSettingsReload = true
            doSettingsReload = false
        }
    }

    function findExecutablePath() {
        if (customConfigPath != "") {
            execPath = StandardPaths.findExecutable(customConfigPath).toString().substring(7)
            return
        }
        execPath = StandardPaths.findExecutable(execName).toString().substring(7)
        if (execPath == "") {
            execPath = StandardPaths.findExecutable(execName,
                        homeDir+"/.local/bin").toString().substring(7)
        }
    }
    Component.onCompleted: {
        findExecutablePath()
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
            // console.log("CHECK BACLEND");
            // console.log("cmd:",cmd);
            // console.log("exitCode:",exitCode);
            // console.log("stdout:",stdout);
            // console.log("stderr:",stderr);
            backendRunning = stdout.replace('\n', '').trim().length>0
        }
    }

    PlasmaCore.DataSource {
        id: checkConfigChange
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
            //console.log("checking if config changed",checkConfigChangeCommand);
            checkConfigChange.connectSource(cmd)
        }

        signal exited(string cmd, int exitCode, int exitStatus, string stdout, string stderr)
    }


    Connections {
        target: checkConfigChange
        function onExited(cmd, exitCode, exitStatus, stdout, stderr) {
            var out = stdout.replace('\n', '').trim()
            //console.log("COMMAND:",cmd);
            //console.log("OUTS:",exitCode,exitStatus);
            //console.log("CONFIG SHA1:",out);
            if (out != "") {
                configSha1 = out.split(" ")[0]
            }
        }
    }

    PlasmaCore.DataSource {
        id: getIconThemes
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
            getIconThemes.connectSource(getIconThemesCommand)
        }

        signal exited(string cmd, int exitCode, int exitStatus, string stdout, string stderr)
    }


    Connections {
        target: getIconThemes
        function onExited(cmd, exitCode, exitStatus, stdout, stderr) {
            iconThemeList.clear()
            var lines = stdout.trim().split("\n")
            for (let i=0; i<lines.length; i++) {
                var line = lines[i].toString().split(",")
                // discard lines that are not actual themes e.g default,
                if (line.length === 2 && line[1] !== '') {
                    iconThemeList.append({"name":line[0], "label":line[1]})
                }
            }
        }
    }

    PlasmaExtras.Representation {
        collapseMarginsHint: true
        id: rootRep

        Layout.fillWidth: true
        Layout.fillHeight: true

        header: PlasmaExtras.PlasmoidHeading {
            id:heading
            visible: !(plasmoid.containmentDisplayHints & PlasmaCore.Types.ContainmentDrawsPlasmoidHeading)

            leftPadding: PlasmaCore.Units.smallSpacing

            RowLayout {
                anchors.fill: parent

                PlasmaExtras.Heading {
                    Layout.fillWidth: true
                    level: 1
                    text: Plasmoid.metaData.name
                }

                PlasmaComponents3.ToolButton {
                    display: PlasmaComponents3.AbstractButton.IconOnly
                    icon.name: 'view-refresh'
                    text: Plasmoid.action("reloadConfig").text

                    onClicked: {
                        reloadConfig()
                    }

                    PlasmaComponents3.ToolTip {
                        text: parent.text
                    }
                }

                PlasmaComponents3.ToolButton {
                    display: PlasmaComponents3.AbstractButton.IconOnly
                    icon.name: 'configure'
                    text: Plasmoid.action("configure").text

                    onClicked: {
                        plasmoid.action("configure").trigger()
                    }

                    PlasmaComponents3.ToolTip {
                        text: parent.text
                    }
                }

                PlasmaComponents3.ToolButton {
                    display: PlasmaComponents3.AbstractButton.IconOnly

                    // hide keep open on the desktop
                    visible: !onDesktop

                    icon.name: 'pin'

                    text: i18n("Keep Open")

                    checked: !autoHide

                    onClicked: {
                        autoHide = !autoHide
                        plasmoid.hideOnWindowDeactivate = autoHide
                    }

                    PlasmaComponents3.ToolTip {
                        text: parent.text
                    }
                }
            }
        }

        ColumnLayout {
            id: rootContent
            anchors.fill: parent

            PlasmaComponents3.ScrollView {
                id: scrollView
                Layout.fillHeight: true
                Layout.fillWidth: true

                topPadding: PlasmaCore.Units.smallSpacing
                bottomPadding: PlasmaCore.Units.smallSpacing

                PlasmaComponents3.ScrollBar.horizontal.policy: PlasmaComponents3.ScrollBar.AlwaysOff
                PlasmaComponents3.ScrollBar.vertical.policy: PlasmaComponents3.ScrollBar.AsNeeded

                contentWidth: availableWidth - contentItem.leftMargin - contentItem.rightMargin

                // scroll ScrollView to the bottom
                // https://stackoverflow.com/a/64449107
                // scroll ScrollView to the bottom
                function scrollToBottom() {
                    ScrollBar.vertical.position = 1.0 - ScrollBar.vertical.size
                }

                function scrollToTop() {
                    ScrollBar.vertical.position = 0
                }

                contentItem: ListView {
                    id: listView
                    // reserve space for the scrollbar
                    property var sideMargin: PlasmaCore.Units.smallSpacing +
                                            scrollView.ScrollBar.vertical.width

                    leftMargin: sideMargin - (scrollView.ScrollBar.vertical.visible ?
                                            scrollView.ScrollBar.vertical.width : 0)
                    rightMargin: sideMargin
                    boundsBehavior: Flickable.StopAtBounds
                    clip: true
                    model: 1
                    // width: rootContent.width

                    delegate: ColumnLayout {
                        // Inherit theme from parent, without this colors don't change on light/dark switch
                        Kirigami.Theme.inherit: true
                        id: mainLayout
                        anchors.left: parent.left
                        anchors.right: parent.right

                        property var dividerColor: Kirigami.Theme.textColor
                        property var dividerOpacity: 0.1
                        property var controlHeight: 36 * PlasmaCore.Units.devicePixelRatio
                        property var controlWidth: 48 * PlasmaCore.Units.devicePixelRatio
                        property var textAreaPadding: 10 * PlasmaCore.Units.devicePixelRatio

                        property var materialYouData: null
                        property var materialYouDataString: null

                        property string doSettingsReload: root.doSettingsReload
                        property bool showAdvanced: root.showAdvanced

                        onDoSettingsReloadChanged: {
                            if (doSettingsReload) {
                                destroySettings();
                                createSettings();
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

                        Component.onCompleted: {
                            createSettings()
                            checkBackend.exec(checkBackendCommand)
                            console.log("@@@@@ BACKEND RUNNING:", backendRunning)
                            readMaterialYouData.exec()
                            getIconThemes.exec()
                            statupTimer.start()
                        }

                        Timer {
                            interval: 1000;
                            running: autoReloadEnabled
                            repeat: true;
                            onTriggered: {
                                checkBackend.exec(checkBackendCommand)
                                checkConfigChange.exec(checkConfigChangeCommand)
                                readMaterialYouData.exec()
                            }
                        }

                        // read settings file
                        // save relevant configs with _last suffix to recover them after reenable
                        property var settings: null

                        function createSettings() {
                            var settingsString = 'import Qt.labs.settings 1.0; \
                                Settings { \
                                    category: "CUSTOM"; \
                                    property int monitor: 0; \
                                    property string color; \
                                    property string color_last; \
                                    property string custom_colors_list; \
                                    property string custom_colors_list_last; \
                                    property bool light: false; \
                                    property int ncolor: 0; \
                                    property bool pywal:false; \
                                    property bool pywal_light: false; \
                                    property real light_blend_multiplier: 1.0; \
                                    property real dark_blend_multiplier: 1.0; \
                                    property real light_saturation_multiplier: 1.0; \
                                    property real dark_saturation_multiplier: 1.0; \
                                    property real light_brightness_multiplier: 1.0; \
                                    property real dark_brightness_multiplier: 1.0; \
                                    property bool plasma_follows_scheme: true; \
                                    property bool pywal_follows_scheme: true; \
                                    property string konsole_profile; \
                                    property int konsole_opacity: 100; \
                                    property string iconslight; \
                                    property string iconsdark; \
                                    property int titlebar_opacity: 100; \
                                    property int toolbar_opacity: 100; \
                                    property bool sierra_breeze_buttons_color: false; \
                                    property bool klassy_windeco_outline: false; \
                                    property string darker_window_list; \
                                    property string on_change_hook; \
                                    property string gui_custom_exec_location; \
                                    property bool use_startup_delay: false; \
                                    property int startup_delay: 0; \
                                }';

                            settings = Qt.createQmlObject(settingsString, mainLayout, "settingsObject");
                            settings.fileName = StandardPaths.writableLocation(
                                        StandardPaths.HomeLocation).toString().substring(7) +
                                        "/.config/kde-material-you-colors/config.conf"
                            customTextColorsCheck.checked = settings.custom_colors_list == ""
                            customColorCheck.checked = settings.color == ""
                            root.customConfigPath = settings.gui_custom_exec_location

                        }

                        function destroySettings() {
                            settings.destroy()
                            // settings = null
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
                                try {
                                    materialYouData = JSON.parse(stdout)
                                } catch(error) {
                                    if (error instanceof SyntaxError) {
                                        console.log("@@@@@ Error parsing JSON data:", error.message);
                                    } else {
                                        throw error;
                                    }
                                }
                            }
                        }

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
                                        findExecutablePath()
                                        checkBackend.exec(startBackendCommand)
                                    }
                                },
                                Kirigami.Action {
                                    icon.name: "media-playback-start"
                                    text: "Start && enable Autostart"
                                    onTriggered: {
                                        findExecutablePath()
                                        checkBackend.exec(startBackendCommand)
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
                            level: 3
                            // visible: execPath == ""
                            Layout.preferredWidth: mainLayout.width
                            text: "Backend not found in system PATH or ~/.local/bin. If installed somewhere else, enter the location in advanced settings"
                            Layout.alignment: Qt.AlignHCenter
                            color: Kirigami.Theme.neutralTextColor
                            wrapMode: Text.WordWrap
                            horizontalAlignment: Text.AlignHCenter
                            visible: root.execPath == ""
                        }

                        PlasmaComponents3.ToolButton {
                            Layout.alignment: Qt.AlignHCenter
                            text: root.showAdvanced?"Hide advanced settings":"Show advanced settings"
                            icon.name: 'configure'
                            visible: root.execPath == ""
                            checked: root.showAdvanced
                            onClicked: {
                                root.showAdvanced = !root.showAdvanced
                            }
                        }

                        // NORMAL SETTINGS
                        ColumnLayout {
                            visible: !root.showAdvanced
                            Layout.preferredWidth: mainLayout.width
                            spacing: PlasmaCore.Units.smallSpacing

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
                                    id: customColorCheck
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
                                    topPadding: textAreaPadding
                                    bottomPadding: textAreaPadding
                                    leftPadding: textAreaPadding
                                    rightPadding: textAreaPadding
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
                                    id: customTextColorsCheck

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
                                    topPadding: textAreaPadding
                                    bottomPadding: textAreaPadding
                                    leftPadding: textAreaPadding
                                    rightPadding: textAreaPadding
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
                                    topPadding: textAreaPadding
                                    bottomPadding: textAreaPadding
                                    leftPadding: textAreaPadding
                                    rightPadding: textAreaPadding
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

                            PlasmaComponents3.ToolButton {
                                Layout.alignment: Qt.AlignHCenter
                                text: root.showAdvanced?"Hide advanced settings":"Show advanced settings"
                                icon.name: 'configure'
                                checked: root.showAdvanced
                                onClicked: {
                                    root.showAdvanced = !root.showAdvanced
                                }
                            }
                        }

                        // ADVANCED SECTION
                        ColumnLayout {
                            id: advancedSection
                            visible: root.showAdvanced
                            // spacing: PlasmaCore.Units.smallSpacing

                            onVisibleChanged: {
                                if (visible) {
                                    scrollTimer.start()
                                }
                            }

                            // Custom backend location
                            PlasmaExtras.Heading {
                                level: 1
                                text: "Backend executable location"
                                Layout.alignment: Qt.AlignHCenter
                            }

                            RowLayout {
                                TextField {
                                    placeholderText: qsTr("Executable location e.g /tmp/testenv/bin/kde-material-you-colors")
                                    topPadding: textAreaPadding
                                    bottomPadding: textAreaPadding
                                    leftPadding: textAreaPadding
                                    rightPadding: textAreaPadding
                                    Layout.fillWidth: true
                                    text: settings.gui_custom_exec_location
                                    onAccepted: {
                                        settings.gui_custom_exec_location = text
                                        root.customConfigPath = text
                                        findExecutablePath()
                                    }
                                }
                                Button {
                                    icon.name: "document-open"
                                    onClicked: {
                                        fileDialogHookExec.open()
                                    }
                                }
                            }

                            Rectangle {
                                Layout.preferredWidth: mainLayout.width
                                height: 1
                                color: dividerColor
                                opacity: dividerOpacity
                            }

                            // Konsole
                            PlasmaExtras.Heading {
                                level: 1
                                text: "Konsole"
                                Layout.alignment: Qt.AlignHCenter
                            }

                            RowLayout {
                                Label {
                                    text: "Profile"
                                    Layout.alignment: Qt.AlignLeft
                                }

                                TextField {
                                    placeholderText: qsTr("Konsole profile name e.g Profile 1")
                                    topPadding: textAreaPadding
                                    bottomPadding: textAreaPadding
                                    leftPadding: textAreaPadding
                                    rightPadding: textAreaPadding
                                    Layout.fillWidth: true
                                    text: settings.konsole_profile

                                    onAccepted: {
                                        settings.konsole_profile = text
                                    }
                                }
                            }

                            RowLayout {
                                Label {
                                    text: "Opacity"
                                    Layout.alignment: Qt.AlignLeft
                                }

                                Slider {
                                    value: settings.konsole_opacity
                                    from: 0
                                    to: 100
                                    stepSize: 5
                                    Layout.fillWidth: true
                                    onValueChanged: {
                                        settings.konsole_opacity = Math.round(value * 10) / 10
                                    }
                                }

                                SpinBox {
                                    Layout.preferredWidth: controlWidth*1.3
                                    leftPadding: textAreaPadding
                                    from: 0
                                    to: 100
                                    value: settings.konsole_opacity
                                    onValueModified: {
                                        settings.konsole_opacity = value
                                    }
                                }
                            }

                            Rectangle {
                                Layout.preferredWidth: mainLayout.width
                                height: 1
                                color: dividerColor
                                opacity: dividerOpacity
                            }

                            // Icon themes
                            PlasmaExtras.Heading {
                                level: 1
                                text: "Icon theme"
                                Layout.alignment: Qt.AlignHCenter
                            }

                            RowLayout {
                                Label {
                                    text: "Dark"
                                    Layout.alignment: Qt.AlignLeft
                                }

                                ComboBox {
                                    id:iconThemeDarkCombo
                                    model: iconThemeList
                                    textRole: "label"
                                    Layout.fillWidth: true
                                    valueRole: "name"
                                    currentIndex:0
                                    popup.height: 300 * PlasmaCore.Units.devicePixelRatio

                                    onCurrentIndexChanged: {
                                        settings.iconsdark = model.get(currentIndex)["name"]
                                    }

                                    // Prevent starting scrolling on collapsed combobox
                                    MouseArea {
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        onWheel: {}
                                        onClicked: parent.popup.open()
                                    }
                                }
                            }

                            RowLayout {
                                Label {
                                    text: "Light"
                                    Layout.alignment: Qt.AlignLeft
                                }

                                ComboBox {
                                    id:iconThemeLightCombo
                                    model: iconThemeList
                                    textRole: "label"
                                    Layout.fillWidth: true
                                    valueRole: "name"
                                    currentIndex:0
                                    popup.height: 300 * PlasmaCore.Units.devicePixelRatio

                                    onCurrentIndexChanged: {
                                        settings.iconslight = model.get(currentIndex)["name"]
                                    }

                                    // Prevent starting scrolling on collapsed combobox
                                    MouseArea {
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        onWheel: {}
                                        onClicked: parent.popup.open()
                                    }
                                }
                            }

                            Rectangle {
                                Layout.preferredWidth: mainLayout.width
                                height: 1
                                color: dividerColor
                                opacity: dividerOpacity
                            }

                            // DECO QT THEME
                            PlasmaExtras.Heading {
                                level: 1
                                text: "Titlebar, Toolbar & Window Decorations"
                                Layout.alignment: Qt.AlignHCenter
                            }


                            // Opacity
                            RowLayout {
                                Label {
                                    text: "Titlebar opacity"
                                    Layout.alignment: Qt.AlignLeft
                                }

                                Slider {
                                    value: settings.titlebar_opacity
                                    from: 0
                                    to: 100
                                    stepSize: 5
                                    Layout.fillWidth: true
                                    onValueChanged: {
                                        settings.titlebar_opacity = Math.round(value * 10) / 10
                                    }
                                }

                                SpinBox {
                                    Layout.preferredWidth: controlWidth*1.3
                                    leftPadding: textAreaPadding
                                    from: 0
                                    to: 100
                                    value: settings.titlebar_opacity
                                    onValueModified: {
                                        settings.titlebar_opacity = value
                                    }
                                }
                            }

                            Text {
                                text: "Requires Klassy or Sierra Breeze Enhanced window decoration"
                                Layout.alignment: Qt.AlignHCenter
                                // Layout.fillWidth: true
                                Layout.preferredWidth: mainLayout.width
                                opacity: 0.7
                                color: Kirigami.Theme.textColor
                                wrapMode: Text.WordWrap
                                horizontalAlignment: Text.AlignHCenter
                            }

                            RowLayout {
                                Label {
                                    text: "Toolbar opacity"
                                    Layout.alignment: Qt.AlignLeft
                                }

                                Slider {
                                    value: settings.toolbar_opacity
                                    from: 0
                                    to: 100
                                    stepSize: 5
                                    Layout.fillWidth: true
                                    onValueChanged: {
                                        settings.toolbar_opacity = Math.round(value * 10) / 10
                                    }
                                }

                                SpinBox {
                                    Layout.preferredWidth: controlWidth*1.3
                                    leftPadding: textAreaPadding
                                    from: 0
                                    to: 100
                                    value: settings.toolbar_opacity
                                    onValueModified: {
                                        settings.toolbar_opacity = value
                                    }
                                }
                            }

                            Text {
                                text: "Requires Lightly Application Style"
                                Layout.alignment: Qt.AlignHCenter
                                // Layout.fillWidth: true
                                Layout.preferredWidth: mainLayout.width
                                opacity: 0.7
                                color: Kirigami.Theme.textColor
                                wrapMode: Text.WordWrap
                                horizontalAlignment: Text.AlignHCenter
                            }

                            RowLayout {
                                Layout.topMargin: PlasmaCore.Units.mediumSpacing
                                Label {
                                    text: "Tint Sierra Breeze window decoration buttons"
                                    Layout.alignment: Qt.AlignLeft
                                }

                                CheckBox {
                                    id: enableSbeColor
                                    checked: settings.sierra_breeze_buttons_color

                                    onCheckedChanged: {
                                        settings.sierra_breeze_buttons_color = checked
                                    }
                                }
                            }

                            // klassy outline color
                            RowLayout {
                                Layout.topMargin: PlasmaCore.Units.mediumSpacing
                                Label {
                                    text: "Tint Klassy window decoration outline"
                                    Layout.alignment: Qt.AlignLeft
                                }

                                CheckBox {
                                    id: enableKlassyOutlineColor
                                    checked: settings.klassy_windeco_outline

                                    onCheckedChanged: {
                                        settings.klassy_windeco_outline = checked
                                    }
                                }
                            }

                            Text {
                                text: "Match Titlebar and Window color for these themed windows (space separated)"
                                Layout.alignment: Qt.AlignLeft
                                Layout.preferredWidth: mainLayout.width
                                color: Kirigami.Theme.textColor
                                wrapMode: Text.WordWrap
                                Layout.topMargin: PlasmaCore.Units.mediumSpacing
                            }

                            TextField {
                                placeholderText: qsTr("Window class names e.g konsole alacritty kitty")
                                topPadding: textAreaPadding
                                bottomPadding: textAreaPadding
                                leftPadding: textAreaPadding
                                rightPadding: textAreaPadding
                                Layout.fillWidth: true
                                text: settings.darker_window_list

                                onAccepted: {
                                    settings.darker_window_list = text
                                }
                            }


                            Rectangle {
                                Layout.preferredWidth: mainLayout.width
                                height: 1
                                color: dividerColor
                                opacity: dividerOpacity
                            }

                            PlasmaExtras.Heading {
                                level: 1
                                text: "Custom script"
                                Layout.alignment: Qt.AlignHCenter
                            }

                            Text {
                                text: "Script to be executed on start or wallpaper/dark/light/settings change"
                                Layout.alignment: Qt.AlignLeft
                                Layout.preferredWidth: mainLayout.width
                                color: Kirigami.Theme.textColor
                                wrapMode: Text.WordWrap
                            }

                            RowLayout {
                                TextField {
                                    placeholderText: qsTr("Executable location e.g /home/luis/.local/bin/conky-colors.sh")
                                    topPadding: textAreaPadding
                                    bottomPadding: textAreaPadding
                                    leftPadding: textAreaPadding
                                    rightPadding: textAreaPadding
                                    Layout.fillWidth: true
                                    text: settings.on_change_hook
                                    onAccepted: {
                                        settings.on_change_hook = text
                                    }
                                }
                                Button {
                                    icon.name: "document-open"
                                    onClicked: {
                                        fileDialogHookExec.open()
                                    }
                                }
                            }

                            Rectangle {
                                Layout.preferredWidth: mainLayout.width
                                height: 1
                                color: dividerColor
                                opacity: dividerOpacity
                            }

                            PlasmaExtras.Heading {
                                level: 1
                                text: "Delay on boot"
                                Layout.alignment: Qt.AlignHCenter
                            }

                            Text {
                                text: "Startup delay delay before doing anything, useful for waiting for other utilities that may change themes on boot"
                                Layout.alignment: Qt.AlignLeft
                                Layout.preferredWidth: mainLayout.width
                                color: Kirigami.Theme.textColor
                                wrapMode: Text.WordWrap
                            }

                            RowLayout {
                                Label {
                                    text: "Seconds"
                                    Layout.alignment: Qt.AlignLeft
                                    // Layout.fillWidth: true
                                }

                                TextField {
                                    Layout.preferredWidth: controlWidth
                                    topPadding: textAreaPadding
                                    bottomPadding: textAreaPadding
                                    leftPadding: textAreaPadding
                                    rightPadding: textAreaPadding
                                    placeholderText: "0-?"
                                    horizontalAlignment: TextInput.AlignHCenter
                                    text: parseInt(settings.startup_delay)
                                    // Layout.fillWidth: true
                                    validator: IntValidator {
                                        bottom: 0
                                    }

                                    onAccepted: {
                                        settings.startup_delay = parseInt(text)
                                        // reset color selection
                                        settings.use_startup_delay = settings.startup_delay > 0
                                    }
                                }
                            }


                            // PlasmaComponents3.ToolButton {
                            //     Layout.alignment: Qt.AlignHCenter
                            //     text: root.showAdvanced?"Hide advanced settings":"Show advanced settings"
                            //     icon.name: 'configure'
                            //     checked: root.showAdvanced
                            //     onClicked: {
                            //         root.showAdvanced = !root.showAdvanced
                            //     }
                            // }


                            FileDialog {
                                id: fileDialogHookExec
                                onAccepted: {
                                    mainLayout.settings.on_change_hook = fileDialogHookExec.fileUrl.toString().substring(7)
                                }
                            }

                            FileDialog {
                                id: fileDialogBackendExec
                                onAccepted: {
                                    mainLayout.settings.gui_custom_exec_location = fileDialogBackendExec.fileUrl.toString().substring(7)
                                }
                            }
                        }

                        Timer {
                            id: scrollTimer
                            interval: 20
                            repeat: false
                            onTriggered: {
                                scrollView.scrollToTop()
                            }
                        }

                        Timer {
                            id: statupTimer
                            interval: 500
                            repeat: false

                            onTriggered: {
                                // Default colors
                                if(settings.color_last==="") {
                                    settings.color_last = "#66a3ef"
                                }
                                if (settings.custom_colors_list_last==="") {
                                    settings.custom_colors_list_last = "#d0265c #74e448 #eece4f #66a3ef #532066 #297d81 #ccc1c1"
                                }

                                var index = 0;
                                var darkFound = false
                                var lightFound = false
                                // set currently selected icon theme here now that it has been loaded
                                for (var i = 0; i < iconThemeList.count; i++) {
                                    if (iconThemeList.get(i)["name"]===settings.iconsdark) {
                                        iconThemeDarkCombo.currentIndex = i;
                                        darkFound = true
                                    }

                                    if (iconThemeList.get(i)["name"]===settings.iconslight) {
                                        iconThemeLightCombo.currentIndex = i;
                                        lightFound = true
                                    }
                                    // stop looking if both are found
                                    if (darkFound && lightFound) {
                                        break
                                    }
                                }
                            }
                        }

                        // Components.FadeBehavior on showAdvanced {
                        //     duration: 250
                        // }
                    }
                }
            }

            RowLayout {
                // anchors.fill: parent
                Layout.alignment: Qt.AlignHCenter
                visible: root.showAdvanced
                Layout.bottomMargin: PlasmaCore.Units.smallSpacing
                PlasmaComponents3.ToolButton {
                    // Layout.alignment: Qt.AlignHCenter
                    text: "Hide advanced settings"
                    icon.name: 'configure'
                    checked: root.showAdvanced
                    onClicked: {
                        root.showAdvanced = !root.showAdvanced
                    }
                }
            }
        }

        // footer: PlasmaExtras.PlasmoidHeading {
        //     id:footer

        //     RowLayout {
        //         anchors.fill: parent

        //         PlasmaComponents3.ToolButton {
        //             Layout.alignment: Qt.AlignHCenter
        //             text: "Show advanced settings"
        //             icon.name: 'configure'

        //             checked: root.showAdvanced
        //             onClicked: {
        //                 root.showAdvanced = !root.showAdvanced
        //             }
        //         }
        //     }
        // }
    }
}
