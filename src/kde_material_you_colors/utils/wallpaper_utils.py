import os
import logging
import dbus
from .. import settings
from . import color_utils
from . import file_utils
from . import math_utils
from . import kwin_utils
from ..config import Configs


class WallpaperReader:
    """Class containing the current wallpaper properties"""

    def __init__(self, config: Configs):
        """
        Args:
            monitor (_type_, optional): _description_. Defaults to None.
            file (_type_, optional): _description_. Defaults to None.
            color (_type_, optional): _description_. Defaults to None.
            light (_type_, optional): _description_. Defaults to None.
        """
        self._monitor = self.validate_monitor(config.read("monitor"))
        self._file = config.read("file")
        self._color = config.read("color")
        self._light = config.read("light")
        self._plugin = None
        self._type = None
        self._source = None
        self._error = None
        self.reload()

    def __str__(self) -> str:
        return f"Wallpaper: {self._plugin} ({self._type}): {self._source}"

    @staticmethod
    def validate_monitor(monitor) -> int:
        return math_utils.clip(monitor, 0, 999, 0)

    def validate_color(self):
        if self._color:
            self._plugin = "Custom color"
            self._type = "color"
            if color_utils.validate_color(self._color):
                self._source = self._color
            else:
                error = f"Error: Color format '{self._color}' is incorrect"
                logging.error(error)
                self._error = error

    def validate_file(self):
        if self._file:
            self._plugin = "file"
            # TODO: detect image file too
            self._type = "image"
            if os.path.exists(self._file):
                with open(self._file, encoding="utf-8") as text_file:
                    wallpaper = str(text_file.read()).replace("file://", "").strip()
                    if wallpaper:
                        self._source = wallpaper
            else:
                error = f"File '{self._file}' does not exist"
                logging.error(error)
                self._error = error

    @property
    def plugin(self):
        return self._plugin

    @property
    def type(self):
        return self._type

    @property
    def source(self):
        return self._source

    @property
    def error(self):
        return self._error

    @property
    def current(self):
        o = {
            "plugin": self._plugin,
            "type": self._type,
            "source": self._source,
            "error": self._error,
        }
        return o

    def reload(self):
        """Reload current wallpaper"""
        # Validate color first
        self.validate_color()
        if self._source:
            return

        # Validate file
        self.validate_file()
        if self._source:
            return

        try:
            output = get_wallpaper_config(self._monitor)
        except dbus.DBusException as e:
            logging.error(e.get_dbus_message())
            self._error = e.get_dbus_message()
            return
        except Exception as e:
            logging.error(e)
            self._error = str(e)
            return
        # Get plugin data, allow commas in plugin config
        plugin, plugin_config = (output).split(",", 1)
        # split config and value
        plugin_config = plugin_config.split(",", 1)

        # special case for picture of the day plugin that requires a
        # directory, provider and sometimes a category
        self._plugin = plugin
        if plugin == settings.PICTURE_OF_DAY_PLUGIN:
            self._type = "image"
            potd = get_picture_of_the_day(plugin_config)
            if potd:
                self._source = potd
                return

        # Color based wallpapers
        elif plugin_config[0] in ["color", "Color"] and len(plugin_config) >= 2:
            self._type = "color"
            color = color_utils.color2hex(plugin_config[1])
            if color:
                self._source = color
                return
            else:
                error = f"Could not resolve color from {plugin}: {plugin_config[1]}"
                logging.error(error)
                self._error = error

        # wallpaper plugin that stores current image
        wallpaper = get_wallpaper_image(plugin_config, self._light)
        if wallpaper:
            self._type = "image"
            # if a single image wasn't returned show the error
            # and continue with screenshot method
            if isinstance(wallpaper, list):
                self._error = f"Could not get compatible image from plugin {plugin}, using screenshot method"
            else:
                self._source = wallpaper
                return
        else:
            # if everything fails, take as screenshot of the desktop
            self._type = "screenshot"
        try:
            screenshot_taken = get_desktop_screenshot(self._monitor)
        except Exception as e:
            logging.error(e)
            self._error = str(e)
            return

        if screenshot_taken:
            self._source = settings.SCREENSHOT_PATH
        else:
            error = "Could not take Desktop screenshot"
            logging.error(error)
            self._error = error

    def update(self, config: Configs):
        """Update from config and reload wallpaper"""
        self._monitor = self.validate_monitor(config.read("monitor"))
        self._file = config.read("file")
        self._color = config.read("color")
        self._light = config.read("light")
        self._plugin = None
        self._type = None
        self._source = None
        self._error = None
        self.reload()

    def is_image(self):
        return self._type == "image"

    def is_screenshot(self):
        return self._type == "screenshot"


