import logging
import subprocess
import re
import threading
import queue
import dbus
import dbus.lowlevel
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from kde_material_you_colors import settings

DBusGMainLoop(set_as_default=True)


class WindowIdReceiver(dbus.service.Object):
    def __init__(self, bus, loop, result_queue):
        self.loop = loop
        self.bus = bus
        self.result_queue = result_queue
        self._quit = False
        self.bus.request_name(settings.DBUS_NAME, dbus.bus.NAME_FLAG_REPLACE_EXISTING)
        super().__init__(self.bus, "/")

    @dbus.service.method(settings.DBUS_NAME)
    def result(self, text):
        self.result_queue.put(text)
        self.cleanup()

    def cleanup(self):
        if self._quit:
            return
        self.remove_from_connection()

        try:
            dbus_daemon = self.bus.get_object(
                "org.freedesktop.DBus", "/org/freedesktop/DBus"
            )
            dbus_interface = dbus.Interface(dbus_daemon, "org.freedesktop.DBus")
            dbus_interface.ReleaseName(settings.DBUS_NAME)
        except dbus.exceptions.DBusException as e:
            logging.exception(f"Error releasing name: {e.get_dbus_message()}")

        self.loop.quit()
        self._quit = True


def run_dbus_service(result_queue):
    loop = GLib.MainLoop()
    bus = dbus.SessionBus()

    service = WindowIdReceiver(bus, loop, result_queue)
    GLib.timeout_add(2000, service.cleanup)

    logging.debug("D-Bus service waiting for window id")
    loop.run()


def reload():
    if not settings.DESKTOP_IS_KDE:
        return
    logging.info("Reloading KWin")

    try:
        bus = dbus.SessionBus()
        kwin = dbus.Interface(
            bus.get_object("org.kde.KWin", "/KWin"),
            dbus_interface="org.kde.KWin",
        )
        kwin.reconfigure()
    except dbus.DBusException as e:
        msg = e.get_dbus_message() if hasattr(e, "get_dbus_message") else str(e)
        logging.warning(f"Could not call KWin.reconfigure: {msg}")
        return
    except Exception as e:
        logging.exception(f"Unexpected error while reloading KWin: {e}")
        return


def klassy_update_decoration_color_cache():
    logging.info("Updating Klassy decoration color cache")
    path = "/KlassyDecoration"
    interface = "org.kde.Klassy.Style"
    method = "updateDecorationColorCache"
    msg = dbus.lowlevel.SignalMessage(path, interface, method)
    dbus.SessionBus().send_message(msg)


def blend_changes():
    try:
        bus = dbus.SessionBus()
        kwin = dbus.Interface(
            bus.get_object("org.kde.KWin", "/org/kde/KWin/BlendChanges"),
            dbus_interface="org.kde.KWin.BlendChanges",
        )
        kwin.start()
    except Exception as e:
        logging.warning(
            f"Could not start blend effect (requires Plasma 5.25 or later):\n{e}"
        )


def load_desktop_window_id_script():
    # based on https://github.com/jinliu/kdotool/blob/master/src/main.rs 7eebebe
    is_loaded = False
    try:
        bus = dbus.SessionBus()
        kwin = bus.get_object("org.kde.KWin", "/Scripting")
        kwin_iface = dbus.Interface(kwin, dbus_interface="org.kde.kwin.Scripting")
        is_loaded = bool(
            kwin_iface.isScriptLoaded("kde_material_you_get_desktop_view_id")
        )
    except dbus.DBusException as e:
        logging.exception(f"An error occurred with D-Bus: {e.get_dbus_message()}")
        raise
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        raise

    if is_loaded:
        try:
            bus = dbus.SessionBus()
            kwin = bus.get_object("org.kde.KWin", "/Scripting")
            kwin_iface = dbus.Interface(kwin, dbus_interface="org.kde.kwin.Scripting")
            kwin_iface.unloadScript("kde_material_you_get_desktop_view_id")
        except dbus.DBusException as e:
            logging.exception(f"An error occurred with D-Bus: {e.get_dbus_message()}")
            raise
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            raise

    try:
        command = [
            "gdbus",
            "call",
            "--session",
            "--dest",
            "org.kde.KWin",
            "--object-path",
            "/Scripting",
            "--method",
            "org.kde.kwin.Scripting.loadScript",
            settings.KWIN_DESKTOP_ID_JSCRIPT,
            "kde_material_you_get_desktop_view_id",
        ]

        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # keep only the id
        script_id = re.sub(r"\D", "", result.stdout.strip())

        logging.debug(f"Script loaded id: {script_id}")

        if script_id.isdigit():
            return script_id
        else:
            raise ValueError(f"Invalid script ID returned: {script_id}")

    except subprocess.CalledProcessError as e:
        logging.exception(f"An error occurred while loading the script: {e}")
        raise
    except ValueError as e:
        logging.exception(f"An error occurred: {e}")
        raise


