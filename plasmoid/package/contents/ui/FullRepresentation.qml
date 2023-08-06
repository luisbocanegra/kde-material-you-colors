import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.0
import org.kde.kirigami 2.20 as Kirigami
import org.kde.kquickcontrols 2.0
import org.kde.plasma.core 2.0 as PlasmaCore
import Qt.labs.platform 1.1
import Qt.labs.settings 1.0
import org.kde.plasma.components 3.0 as PlasmaComponents3
import org.kde.plasma.extras 2.0 as PlasmaExtras
import org.kde.plasma.plasmoid 2.0

ColumnLayout {
    id: root

    property bool autoHide: true
    property bool backendRunning: true
    property string execName: 'kde-material-you-colors'
    property string checkBackendCommand: 'ps -C '+execName+' -F --no-headers'
    property string startBackendCommand: execName
    property string autoStartBackendCommand: execName+' --autostart;' +execName
    property bool onDesktop: plasmoid.location === PlasmaCore.Types.Floating
    property bool plasmoidExpanded: plasmoid.expanded || onDesktop


    Layout.minimumWidth: PlasmaCore.Units.gridUnit * 19
    Layout.minimumHeight: PlasmaCore.Units.gridUnit * 19
    Layout.preferredWidth: rootRep.width
    Layout.preferredHeight: rootRep.height + heading.height

    // used to trigger reload from parent if true
    property bool mainRequiresReload
    property string mainContentSource: "MainWidgetContent.qml"

    onMainRequiresReloadChanged: {
        if (mainRequiresReload === true) {
            var tmp = mainContentSource
            mainContentSource = ""
            mainContentSource = tmp
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

    PlasmaExtras.PlasmoidHeading {
        id:heading
        visible: !(plasmoid.containmentDisplayHints & PlasmaCore.Types.ContainmentDrawsPlasmoidHeading)

        //leftPadding: PlasmaCore.Units.smallSpacing

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


    PlasmaExtras.Representation {
        collapseMarginsHint: true
        id: rootRep

        Layout.fillWidth: true
        Layout.fillHeight: true

        ColumnLayout {
            id: rootContent
            anchors.fill: parent

            PlasmaComponents3.ScrollView {
                id: scrollView
                Layout.fillHeight: true
                Layout.fillWidth: true

                topPadding: PlasmaCore.Units.mediumSpacing

                PlasmaComponents3.ScrollBar.horizontal.policy: PlasmaComponents3.ScrollBar.AlwaysOff
                PlasmaComponents3.ScrollBar.vertical.policy: PlasmaComponents3.ScrollBar.AsNeeded

                contentWidth: availableWidth - contentItem.leftMargin - contentItem.rightMargin

                contentItem: ListView {
                    id: listView
                    leftMargin: PlasmaCore.Units.mediumSpacing
                    rightMargin: PlasmaCore.Units.mediumSpacing
                    boundsBehavior: Flickable.StopAtBounds
                    clip: true
                    model: 1

                    delegate: ColumnLayout {
                        property string mainContentSource: root.mainContentSource
                        // Inherit theme from parent, without this colors don't change on light/dark switch
                        Kirigami.Theme.inherit: true
                        id: mainLayout
                        anchors.left: parent.left
                        anchors.right: parent.right

                        property var dividerColor: Kirigami.Theme.textColor
                        property var dividerOpacity: 0.1

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
                                        checkBackend.exec(startBackendCommand)
                                    }
                                },
                                Kirigami.Action {
                                    icon.name: "media-playback-start"
                                    text: "Start && enable Autostart"
                                    onTriggered: {
                                        checkBackend.exec(startBackendCommandAutostart)
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

                        Component.onCompleted: {
                            checkBackend.exec(checkBackendCommand)
                            console.log("@@@@@ BACKEND RUNNING:", backendRunning)
                        }

                        Timer {
                            interval: 1000;
                            running: plasmoidExpanded
                            repeat: true;
                            onTriggered: {
                                checkBackend.exec(checkBackendCommand)
                                //console.log("Main H:",mainLayout.height," View H:",root.height);
                            }
                        }

                        // Main widget content here
                        Loader {
                            id: loader
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            source: mainContentSource
                        }
                    }
                }
            }
        }
    }
}