def evaluate_script(script: str):
    """Make a dbus call to org.kde.PlasmaShell.evaluateScript

    Args:
        script (str): js string to evaluate

    Returns:
        string : Script output
    """
    script_output = ""
    try:
        bus = dbus.SessionBus()
        plasma = dbus.Interface(
            bus.get_object("org.kde.plasmashell", "/PlasmaShell"),
            dbus_interface="org.kde.PlasmaShell",
        )
        script_output = str(plasma.evaluateScript(script)).replace("file://", "")
    except dbus.DBusException as e:
        error = f"Error getting wallpaper from dbus: {e.get_dbus_message()}"
        logging.exception(error)
        raise
    return script_output


def get_desktop_screenshot(screen=0):
    # take screenshot of desktop
    try:
        window_handle = kwin_utils.get_desktop_window_id(screen)
    except Exception as e:
        logging.error(e)
        raise

    screenshot_taken = False
    if window_handle is not None:
        try:
            screenshot_taken = kwin_utils.screenshot_window(
                window_handle, settings.SCREENSHOT_PATH
            )
        except Exception as e:
            logging.error(e)
            raise
    return screenshot_taken


def get_wallpaper_config(monitor=0):
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
var desktop;
if ({monitor} < desktops.length) {{
    for (let i=0; i<desktops.length; i++) {{
        if (desktops[i].screen == {monitor}) {{
            desktop = desktops[i];
            break
        }}
    }}
    if (desktop !== undefined) {{
        if ('wallpaperPlugin' in desktop) {{
            var plugin = desktop.wallpaperPlugin
            desktop.currentConfigGroup = Array("Wallpaper", plugin, "General");
            const keys = ["Image", "Color","color","Provider"];
            var config = getConfig(desktop, keys);
            print(plugin+","+config);
        }}
    }} else {{
        print("monitor value '{monitor}' didn't match any Desktop")
    }}
}} else {{
    print("monitor value '{monitor}' out of range")
}}
"""
    script_output = ""
    try:
        script_output = evaluate_script(script)
    except dbus.DBusException as e:
        logging.error(e.get_dbus_message())
        raise
    except Exception as e:
        logging.error(e)
        raise
    else:
        try:
            if len(script_output.split(",")) < 2:
                raise ValueError(f"Plasma Scripting API says: {script_output}")
            return script_output
        except ValueError as e:
            logging.exception(e)
            raise


def get_picture_of_the_day(plugin_config):
    potd_cache_dir = settings.PICTURE_OF_DAY_PLUGIN_CACHE_DIR
    plugin_config = plugin_config[1] if len(plugin_config) > 1 else ""
    img_provider, provider_category = (plugin_config + ",").split(",")[:2]

    if not img_provider:
        img_provider = settings.PICTURE_OF_DAY_DEFAULT_PROVIDER

    potd_image = os.path.join(potd_cache_dir, img_provider)

    # unsplash also has a category
    if img_provider == settings.PICTURE_OF_DAY_UNSPLASH_PROVIDER:
        # defaul category doesnt return id, add it
        if not provider_category:
            provider_category = settings.PICTURE_OF_DAY_UNSPLASH_DEFAULT_CATEGORY
        potd_image = f"{potd_image}:{provider_category}"

    if img_provider == settings.PICTURE_OF_DAY_BING_PROVIDER:
        potd_files = [
            file
            for file in os.listdir(potd_cache_dir)
            if file.startswith(img_provider) and not file.endswith("json")
        ]
        potd_image = os.path.join(potd_cache_dir, max(potd_files, default=""))

    return potd_image if os.path.exists(potd_image) else None


def get_wallpaper_image(plugin_config, light):
    if plugin_config[0] != "Image" or len(plugin_config) < 2:
        return None

    wallpaper = plugin_config[1]
    if not os.path.isdir(wallpaper):
        return wallpaper

    dark_path = os.path.join(wallpaper, "contents/images_dark/")
    normal_path = os.path.join(wallpaper, "contents/images/")

    if not light and os.path.exists(dark_path):
        return file_utils.get_smallest_image(dark_path)
    elif os.path.exists(normal_path):
        return file_utils.get_smallest_image(normal_path)

    return wallpaper
