import os
import logging
import dbus
from .. import settings
from . import color_utils
from . import file_utils
from . import math_utils
from . import notify
from . import kwin_utils


def get_wallpaper_data(monitor=0, file=None, color=None, light=None):
    """Get current wallpaper or color from text file or plugin + containment combo
    and return a string with its type (color or image file)

    Args:
        script (str): javascript to evaluate
        monitor (int): containment (monitor) number

    Returns:
        tuple: (source name (str), type (int), data (str), error (str))
    """

    if monitor and not monitor is None:
        monitor = math_utils.clip(monitor, 0, 999, 0)
    else:
        monitor = 0

    if file:
        # TODO: detect if path is image
        if os.path.exists(file):
            with open(file, encoding="utf-8") as text_file:
                wallpaper = str(text_file.read()).replace("file://", "").strip()
                if wallpaper:
                    return ("file", "image", wallpaper)
        else:
            error = f'File "{file}" does not exist'
            logging.error(error)
            return (f"file:{file}", None, None, error)

    elif color:
        if color_utils.validate_color(color):
            return ("Custom color", "color", color)
        error = f'Error: Color format "{color}" is incorrect'
        logging.error(error)
        return (f"color:{color}", None, None, error)

    else:
        # Get wallpaper data
        script = f"""
        function getConfig(desktop, keys) {{
            for (const key of keys) {{
                const value = desktop.readConfig(key);
                if (value !== "") {{
                    if (key == "Provider") {{
                        return key + "," + value + "," + desktop.readConfig("Category");
                    }}
                    return key + "," + value;
                }}
            }}
        }}
        var desktops = desktops();
        var screen = {monitor}
        if (screen > desktops.length) {{
            screen = 0
        }}
        for (let i=0; i<desktops.length; i++) {{
            if (desktops[i].screen == screen) {{
                desktop = desktops[i];
                break
            }}
        }}
        var plugin = desktop.wallpaperPlugin
        desktop.currentConfigGroup = Array("Wallpaper", plugin, "General");
        const keys = ["Image", "Color","color","Provider"];
        var config = getConfig(desktop, keys);
        print(plugin+","+config);
        """
        # split type and wallpaper data, this allows commas in wallpaper name
        plugin, script_output = evaluate_script(script).split(",", 1)
        script_output = script_output.split(",", 1)

        # special case for picture of the day plugin that requires a
        # directory, provider and sometimes a category
        if plugin == settings.PICTURE_OF_DAY_PLUGIN:
            img_provider = None
            provider_category = None
            # potd output has format Provider,provider_name,provider_category
            if len(script_output) >= 2:
                wallpaper_data = script_output[1].split(",", 1)
                img_provider = wallpaper_data[0]
                # some potd providers also have a category
                if len(wallpaper_data) == 2:
                    provider_category = wallpaper_data[1]

            # no provider means using defaults
            if img_provider:
                potd = settings.PICTURE_OF_DAY_PLUGIN_IMGS_DIR + img_provider
            else:
                # default provider is astronomic picture of the day
                potd = (
                    settings.PICTURE_OF_DAY_PLUGIN_IMGS_DIR
                    + settings.PICTURE_OF_DAY_DEFAULT_PROVIDER
                )

            # unsplash also has a category
            if img_provider == settings.PICTURE_OF_DAY_UNSPLASH_PROVIDER:
                # defaul category doesnt doesnt return id, add it
                if not provider_category:
                    provider_category = (
                        settings.PICTURE_OF_DAY_UNSPLASH_DEFAULT_CATEGORY
                    )
                potd = f"{potd}:{provider_category}"

            # Bing file now has the wallpaper resolution in the name
            if img_provider == settings.PICTURE_OF_DAY_BING_PROVIDER:
                # find and return files that start with bing and don't end with json
                # and use the largest one
                potd = [
                    file
                    for file in os.listdir(settings.PICTURE_OF_DAY_PLUGIN_IMGS_DIR)
                    if os.path.isfile(
                        os.path.join(settings.PICTURE_OF_DAY_PLUGIN_IMGS_DIR, file)
                    )
                    if file.startswith(settings.PICTURE_OF_DAY_BING_PROVIDER)
                    and not file.endswith("json")
                ]
                potd = settings.PICTURE_OF_DAY_PLUGIN_IMGS_DIR + max(potd)

            if os.path.exists(potd):
                return (plugin, "image", potd)

        # Color based wallpapers
        elif script_output[0] in ["color", "Color"] and len(script_output) >= 2:
            color = script_output[1]
            # convert color if needed
            color_fmt = color_utils.validate_color(color)
            if color_fmt:
                try:
                    if color_fmt == 1:
                        color_rgb = tuple(color.split(","))
                        color = color_utils.rgb2hex(
                            r=int(color_rgb[0]),
                            g=int(color_rgb[1]),
                            b=int(color_rgb[2]),
                        )
                    return (plugin, "color", color)
                except Exception as e:
                    error = f"Could not resolve color from {plugin}: {e}"
                    logging.error(error)
                    return (f"plugin:{plugin}", None, None, error)
        else:
            # wallpaper plugin that stores current image
            if script_output[0] in ["Image"] and len(script_output) >= 2:
                wallpaper = script_output[1]
                # if script returns a directory check for mormal/dark variant
                if os.path.isdir(wallpaper):
                    if (
                        os.path.exists(wallpaper + "contents/images_dark")
                        and light is False
                    ):
                        wallpaper = file_utils.get_smallest_image(
                            wallpaper + "contents/images_dark/"
                        )

                    elif os.path.exists(wallpaper + "contents/images"):
                        wallpaper = file_utils.get_smallest_image(
                            wallpaper + "contents/images/"
                        )
                return (plugin, "image", wallpaper)

        # nothing matches
        return (f"plugin:{plugin}", None, None, "Plugin unsupported")


def evaluate_script(script):
    """Make a dbus call to org.kde.PlasmaShell.evaluateScript to get wallpaper data

    Args:
        script (str): js string to evaluate
        monitor (int): containment (monitor) number

    Returns:
        string : wallpaper data (wallpaper path or color)
    """
    try:
        bus = dbus.SessionBus()
        plasma = dbus.Interface(
            bus.get_object("org.kde.plasmashell", "/PlasmaShell"),
            dbus_interface="org.kde.PlasmaShell",
        )
        wallpaper_data = str(plasma.evaluateScript(script)).replace("file://", "")
        return wallpaper_data
    except Exception as e:
        error = f"Error getting wallpaper from dbus:\n{e}"
        logging.error(error)
        notify.send_notification("Error getting wallpaper from dbus:", f"{e}")
    return ""


def get_desktop_screenshot(screen=0):
    # take screenshot of desktop
    window_handle = kwin_utils.get_desktop_window_id(screen)
    if window_handle is not None:
        screenshot_taken = kwin_utils.screenshot_window(
            window_handle, settings.SCREENSHOT_PATH
        )
        if screenshot_taken:
            return ("desktop_screenshot", "image", settings.SCREENSHOT_PATH)

    return (
        f"desktop_screenshot",
        None,
        None,
        " Couldn't take screenshot",
    )
