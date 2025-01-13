import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    id: root
    readonly property string ghUser: "luisbocanegra"
    readonly property string projectName: "kde-material-you-colors"
    readonly property string ghRepo: "https://github.com/"+ghUser+"/"+projectName
    readonly property string kofi: "https://ko-fi.com/luisbocanegra"
    readonly property string paypal: "https://www.paypal.com/donate/?hosted_button_id=Y5TMH3Z4YZRDA"
    readonly property string email: "mailto:luisbocanegra17b@gmail.com"
    readonly property string projects: "https://github.com/"+ghUser+"?tab=repositories&q=&type=source&language=&sort=stargazers"
    readonly property string kdeStore: "https://store.kde.org/p/2136963"

    Menu {
        id: menu
        y: linksButton.height
        x: linksButton.x
        Action {
            text: "Changelog"
            onTriggered: Qt.openUrlExternally(ghRepo+"/blob/main/CHANGELOG.md")
            icon.name: "view-calendar-list-symbolic"
        }
        Action {
            text: "Releases"
            onTriggered: Qt.openUrlExternally(ghRepo+"/releases")
            icon.name: "update-none-symbolic"
        }

        MenuSeparator { }

        Menu {
            title: "Project page"
            icon.name: "globe"
            Action {
                text: "GitHub"
                onTriggered: Qt.openUrlExternally(ghRepo)
            }
            Action {
                text: "KDE Store"
                onTriggered: Qt.openUrlExternally(kdeStore)
            }
        }

        Menu {
            title: "Issues"
            icon.name: "project-open-symbolic"
            Action {
                text: "Current issues"
                onTriggered: Qt.openUrlExternally(ghRepo+"/issues?q=sort%3Aupdated-desc+is%3Aissue+is%3Aopen")
            }
            Action {
                text: "Report a bug"
                onTriggered: Qt.openUrlExternally(ghRepo+"/issues/new?assignees=&labels=bug&projects=&template=bug_report.md&title=%5BBug%5D%3A+")
            }
            Action {
                text: "Request a feature"
                onTriggered: Qt.openUrlExternally(ghRepo+"/issues/new?assignees=&labels=enhancement&projects=&template=feature_request.md&title=%5BFeature+Request%5D%3A+")
            }
        }

        Menu {
            title: "Help"
            icon.name: "question-symbolic"
            Action {
                text: "Discussions"
                onTriggered: Qt.openUrlExternally(ghRepo+"/discussions")
            }
            Action {
                text: "Send an email"
                onTriggered: Qt.openUrlExternally(email)
            }
        }

        Menu {
            title: "Donate"
            icon.name: "love"
            Action {
                text: "Ko-fi"
                onTriggered: Qt.openUrlExternally(kofi)
            }
            Action {
                text: "Paypal"
                onTriggered: Qt.openUrlExternally(paypal)
            }
            Action {
                text: "GitHub sponsors"
                onTriggered: Qt.openUrlExternally("https://github.com/sponsors/"+ghUser)
            }
        }

        MenuSeparator { }

        Action {
            text: "More projects"
            onTriggered: Qt.openUrlExternally(projects)
            icon.name: "starred-symbolic"
        }
    }
    ToolButton {
        text: "Links"
        icon.name: "application-menu"
        id: linksButton
        onClicked: {
            if (menu.opened) {
                menu.close()
            } else {
                menu.open()
            }
        }
    }
}
