import logging
import dbus


def send_notification(heading="", content="", icon=None):
    try:
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
    except dbus.exceptions.DBusException as e:
        logging.warning(f"An error occurred while sending the notification: {e}")
