import dbus


def send_notification(heading, content, icon=None):
    bus = dbus.SessionBus()
    notify = dbus.Interface(
        bus.get_object(
            "org.freedesktop.Notifications", "/org/freedesktop/Notifications"
        ),
        "org.freedesktop.Notifications",
    )
    hints = {}

    hints["desktop-entry"] = "kde-material-you-colors"
    notify.Notify(
        "KDE Material You Colors", 0, icon or "", heading, content, [], hints, -1
    )
