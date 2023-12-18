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
    id: fullRepresentation
    Layout.minimumWidth: PlasmaCore.Units.gridUnit * 20
    Layout.minimumHeight: PlasmaCore.Units.gridUnit * 19
    Layout.preferredWidth: rootRep.width
    Layout.preferredHeight: rootRep.height

    property bool autoHide: true
    property bool backendRunning: true
    property string homeDir: StandardPaths.writableLocation(
                            StandardPaths.HomeLocation).toString().substring(7)
    property string username: ""

    property string execName: 'kde-material-you-colors'
    property string execPath: ""
    property string checkBackendCommand: 'ps -o user,pid,cmd -C '+execName+' --no-headers | grep -e "'+username+'" | grep -v "<defunct>" | grep -ve "--version" | grep "" | awk \'{print $2}\''
    property string startBackendCommand: execPath
    property string autoStartBackendCommand: execPath + ' --autostart;' + execPath
    property string backendVersionCommand: execPath + ' --version'
    property string backendVersion: ""
    property string backendVersionDisplay: backendVersion !== "" ? backendVersion : "unknown"
    property string recommendedVersion: "1.7.0"
    property string versionStatus: "same"
    property string versionMessage: "You're using a "+versionStatus+" version of the backend (<strong>" + backendVersionDisplay + "</strong>) than this widget version was written for (<strong>"+ recommendedVersion+ "</strong>). Some features may be missing or not work as intended. You can find the latest versions of the widget <a href='https://store.kde.org/p/2073783'>here</a> and the backend <a href='https://github.com/luisbocanegra/kde-material-you-colors'>here</a>."
    property bool showVersionMessage: false

    property bool onDesktop: plasmoid.location === PlasmaCore.Types.Floating
    property bool plasmoidExpanded: plasmoid.expanded
    property bool autoReloadEnabled: onDesktop || plasmoidExpanded

    // used to trigger reload from parent if true
    property bool doSettingsReload

    // used to trigger a reload if the config file has changed
    property string configPath: homeDir + "/.config/kde-material-you-colors/config.conf"
    property string checkConfigChangeCommand: "sha1sum " + configPath+" 2> /dev/null"
    property string configSha1

    property bool showAdvanced: false

    property bool pauseMode: false

    signal savePauseMode()

    property Item parentMain

    Connections {
        target: parentMain
        function onTogglePauseMode() {
            fullRepresentation.pauseMode = !fullRepresentation.pauseMode
            parentMain.pauseModeMain = fullRepresentation.pauseMode
            savePauseMode()
        }
    }

    Connections {
        target: parentMain
        function onUpdatePauseMode() {
            parentMain.pauseModeMain = fullRepresentation.pauseMode
        }
    }


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
        findExecutablePath()
    }

    onConfigSha1Changed: {
        // trigger a reload when config changes to update view
        console.log("@@@@@ RELOADING ID:", plasmoid.id)
        doSettingsReload = true
        doSettingsReload = false
    }

    function findExecutablePath() {
        var temp = ""
        temp = StandardPaths.findExecutable(execName).toString().substring(7)
        if (temp == "") {
            temp = StandardPaths.findExecutable(execName,
                        homeDir+"/.local/bin").toString().substring(7)
        }
        execPath = temp

    }
    function getUsername() {
        var parts = homeDir.split('/');
        if (parts.length > 2 && parts[1] === "home") {
            username = parts[2];
        }
    }

    Component.onCompleted: {
        findExecutablePath()
        getUsername()
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
            // console.log("CHECK BACKEND");
            // console.log("cmd:",cmd);
            // console.log("exitCode:",exitCode);
            // console.log("stdout:",stdout);
            // console.log("stderr:",stderr);
            backendRunning = stdout.replace('\n', '').trim().length>0
        }
    }

    PlasmaCore.DataSource {
        id: checkBackendVersion
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
            checkBackendVersion.connectSource(cmd)
        }

        signal exited(string cmd, int exitCode, int exitStatus, string stdout, string stderr)
    }


    Connections {
        target: checkBackendVersion
        function onExited(cmd, exitCode, exitStatus, stdout, stderr) {
            // console.log("CHECK BACLEND");
            // console.log("cmd:",cmd);
            // console.log("exitCode:",exitCode);
            // console.log("stdout:",stdout);
            // console.log("stderr:",stderr);
            backendVersion = stdout.replace('\n', '').trim()
            versionStatus = compareVersions(backendVersion,recommendedVersion)
        }
    }

    function compareVersions(version1, version2) {
        var v1 = version1.split('-')[0].split('.').map(Number);
        var v2 = version2.split('-')[0].split('.').map(Number);

        for (var i = 0; i < v1.length; ++i) {
            if (v2.length == i) {
                return 'newer';
            }
            if (v1[i] == v2[i]) {
                continue;
            } else if (v1[i] > v2[i]) {
                return 'newer';
            } else {
                return 'older';
            }
        }

        if (version1.includes('-') && !version2.includes('-')) {
            return 'older';
        } else if (!version1.includes('-') && version2.includes('-')) {
            return 'newer';
        } else if (version1.includes('-') && version2.includes('-')) {
            let suffix1 = version1.split('-')[1];
            let suffix2 = version2.split('-')[1];
            if (suffix1 > suffix2) {
                return 'newer';
            } else if (suffix1 < suffix2) {
                return 'older';
            }
        }

        return v1.length != v2.length ? 'older' : 'same';
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
                    visible: !onDesktop
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
                    checkable: false
                    id: pauseBtn
                    icon.name: fullRepresentation.pauseMode ? 'media-playback-start' : 'media-playback-pause'
                    text: fullRepresentation.pauseMode ? 'Resume automatic theming' : 'Pause automatic theming'

                    onClicked: {
                        fullRepresentation.pauseMode = !fullRepresentation.pauseMode
                        savePauseMode()
                    }

                    PlasmaComponents3.ToolTip {
                        text: parent.text
                    }
                }

                PlasmaComponents3.ToolButton {
                    display: PlasmaComponents3.AbstractButton.IconOnly
                    visible: !onDesktop
                    icon.name: 'pin'
                    text: i18n("Keep Open")
                    checked: !autoHide

                    PlasmaComponents3.ToolTip {
                        text: parent.text
                    }

                    onClicked: {
                        autoHide = !autoHide
                        plasmoid.hideOnWindowDeactivate = autoHide
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
                function scrollToBottom() {
                    ScrollBar.vertical.position = 1.0 - ScrollBar.vertical.size
                }

                function scrollToTop() {
                    ScrollBar.vertical.position = 0
                }

                contentItem: ListView {
                    id: listView
                    // reserve space for the scrollbar
                    property var sideMargin: PlasmaCore.Units.mediumSpacing

                    leftMargin: sideMargin
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

                        property string doSettingsReload: fullRepresentation.doSettingsReload
                        property bool showAdvanced: fullRepresentation.showAdvanced
                        property bool pauseMode: fullRepresentation.pauseMode

                        onDoSettingsReloadChanged: {
                            if (doSettingsReload) {
                                destroySettings();
                                createSettings();
                            }
                        }

                        Connections {
                            target: fullRepresentation
                            function onSavePauseMode() {
                                settings.pause_mode = fullRepresentation.pauseMode
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
                            console.log("@@@@@ BACKEND RUNNING:", backendRunning)
                            readMaterialYouData.exec()
                            getIconThemes.exec()
                            statupTimer.start()
                        }

                        Timer {
                            interval: autoReloadEnabled ? 1000 : 2000
                            running: true
                            repeat: true;
                            onTriggered: {
                                checkConfigChange.exec(checkConfigChangeCommand)
                                readMaterialYouData.exec()
                                fullRepresentation.pauseMode = settings.pause_mode
                                parentMain.updatePauseMode()
                            }
                        }

                        Timer {
                            interval: autoReloadEnabled ? 2000 : 5000
                            running: true
                            repeat: true;
                            onTriggered: {
                                checkBackend.exec(checkBackendCommand)
                                findExecutablePath()
                                checkBackendVersion.exec(backendVersionCommand)
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
                                    property bool disable_konsole: false; \
                                    property string iconslight; \
                                    property string iconsdark; \
                                    property int konsole_opacity: 100; \
                                    property int konsole_opacity_dark: 100; \
                                    property int titlebar_opacity: 100; \
                                    property int titlebar_opacity_dark: 100; \
                                    property int toolbar_opacity: 100; \
                                    property int toolbar_opacity_dark: 100; \
                                    property bool sierra_breeze_buttons_color: false; \
                                    property bool klassy_windeco_outline: false; \
                                    property string darker_window_list; \
                                    property string on_change_hook; \
                                    property string gui_custom_exec_location; \
                                    property bool use_startup_delay: false; \
                                    property int startup_delay: 0; \
                                    property int main_loop_delay: 1; \
                                    property int screenshot_delay: 900; \
                                    property bool once_after_change: false; \
                                    property bool pause_mode: false; \
                                }';

                            settings = Qt.createQmlObject(settingsString, mainLayout, "settingsObject");
                            settings.fileName = StandardPaths.writableLocation(
                                        StandardPaths.HomeLocation).toString().substring(7) +
                                        "/.config/kde-material-you-colors/config.conf"
                            customTextColorsCheck.checked = settings.custom_colors_list == ""
                            customColorCheck.checked = settings.color == ""

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
                                    readMaterialYouData.connectSource(
                                        "cat /tmp/kde-material-you-colors-"+username+".json"
                                        )
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
                                        checkBackend.exec(autoStartBackendCommand)
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
                            level: 5
                            // visible: execPath == ""
                            Layout.preferredWidth: mainLayout.width
                            text: "Backend not found in system PATH or ~/.local/bin. If installed somewhere else, make sure to execute outside python environment with -a/-cl argument\ne.g /tmp/testenv/bin/kde-material-you-colors -cl"
                            Layout.alignment: Qt.AlignHCenter
                            color: Kirigami.Theme.neutralTextColor
                            wrapMode: Text.WordWrap
                            horizontalAlignment: Text.AlignHCenter
                            visible: fullRepresentation.execPath == ""
                        }

                        // NORMAL SETTINGS
                        ColumnLayout {
                            visible: !fullRepresentation.showAdvanced
                            Layout.preferredWidth: mainLayout.width
                            spacing: PlasmaCore.Units.smallSpacing

                            RowLayout {
                                Item { Layout.fillWidth: true }
                                // visible: fullRepresentation.versionStatus !== "same"
                                visible: fullRepresentation.showVersionMessage
                                Label {
                                    Layout.fillWidth: true
                                    text: fullRepresentation.versionMessage
                                    onLinkActivated: Qt.openUrlExternally(link)
                                    wrapMode: Text.WordWrap
                                }

                                ToolButton {
                                    icon.name: "dialog-warning"
                                    visible: fullRepresentation.showVersionMessage
                                    opacity: 0.8
                                    Kirigami.Theme.inherit: false
                                    Kirigami.Theme.textColor: Kirigami.Theme.neutralTextColor
                                    Kirigami.Theme.highlightColor: Kirigami.Theme.neutralTextColor

                                    hoverEnabled: true
                                    onClicked: {
                                        fullRepresentation.showVersionMessage = !fullRepresentation.showVersionMessage
                                    }
                                    Layout.alignment: Qt.AlignHRight|Qt.AlignTop

                                    PlasmaComponents3.ToolTip {
                                        x: parent.width / 2
                                        y: parent.height
                                        text: "Tap to hide"
                                    }
                                }
                            }

                            // COLOR SELECTION FROM WALLPAPER OR CUSTOM COLOR
                            RowLayout {
                                Item { Layout.fillWidth: true }
                                PlasmaExtras.Heading {
                                    level: 1
                                    text: "Colors source"
                                    anchors.centerIn: parent
                                }

                                ToolButton { // PlasmaComponents3 one doesnt take colors??
                                    id: versionInfoBtn
                                    icon.name: "dialog-warning"
                                    visible: !fullRepresentation.showVersionMessage &&
                                        fullRepresentation.versionStatus !== "same" &&
                                        fullRepresentation.execPath !== ""
                                    opacity: 0.8
                                    Kirigami.Theme.inherit: false
                                    Kirigami.Theme.textColor: Kirigami.Theme.neutralTextColor
                                    Kirigami.Theme.highlightColor: Kirigami.Theme.neutralTextColor

                                    hoverEnabled: true
                                    onClicked: {
                                        fullRepresentation.showVersionMessage = !fullRepresentation.showVersionMessage
                                    }
                                    PlasmaComponents3.ToolTip {
                                        x: parent.width / 2
                                        y: parent.height
                                        text: "Tap to show"
                                    }
                                }

                            }

                            RowLayout {
                                Label {
                                    text: "From Wallpaper"
                                }

                                CheckBox {
                                    id: customColorCheck
                                    onCheckedChanged: {
                                        settings.color = checked?"":settings.color_last
                                    }
                                }

                                // Monitor number when wallpaper colors is enabled
                                Label {
                                    visible: settings.color==""
                                    text: "on screen"
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

                                PlasmaComponents3.ToolButton {
                                    id: screenInfoBtn
                                    icon.name: "help-hint"
                                    visible: plasmoid.screen !== -1
                                    opacity: 0.7

                                    hoverEnabled: true
                                    onClicked: screenInfoPopup.show()

                                    PlasmaComponents3.ToolTip {
                                        id: screenInfoPopup
                                        x: screenInfoBtn.width / 2
                                        y: screenInfoBtn.height
                                        text: "<strong>Tip:</strong> This widget is on screen " + plasmoid.screen.toString()
                                    }
                                }
                            }



                            // Color selection
                            RowLayout {
                                Layout.preferredWidth: mainLayout.width

                                Label {
                                    text: "Select color"
                                    id:selectColorLabel
                                    Layout.fillWidth: settings.color!==""
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
                            RowLayout {
                                Item { Layout.fillWidth: true }

                                PlasmaExtras.Heading {
                                    id: headingTextColors
                                    level: 1
                                    text: "Text colors"
                                    anchors.centerIn: parent
                                }

                                PlasmaComponents3.ToolButton {
                                    id: textColorsHelpBtn
                                    icon.name: "help-hint"
                                    opacity: 0.7

                                    hoverEnabled: true
                                    onClicked: textColorsHelpPopup.show()
                                    anchors.left: headingTextColors.right

                                    PlasmaComponents3.ToolTip {
                                        id: textColorsHelpPopup
                                        x: textColorsHelpBtn.width / 2
                                        y: textColorsHelpBtn.height
                                        text: "Applies to <strong>Konsole</strong>, <strong>Pywal</strong>, <strong>KSyntaxHighlighting</strong>"
                                    }
                                }
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

                            // PYWAL
                            RowLayout {
                                Label {
                                    text: "Apply to Pywal"
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

                            RowLayout {
                                Label {
                                    text: "Apply to Konsole"
                                    Layout.alignment: Qt.AlignLeft
                                    // Layout.fillWidth: true
                                }

                                CheckBox {
                                    id: enableKonsole
                                    checked: !settings.disable_konsole

                                    onCheckedChanged: {
                                        settings.disable_konsole = !checked
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
                            RowLayout {
                                Item {
                                    Layout.fillWidth: true
                                }
                                PlasmaExtras.Heading {
                                    level: 1
                                    text: "Dark mode"
                                    anchors.centerIn: parent
                                    id: headingDarkMode
                                }

                                PlasmaComponents3.ToolButton {
                                    id: darkModeHelpBtn
                                    icon.name: "help-hint"
                                    opacity: 0.7

                                    hoverEnabled: true
                                    onClicked: darkModeHelpPopup.open()
                                    anchors.left: headingDarkMode.right

                                    PlasmaComponents3.ToolTip {
                                        id: darkModeHelpPopup
                                        x: darkModeHelpBtn.width / 2
                                        y: darkModeHelpBtn.height
                                        text: "<strong>Follow color scheme</strong> applies only for Material You color schemes when changed by you or other programs"
                                    }
                                }
                            }
                            // Headings
                            RowLayout {
                                Layout.preferredWidth: mainLayout.width
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
                                Layout.preferredWidth: mainLayout.width
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
                                text: fullRepresentation.showAdvanced?"Hide advanced settings":"Show advanced settings"
                                icon.name: 'configure'
                                checked: fullRepresentation.showAdvanced
                                onClicked: {
                                    fullRepresentation.showAdvanced = !fullRepresentation.showAdvanced
                                }
                            }
                        }

                        // ADVANCED SECTION
                        ColumnLayout {
                            id: advancedSection
                            visible: fullRepresentation.showAdvanced
                            Layout.preferredWidth: mainLayout.width

                            onVisibleChanged: {
                                if (visible) {
                                    scrollTimer.start()
                                }
                            }

                            // Konsole
                            PlasmaExtras.Heading {
                                level: 1
                                text: "Konsole"
                                Layout.alignment: Qt.AlignHCenter
                            }

                            PlasmaExtras.Heading {
                                level: 4
                                text: "Background opacity"
                                Layout.alignment: Qt.AlignHCenter
                            }

                            RowLayout {

                                Label {
                                    text: "Light"
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

                            RowLayout {
                                Label {
                                    text: "Dark"
                                    Layout.alignment: Qt.AlignLeft
                                }

                                Slider {
                                    value: settings.konsole_opacity_dark
                                    from: 0
                                    to: 100
                                    stepSize: 5
                                    Layout.fillWidth: true
                                    onValueChanged: {
                                        settings.konsole_opacity_dark = Math.round(value * 10) / 10
                                    }
                                }

                                SpinBox {
                                    Layout.preferredWidth: controlWidth*1.3
                                    leftPadding: textAreaPadding
                                    from: 0
                                    to: 100
                                    value: settings.konsole_opacity_dark
                                    onValueModified: {
                                        settings.konsole_opacity_dark = value
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
                                Layout.preferredWidth: parent.width
                                color: Kirigami.Theme.textColor
                                wrapMode: Text.WordWrap
                                horizontalAlignment: Text.AlignHCenter
                            }


                            RowLayout {
                                Layout.alignment: Qt.AlignHCenter
                                PlasmaExtras.Heading {
                                    level: 4
                                    text: "Titlebar opacity"
                                    // Layout.alignment: Qt.AlignHCenter
                                }
                                PlasmaComponents3.ToolButton {
                                    id: titlebarOpacityHelpBtn
                                    icon.name: "help-hint"
                                    opacity: 0.7

                                    hoverEnabled: true
                                    onClicked: titlebarOpacityHelpPopup.open()

                                    PlasmaComponents3.ToolTip {
                                        id: titlebarOpacityHelpPopup
                                        x: titlebarOpacityHelpBtn.width / 2
                                        y: titlebarOpacityHelpBtn.height
                                        text: "Requires <strong>Klassy</strong> or <strong>Sierra Breeze Enhanced</strong> window decoration"
                                    }
                                }
                            }

                            RowLayout {
                                Label {
                                    text: "Light"
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

                            RowLayout {
                                Label {
                                    text: "Dark"
                                    Layout.alignment: Qt.AlignLeft
                                }

                                Slider {
                                    value: settings.titlebar_opacity_dark
                                    from: 0
                                    to: 100
                                    stepSize: 5
                                    Layout.fillWidth: true
                                    onValueChanged: {
                                        settings.titlebar_opacity_dark = Math.round(value * 10) / 10
                                    }
                                }

                                SpinBox {
                                    Layout.preferredWidth: controlWidth*1.3
                                    leftPadding: textAreaPadding
                                    from: 0
                                    to: 100
                                    value: settings.titlebar_opacity_dark
                                    onValueModified: {
                                        settings.titlebar_opacity_dark = value
                                    }
                                }
                            }

                            RowLayout {
                                Layout.alignment: Qt.AlignHCenter
                                PlasmaExtras.Heading {
                                    level: 4
                                    text: "Toolbar opacity"
                                    // Layout.alignment: Qt.AlignHCenter
                                }
                                PlasmaComponents3.ToolButton {
                                    id: toolbarOpacityHelpBtn
                                    icon.name: "help-hint"
                                    opacity: 0.7

                                    hoverEnabled: true
                                    onClicked: toolbarOpacityHelpPopup.open()

                                    PlasmaComponents3.ToolTip {
                                        id: toolbarOpacityHelpPopup
                                        x: toolbarOpacityHelpBtn.width / 2
                                        y: toolbarOpacityHelpBtn.height
                                        text: "Requires <strong>Lightly</strong> Application Style"
                                    }
                                }
                            }

                            RowLayout {
                                Label {
                                    text: "Light"
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

                            RowLayout {
                                Label {
                                    text: "Dark"
                                    Layout.alignment: Qt.AlignLeft
                                }

                                Slider {
                                    value: settings.toolbar_opacity_dark
                                    from: 0
                                    to: 100
                                    stepSize: 5
                                    Layout.fillWidth: true
                                    onValueChanged: {
                                        settings.toolbar_opacity_dark = Math.round(value * 10) / 10
                                    }
                                }

                                SpinBox {
                                    Layout.preferredWidth: controlWidth*1.3
                                    leftPadding: textAreaPadding
                                    from: 0
                                    to: 100
                                    value: settings.toolbar_opacity_dark
                                    onValueModified: {
                                        settings.toolbar_opacity_dark = value
                                    }
                                }
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



                            RowLayout {
                                Label {
                                    text: "Match Titlebar"
                                    Layout.alignment: Qt.AlignLeft
                                    color: Kirigami.Theme.textColor
                                    wrapMode: Text.WordWrap
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
                                PlasmaComponents3.ToolButton {
                                    id: matchTitlebarOpacityHelpBtn
                                    icon.name: "help-contents"

                                    hoverEnabled: true
                                    onClicked: matchTitlebarOpacityHelpPopup.open()

                                    PlasmaComponents3.ToolTip {
                                        id: matchTitlebarOpacityHelpPopup
                                        x: matchTitlebarOpacityHelpBtn.width / 2
                                        y: matchTitlebarOpacityHelpBtn.height
                                        text: "Match Titlebar and Window color for these themed windows (space separated)"
                                    }
                                }
                            }

                            Rectangle {
                                Layout.preferredWidth: mainLayout.width
                                height: 1
                                color: dividerColor
                                opacity: dividerOpacity
                            }

                            RowLayout {
                                Layout.alignment: Qt.AlignHCenter
                                PlasmaExtras.Heading {
                                    level: 1
                                    text: "Run script"
                                    // Layout.alignment: Qt.AlignHCenter
                                }
                                PlasmaComponents3.ToolButton {
                                    id: scriptInfoBtn
                                    icon.name: "help-hint"
                                    opacity: 0.7

                                    hoverEnabled: true
                                    onClicked: scriptInfoPopup.open()

                                    PlasmaComponents3.ToolTip {
                                        id: scriptInfoPopup
                                        x: scriptInfoBtn.width / 2
                                        y: scriptInfoBtn.height
                                        text: "Absolute path of script to be executed on start or wallpaper/dark/light/settings change"
                                    }
                                }
                            }

                            RowLayout {
                                Label {
                                    text: "Script"
                                }
                                TextField {
                                    placeholderText: qsTr("e.g /home/"+username+"/scripts/script.sh")
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
                                text: "Delay options"
                                Layout.alignment: Qt.AlignHCenter
                            }

                            RowLayout{
                                Text {
                                    text: "Startup delay (seconds)"
                                    Layout.alignment: Qt.AlignLeft
                                    // Layout.preferredWidth: mainLayout.width
                                    // Layout.fillWidth: true
                                    color: Kirigami.Theme.textColor
                                    wrapMode: Text.WordWrap
                                }

                                TextField {
                                    Layout.preferredWidth: controlWidth * 1.5
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

                                PlasmaComponents3.ToolButton {
                                    id: startupDelayBtn
                                    icon.name: "help-contents"

                                    hoverEnabled: true
                                    onClicked: startupDelayPopup.open()

                                    PlasmaComponents3.ToolTip {
                                        id: startupDelayPopup
                                        x: startupDelayBtn.width / 2
                                        y: startupDelayBtn.height
                                        text: "Delay before doing anything\nUseful for waiting for other utilities that may change themes on boot (default is 0)"
                                    }
                                }
                            }

                            RowLayout {
                                Text {
                                    text: "Wallpaper detection delay"
                                    Layout.alignment: Qt.AlignLeft
                                    // Layout.preferredWidth: mainLayout.width
                                    // Layout.fillWidth: true
                                    color: Kirigami.Theme.textColor
                                    wrapMode: Text.WordWrap
                                }

                                TextField {
                                    Layout.preferredWidth: controlWidth * 1.5
                                    topPadding: textAreaPadding
                                    bottomPadding: textAreaPadding
                                    leftPadding: textAreaPadding
                                    rightPadding: textAreaPadding
                                    placeholderText: "0-?"
                                    horizontalAlignment: TextInput.AlignHCenter
                                    text: parseInt(settings.main_loop_delay)
                                    // Layout.fillWidth: true
                                    validator: IntValidator {
                                        bottom: 0
                                    }

                                    onAccepted: {
                                        settings.main_loop_delay = parseInt(text)
                                        // reset color selection
                                    }
                                }

                                PlasmaComponents3.ToolButton {
                                    id: mainDelayBtn
                                    icon.name: "help-contents"

                                    hoverEnabled: true
                                    onClicked: mainDelayPopup.open()

                                    PlasmaComponents3.ToolTip {
                                        id: mainDelayPopup
                                        x: mainDelayBtn.width / 2
                                        y: mainDelayBtn.height
                                        text: "Main loop delay (in seconds).\nUseful for decreasing unnecessary detections or save a bit of power (default is 1)"
                                    }
                                }
                            }

                            RowLayout {
                                Text {
                                    text: "Screenshot method delay"
                                    Layout.alignment: Qt.AlignLeft
                                    // Layout.preferredWidth: mainLayout.width
                                    // Layout.fillWidth: true
                                    color: Kirigami.Theme.textColor
                                    wrapMode: Text.WordWrap
                                }

                                TextField {
                                    Layout.preferredWidth: controlWidth * 1.5
                                    topPadding: textAreaPadding
                                    bottomPadding: textAreaPadding
                                    leftPadding: textAreaPadding
                                    rightPadding: textAreaPadding
                                    placeholderText: "0-?"
                                    horizontalAlignment: TextInput.AlignHCenter
                                    text: parseInt(settings.screenshot_delay)
                                    // Layout.fillWidth: true
                                    validator: IntValidator {
                                        bottom: 0
                                    }

                                    onAccepted: {
                                        settings.screenshot_delay = parseInt(text)
                                        // reset color selection
                                    }
                                }

                                PlasmaComponents3.ToolButton {
                                    id: screenshotDelayBtn
                                    icon.name: "help-contents"

                                    hoverEnabled: true
                                    onClicked: screenshotDelayPopup.open()

                                    PlasmaComponents3.ToolTip {
                                        id: screenshotDelayPopup
                                        x: screenshotDelayBtn.width / 2
                                        y: screenshotDelayBtn.height
                                        text: "Delay after taking screenshot (in seconds).\nUseful for live wallpapers that display a constant transition based on time or other circumstances, which would trigger colors generation too often (default is 900)"
                                    }
                                }
                            }

                            RowLayout {
                                Label {
                                    text: "Single screenshot mode"
                                    Layout.alignment: Qt.AlignLeft
                                }

                                CheckBox {
                                    checked: settings.once_after_change

                                    onCheckedChanged: {
                                        settings.once_after_change = checked
                                    }
                                }

                                PlasmaComponents3.ToolButton {
                                    icon.name: "help-contents"

                                    hoverEnabled: true
                                    onClicked: pauseScreenshotDelayPopup.open()

                                    PlasmaComponents3.ToolTip {
                                        id: pauseScreenshotDelayPopup
                                        x: parent.width / 2
                                        y: parent.height
                                        text: "Only extract colors from screenshot after changing wallpaper plugin. This option makes sense for wallpaper plugins that display an animated loop that never stops. Makes the color extraction run only a single time instead of detecting every change."
                                    }
                                }
                            }

                            Rectangle {
                                Layout.topMargin: PlasmaCore.Units.mediumSpacing
                                Layout.preferredWidth: mainLayout.width
                                height: 1
                                color: dividerColor
                                opacity: dividerOpacity
                            }

                            ColumnLayout {
                                spacing: PlasmaCore.Units.mediumSpacing
                                PlasmaExtras.Heading {
                                    level: 1
                                    text: "About " + Plasmoid.metaData.name
                                    Layout.alignment: Qt.AlignHCenter
                                    wrapMode: Text.WordWrap
                                    horizontalAlignment: Text.AlignHCenter
                                }

                                Label {
                                    text: "Plasmoid version: " + Plasmoid.metaData.version
                                    Layout.alignment: Qt.AlignHCenter
                                    onLinkActivated: Qt.openUrlExternally(link)
                                }

                                Label {
                                    text: "Backend version: " + fullRepresentation.backendVersionDisplay
                                    Layout.alignment: Qt.AlignHCenter
                                    onLinkActivated: Qt.openUrlExternally(link)
                                }

                                Label {
                                    text: "If you like the project you can leave a review in <a href='https://store.kde.org/p/2073783'>KDE Store</a> or give it a star on <a href='https://github.com/luisbocanegra/kde-material-you-colors'>Github</a>. For bugs and feature requests please go to the <a href='https://github.com/luisbocanegra/kde-material-you-colors/issues'>issues page</a>."
                                    onLinkActivated: Qt.openUrlExternally(link)
                                    wrapMode: Text.WordWrap
                                    Layout.alignment: Qt.AlignHCenter
                                    Layout.preferredWidth: mainLayout.width
                                    horizontalAlignment: Text.AlignHCenter
                                }
                            }

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
                                // FIXME: for some reason color_last starts with red??
                                if(settings.color_last==="" || settings.color_last ==="red") {
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
                visible: fullRepresentation.showAdvanced
                Layout.bottomMargin: PlasmaCore.Units.smallSpacing
                PlasmaComponents3.ToolButton {
                    // Layout.alignment: Qt.AlignHCenter
                    text: "Hide advanced settings"
                    icon.name: 'configure'
                    checked: fullRepresentation.showAdvanced
                    onClicked: {
                        fullRepresentation.showAdvanced = !fullRepresentation.showAdvanced
                    }
                }
            }
        }
    }
}
