import dbus
import logging
import os
import globals
from . import color_utils
from . import file_utils


def get_wallpaper_data(plugin=globals.DEFAULT_PLUGIN, monitor=0, file=None, color=None, light=None):
    """Get current wallpaper or color from text file or plugin + containment combo
    and return a string with its type (color or image file)

    Args:
        script (str): javascript to evaluate
        monitor (int): containment (monitor) number
        plugin (str): wallpaper plugin id

    Returns:
        tuple: (type (int), data (str))
    """
    if plugin == None:
        plugin = globals.DEFAULT_PLUGIN
    if file:
        if os.path.exists(file):
            with open(file) as file:
                wallpaper = str(file.read()).replace('file://', '').strip()
                if wallpaper:
                    return ("image", wallpaper)
                else:
                    return None
        else:
            logging.error(f'File "{file}" does not exist')
            return None
    elif color:
        if color_utils.validate_color(color):
            return ("color", color)
        else:
            logging.error(f'Error: Color format "{color}" is incorrect')
    else:
        # special case for picture of the day plugin that requires a
        # directory, provider and a category
        if plugin == globals.PICTURE_OF_DAY_PLUGIN:
            # wait a bit to for wallpaper update
            script = """
            var Desktops = desktops();
                d = Desktops[%s];
                d.wallpaperPlugin = "%s";
                d.currentConfigGroup = Array("Wallpaper", "%s", "General");
                print(d.readConfig("Provider")+","+d.readConfig("Category"));
            """
            script_output = evaluate_script(script, monitor, plugin)
            if script_output != None:
                try:
                    script_output = tuple(script_output.split(","))
                except:
                    script_output = ('', '')
            else:
                script_output = ('', '')
            img_provider = script_output[0]
            provider_category = script_output[1]

            if img_provider:
                potd = globals.PICTURE_OF_DAY_PLUGIN_IMGS_DIR+img_provider
            else:
                # default provider is astronomic picture of the day
                potd = globals.PICTURE_OF_DAY_PLUGIN_IMGS_DIR + \
                    globals.PICTURE_OF_DAY_DEFAULT_PROVIDER

            # unsplash also has a category
            if img_provider == globals.PICTURE_OF_DAY_UNSPLASH_PROVIDER:
                # defaul category doesnt doesnt return id, add it
                if not provider_category:
                    provider_category = globals.PICTURE_OF_DAY_UNSPLASH_DEFAULT_CATEGORY
                potd = f"{potd}:{provider_category}"

            # Bing file now has the wallpaper resolution in the name
            if img_provider == globals.PICTURE_OF_DAY_BING_PROVIDER:
                # find and return files that start with bing and don't end with json and use the largest one
                potd = [file for file in os.listdir(globals.PICTURE_OF_DAY_PLUGIN_IMGS_DIR) if os.path.isfile(os.path.join(
                    globals.PICTURE_OF_DAY_PLUGIN_IMGS_DIR, file)) if file.startswith(globals.PICTURE_OF_DAY_BING_PROVIDER) and not file.endswith('json')]
                potd = globals.PICTURE_OF_DAY_PLUGIN_IMGS_DIR+max(potd)

            if os.path.exists(potd):
                return ("image", potd)
            else:
                return None
        elif plugin == globals.PLAIN_COLOR_PLUGIN:
            script = """
            var Desktops = desktops();
                d = Desktops[%s];
                d.wallpaperPlugin = "%s";
                d.currentConfigGroup = Array("Wallpaper", "%s", "General");
                print(d.readConfig("Color"));
            """
            color_rgb = evaluate_script(script, monitor, plugin)
            if color_rgb != None:
                try:
                    color_rgb = tuple(color_rgb.split(","))
                    return ("color", color_utils.rgb2hex(r=int(color_rgb[0]), g=int(color_rgb[1]), b=int(color_rgb[2])))
                except Exception as e:
                    logging.error(f'Plain color error: {e}')
                    return None
            else:
                return None
        else:
            # wallpaper plugin that stores current image
            script = """
            var Desktops = desktops();
                d = Desktops[%s];
                d.wallpaperPlugin = "%s";
                d.currentConfigGroup = Array("Wallpaper", "%s", "General");
                print(d.readConfig("Image"));
            """

            wallpaper = evaluate_script(script, monitor, plugin)
            if wallpaper != None:
                # if script returns a directory
                if os.path.isdir(wallpaper):
                    # check for mormal/dark variant
                    if os.path.exists(wallpaper+"contents/images_dark") and light == False:
                        wallpaper = file_utils.get_smallest_image(
                            wallpaper+"contents/images_dark/")

                    elif os.path.exists(wallpaper+"contents/images"):
                        wallpaper = file_utils.get_smallest_image(
                            wallpaper+"contents/images/")
                return ("image", wallpaper)


def evaluate_script(script, monitor, plugin):
    """Make a dbus call to org.kde.PlasmaShell.evaluateScript to get wallpaper data

    Args:
        script (str): js string to evaluate
        monitor (int): containment (monitor) number
        plugin (str): wallpaper plugin id

    Returns:
        string : wallpaper data (wallpaper path or color)
    """
    try:
        bus = dbus.SessionBus()
        plasma = dbus.Interface(bus.get_object(
            'org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
        wallpaper_data = str(plasma.evaluateScript(
            script % (monitor, plugin, plugin))).replace('file://', '')
        return wallpaper_data
    except Exception as e:
        logging.error(f'Error getting wallpaper from dbus:\n{e}')
        return None
