import os
import logging
import dbus
from .. import settings
from . import color_utils
from . import file_utils
from . import math_utils


def get_wallpaper_data(monitor=0, file=None, color=None, light=None):
    """Get current wallpaper or color from text file or plugin + containment combo
    and return a string with its type (color or image file)

    Args:
        script (str): javascript to evaluate
        monitor (int): containment (monitor) number

    Returns:
        tuple: (type (int), data (str))
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
                    return ("image", wallpaper)
                return None
        else:
            logging.error(f'File "{file}" does not exist')
            return None

    elif color:
        if color_utils.validate_color(color):
            return ("color", color)
        logging.error(f'Error: Color format "{color}" is incorrect')

    else:
        # Get current wallpaper plugin id
        script = """
            var desktops = desktops();
                d = desktops[%s];
                print(d.wallpaperPlugin)
            """
        plugin = evaluate_script(script, monitor)

        # Get wallpaper data
        script = """
        function getConfig(desktop, keys) {
            for (const key of keys) {
                const value = desktop.readConfig(key);
                if (value !== "") {
                    if (key == "Provider") {
                        return key+","+value+","+desktop.readConfig("Category");
                    }
                    return key+","+value
                }
            }
        }
        var desktops = desktops();
        var desktop = desktops[%s];
        var plugin = desktop.wallpaperPlugin
        desktop.currentConfigGroup = Array("Wallpaper", plugin, "General");
        const keys = ["Image", "Color","color","Provider"];
        var config = getConfig(desktop, keys);
        print(config);
        """
        script_output = evaluate_script(script, monitor)
        wallpaper_data = [] if script_output is None else script_output.split(",")

        # special case for picture of the day plugin that requires a
        # directory, provider and sometimes a category
        if plugin == settings.PICTURE_OF_DAY_PLUGIN:
            img_provider = None
            provider_category = None
            if len(wallpaper_data) >= 2:
                img_provider = wallpaper_data[1]
                # some potd providers also have a category
                if len(wallpaper_data) == 3:
                    provider_category = wallpaper_data[2]

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
                return ("image", potd)
            return None
        # Color based wallpapers
        elif wallpaper_data[0] in ["color", "Color"]:
            if len(wallpaper_data) >= 2:
                color = ",".join(wallpaper_data[1:])
                color_fmt = color_utils.validate_color(color)
                # print(color, "fmt:", color_fmt)
                try:
                    if color_fmt == 1:
                        color_rgb = tuple(color.split(","))
                        return (
                            "color",
                            color_utils.rgb2hex(
                                r=int(color_rgb[0]),
                                g=int(color_rgb[1]),
                                b=int(color_rgb[2]),
                            ),
                        )
                    elif color_fmt == 2:
                        return ("color", color)
                except Exception as e:
                    logging.error(f"Could not resolve color from {plugin}: {e}")
                    return None
            else:
                return None
        else:
            # wallpaper plugin that stores current image
            if wallpaper_data and wallpaper_data[0] in ["Image"]:
                if len(wallpaper_data) == 2:
                    # if script returns a directory check for mormal/dark variant
                    wallpaper = wallpaper_data[1]
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
                    return ("image", wallpaper)


def evaluate_script(script, monitor):
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
        wallpaper_data = str(plasma.evaluateScript(script % (monitor,))).replace(
            "file://", ""
        )
        return wallpaper_data
    except Exception as e:
        logging.error(f"Error getting wallpaper from dbus:\n{e}")
        return None
