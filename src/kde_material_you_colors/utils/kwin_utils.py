import logging
import subprocess
import dbus
import time
import os
from PIL import Image
from .. import settings


def reload():
    logging.info(f"Reloading KWin")
    subprocess.Popen(
        "qdbus org.kde.KWin /KWin reconfigure",
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )


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
        return None


def load_desktop_window_id_script():
    is_loaded = bool(
        subprocess.check_output(
            "qdbus org.kde.KWin /Scripting org.kde.kwin.Scripting.isScriptLoaded kde_material_you_get_desktop_view_id",
            shell=True,
            universal_newlines=True,
            stderr=subprocess.DEVNULL,
        )
    )

    if is_loaded:
        subprocess.run(
            "qdbus org.kde.KWin /Scripting org.kde.kwin.Scripting.unloadScript kde_material_you_get_desktop_view_id",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    # Calling this overloaded method raises TypeError:
    # Fewer items found in D-Bus signature than in Python arguments
    # So have use subprocess with qdbus instead :(
    script_id = (
        subprocess.check_output(
            [
                "qdbus",
                "org.kde.KWin",
                "/Scripting",
                "loadScript",
                settings.KWIN_DESKTOP_ID_JSCRIPT,
                "kde_material_you_get_desktop_view_id",
            ]
        )
        .decode()
        .strip()
    )
    return script_id


def get_desktop_window_id(screen: int = 0) -> str | None:
    """_summary_

    Args:
        screen (int): Screen number

    Returns:
        str: Window id (empty if not found)
    """

    win_id = None
    script_str = f"""var windows = workspace.clientList()
for (var i = 0; i < windows.length; i++) {{
    let window = windows[i];
    var regex = /Desktop @ QRect\\((.*?)\\) — Plasma/;
    if (window.caption.match(regex) != null && window.screen == {screen}) {{
        print("KMYC-desktop-window-id:", window.internalId)
    }}
}}
"""
    with open(settings.KWIN_DESKTOP_ID_JSCRIPT, "w", encoding="utf-8") as js:
        js.write(script_str)

    # Load the script using qdbus
    script_id = load_desktop_window_id_script()

    # print(script_id)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    subprocess.run(["qdbus", "org.kde.KWin", "/" + script_id, "run"])
    bus = dbus.SessionBus()

    try:
        # run the script
        kwin = bus.get_object("org.kde.KWin", "/" + script_id)
        script = dbus.Interface(kwin, "org.kde.kwin.Script")
        script.run()
        # stop the script
        try:
            output = (
                subprocess.check_output(
                    [
                        "journalctl",
                        "--since",
                        timestamp,
                        "--user",
                        "-u",
                        "plasma-kwin_wayland.service",
                        "--output",
                        "cat",
                        "-g",
                        "js: " + "KMYC-desktop-window-id",
                    ],
                    stderr=subprocess.STDOUT,
                )
                .decode()
                .strip()
            )
            win_id = output.split(" ")[2]
        except subprocess.CalledProcessError as e:
            pass
        script.stop()
    except dbus.exceptions.DBusException as e:
        logging.error(f"Error taking Desktop screenshot for screen {screen}:\n{e}")

    return win_id


def screenshot_window(window_handle, output_file):
    # create a pipe where the screenshot will be written
    read_fd, write_fd = os.pipe()
    results = None
    screenshot_taken = False

    try:
        # Create a connection to the session bus
        bus = dbus.SessionBus()

        # Get a proxy for the KWin object
        kwin = bus.get_object("org.kde.KWin", "/org/kde/KWin/ScreenShot2")
        screenshot = dbus.Interface(kwin, "org.kde.KWin.ScreenShot2")

        options = {
            "include-cursor": False,
            "native-resolution": True,
            "include-shadow": False,
            "include-decoration": False,
        }

        results = screenshot.CaptureWindow(
            window_handle, options, dbus.types.UnixFd(write_fd)
        )

    except dbus.exceptions.DBusException as e:
        logging.error(f"Couldn't take screenshot of desktop: {window_handle}:\n{e}")

    os.close(write_fd)

    if results is not None:
        # Read the screenshot data from the pipe
        screenshot_data = b""
        while True:
            chunk = os.read(read_fd, 1048576)
            if not chunk:
                break
            screenshot_data += chunk

        os.close(read_fd)

        # get image dimensions and format from the results
        img_width = results["width"]
        img_height = results["height"]
        # img_format = results["format"]  # 5

        # image from the raw data
        image = Image.frombytes("RGBA", (img_width, img_height), screenshot_data, "raw")

        # convert from ABGR??? to RGBA
        b, g, r, a = image.split()
        image = Image.merge("RGB", (r, g, b))

        image.save(fp=output_file, compress_level=0)

        screenshot_taken = True

    return screenshot_taken
