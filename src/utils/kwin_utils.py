import logging
import subprocess
import dbus


def reload():
    logging.info(f"Reloading KWin...")
    subprocess.Popen("qdbus org.kde.KWin /KWin reconfigure", shell=True,
                     stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


def blend_changes():
    try:
        bus = dbus.SessionBus()
        kwin = dbus.Interface(bus.get_object(
            'org.kde.KWin', '/org/kde/KWin/BlendChanges'), dbus_interface='org.kde.KWin.BlendChanges')
        kwin.start()
    except Exception as e:
        logging.warning(
            f'Could not start blend effect (requires Plasma 5.25 or later):\n{e}')
        return None