def get_desktop_window_id(screen: int = 0) -> str | None:
    # based on https://github.com/jinliu/kdotool/blob/master/src/main.rs 7eebebe
    """_summary_

    Args:
        screen (int): Screen number

    Returns:
        str|none: Window id (None if not found)
    """

    if not settings.DESKTOP_IS_KDE:
        return None

    win_id = None
    script_str = f"""var windows = workspace.windowList()
desktopWindows = []
for (var i = 0; i < windows.length; i++) {{
    let w = windows[i];
    let wClass = w.resourceClass
    let name = w.resourceName
    var id = w.internalId
    isDesktop = w.desktopWindow
    pos = w.pos
    const nameMatches = (name == "plasmashell" && wClass == "plasmashell")
    if(nameMatches && isDesktop) {{
        desktopWindows.push({{ "id": id, "pos": pos }})
    }}
}}
// TODO: Make sure this is reliable for more than two monitors,
// Looks like KWin already returns the windows in a predictable way,
// it seems the list of windows is sorted by the screens positions(?)
// and (at least on my machine) this works for any arrangement
//desktopWindows.sort((b,a) => (a.pos.x - b.pos.x))
callDBus("{settings.DBUS_NAME}", "/", "{settings.DBUS_NAME}", "result", desktopWindows[{screen}].id.toString());
"""
    with open(settings.KWIN_DESKTOP_ID_JSCRIPT, "w", encoding="utf-8") as js:
        js.write(script_str)

    # Load the script
    try:
        script_id = load_desktop_window_id_script()
    except Exception as error:
        logging.error(error)
        raise

    try:
        result_queue: queue.Queue = queue.Queue()
        t = threading.Thread(target=run_dbus_service, args=(result_queue,))
        t.start()

        # run the script
        bus = dbus.SessionBus()
        kwin = bus.get_object("org.kde.KWin", "/Scripting/Script" + script_id)
        script = dbus.Interface(kwin, "org.kde.kwin.Script")
        script.run()
        try:
            win_id = result_queue.get(block=True, timeout=2)
        except queue.Empty:
            win_id = None

        t.join()
        script.stop()
    except dbus.exceptions.DBusException as e:
        msg = f"Error running script with id {script_id}: {e.get_dbus_message()}"
        logging.exception(msg)
        raise

    logging.debug(f"Desktop window id: {win_id}")
    return win_id


def screenshot_window(window_handle, output_file):
    screenshot_taken = False
    result = None
    command = [settings.SCREENSHOT_HELPER_PATH, window_handle, output_file]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        return_code = result.returncode
    except subprocess.CalledProcessError as e:
        error = f"Error taking screenshot for window {window_handle}: {e}"
        logging.exception(error)
        raise subprocess.CalledProcessError(e.returncode, command, e.stdout, e.stderr)

    if result is not None and len(result.stderr) > 0:
        raise subprocess.CalledProcessError(
            result.returncode, command, result.stdout, result.stderr
        )

    screenshot_taken = return_code == 0
    return screenshot_taken


def kde_rounded_corners_reload_effect():
    try:
        bus = dbus.SessionBus()
        kwin = bus.get_object("org.kde.KWin", "/Effects")
        effects_iface = dbus.Interface(kwin, "org.kde.kwin.Effects")
        is_loaded = effects_iface.isEffectLoaded("kwin4_effect_shapecorners")
        if is_loaded:
            effects_iface.reconfigureEffect("kwin4_effect_shapecorners")
    except dbus.exceptions.DBusException as e:
        logging.exception(
            f"Error reloading rounded corners effect: {e.get_dbus_message()}"
        )
    except Exception as e:
        logging.exception(f"Unexpected error reloading rounded corners effect: {e}")
