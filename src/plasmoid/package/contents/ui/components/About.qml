import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    id: root
    readonly property string ghUser: "luisbocanegra"
    readonly property string projectName: "kde-material-you-colors"
    readonly property string ghProfile: "https://github.com/" + ghUser
    readonly property string ghRepo: ghProfile + "/" + projectName
    readonly property string ghSponsors: `https://github.com/sponsors/${ghUser}`
    readonly property string kofi: "https://ko-fi.com/luisbocanegra"
    readonly property string paypal: "https://www.paypal.com/donate/?hosted_button_id=68SF5ZPAZ46UN"
    readonly property string patreon: "https://www.patreon.com/luisbocanegra"
    readonly property string buymeacoffee: "https://buymeacoffee.com/luisbocanegra"
    readonly property string liberapay: "https://liberapay.com/luisbocanegra"
    readonly property string email: "mailto:luisbocanegra17b@gmail.com"
    readonly property string projects: root.ghProfile + "?tab=repositories&q=&type=source&language=&sort=stargazers"
    readonly property string kdeStore: "https://store.kde.org/p/2136963"

    Menu {
        id: menu

        Action {
            text: i18n("Changelog")
            onTriggered: Qt.openUrlExternally(`${root.ghRepo}/blob/main/CHANGELOG.md`)
            icon.name: "view-calendar-list-symbolic"
        }

        Action {
            text: i18n("Releases")
            onTriggered: Qt.openUrlExternally(`${root.ghRepo}/releases`)
            icon.name: "update-none-symbolic"
        }

        Action {
            text: "Discord"
            icon.source: Qt.resolvedUrl("../../icons/discord.svg")
            onTriggered: Qt.openUrlExternally("https://discord.gg/ZqD75dzKTe")
        }

        Action {
            text: "Matrix"
            icon.name: Qt.resolvedUrl("../../icons/matrix_logo.svg").toString().replace("file://", "")
            onTriggered: Qt.openUrlExternally("https://matrix.to/#/#kde-plasma-panel-colorizer:matrix.org")
        }

        MenuSeparator {}

        Menu {
            title: i18n("Home page")
            icon.name: "globe"

            Action {
                text: "GitHub"
                onTriggered: Qt.openUrlExternally(root.ghRepo)
            }

            Action {
                text: i18n("KDE Store")
                onTriggered: Qt.openUrlExternally(root.kdeStore)
            }
        }

        Menu {
            title: i18n("Issues")
            icon.source: Qt.resolvedUrl("../../icons/github.svg")

            Action {
                text: i18n("Current issues")
                onTriggered: Qt.openUrlExternally(`${root.ghRepo}/issues?q=sort%3Aupdated-desc+is%3Aissue+is%3Aopen`)
            }

            Action {
                text: i18n("Report a bug")
                onTriggered: Qt.openUrlExternally(`${root.ghRepo}/issues/new?assignees=&labels=bug&projects=&template=bug_report.md&title=%5BBug%5D%3A+`)
            }

            Action {
                text: i18n("Request a feature")
                onTriggered: Qt.openUrlExternally(`${root.ghRepo}/issues/new?assignees=&labels=enhancement&projects=&template=feature_request.md&title=%5BFeature+Request%5D%3A+`)
            }
        }

        Menu {
            title: i18n("Help")
            icon.name: "question-symbolic"

            Action {
                text: i18n("FAQ")
                onTriggered: Qt.openUrlExternally(`${root.ghRepo}?tab=readme-ov-file#faq`)
            }

            Action {
                text: i18n("GitHub Discussions")
                onTriggered: Qt.openUrlExternally(`${root.ghRepo}/discussions`)
            }

            Action {
                text: i18n("Send an email")
                onTriggered: Qt.openUrlExternally(root.email)
            }
        }

        MenuSeparator {}

        Menu {
            id: donateMenu
            title: i18n("Donate")
            icon.name: "emblem-favorite-symbolic"

            Instantiator {
                model: [
                    {
                        label: "GitHub Sponsors",
                        url: root.ghSponsors
                    },
                    {
                        label: "Ko-fi",
                        url: root.kofi
                    },
                    {
                        label: "Buy Me A Coffee",
                        url: root.buymeacoffee
                    },
                    {
                        label: "Patreon",
                        url: root.patreon
                    },
                    {
                        label: "PayPal",
                        url: root.paypal
                    },
                    {
                        label: "Liberapay",
                        url: root.liberapay
                    },
                ]
                delegate: MenuItem {
                    required property var modelData
                    text: modelData.label
                    onTriggered: Qt.openUrlExternally(modelData.url)
                }
                onObjectAdded: (index, object) => donateMenu.insertItem(index, object)
            }
        }

        Action {
            text: i18n("More projects")
            onTriggered: Qt.openUrlExternally(`${root.ghProfile}?tab=repositories&type=source`)
            icon.name: "starred"
        }
    }
    ToolButton {
        id: linksButton
        text: "Links"
        icon.name: "application-menu"
        onClicked: {
            if (menu.opened) {
                menu.close();
            } else {
                menu.open();
            }
        }
    }
}
