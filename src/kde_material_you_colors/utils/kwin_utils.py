import logging
import subprocess
import time
import re
import dbus
import dbus.lowlevel
from kde_material_you_colors import settings


def reload():
    logging.info("Reloading KWin")

    bus = dbus.SessionBus()
    kwin = dbus.Interface(
        bus.get_object("org.kde.KWin", "/KWin"),
        dbus_interface="org.kde.KWin",
    )
    kwin.reconfigure()


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

        # logging.debug(f"Script loaded id: {command}")

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
        str: Window id (empty if not found)
    """

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
// FIXME: Use callDBus + dbus service instead
console.error("KMYC-desktop-window-id:", desktopWindows[{screen}].id)
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
        # run the script
        bus = dbus.SessionBus()
        kwin = bus.get_object("org.kde.KWin", "/Scripting/Script" + script_id)
        script = dbus.Interface(kwin, "org.kde.kwin.Script")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        script.run()
        time.sleep(0.1)
        try:
            command = [
                "journalctl",
                "--since",
                timestamp,
                "--user",
                "-u",
                "plasma-kwin_wayland.service",
                "-u",
                "plasma-kwin_x11.service",
                "--output",
                "cat",
                "-g",
                "js: KMYC-desktop-window-id",
            ]

            # Execute the command using subprocess.run
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=True,
            )

            # The output is now stored in result.stdout
            output = result.stdout.strip()
            win_id = output.split(" ")[2]
        except subprocess.CalledProcessError as e:
            error = f"Script id {script_id} didn't return a desktop id for screen {screen}: {e}"
            # Replace time to make notify show the error only one time
            cmd = str(e).replace(timestamp, "TIME_NOW")
            logging.exception(error)
            script.stop()
            raise subprocess.CalledProcessError(e.returncode, cmd, e.output, e.stderr)
    except dbus.exceptions.DBusException as e:
        msg = f"Error running script with id {script_id}: {e.get_dbus_message()}"
        logging.exception(msg)
        raise
    else:
        script.stop()

    # logging.debug(f"HANDLE: {win_id}")
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
