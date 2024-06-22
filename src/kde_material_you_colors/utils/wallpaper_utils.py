import os
import logging
import dbus
from kde_material_you_colors import settings
from kde_material_you_colors.utils import color_utils
from kde_material_you_colors.utils import file_utils
from kde_material_you_colors.utils import math_utils
from kde_material_you_colors.utils import kwin_utils
from kde_material_you_colors.config import Configs


class WallpaperReader:
    """Class containing the current wallpaper properties"""

    def __init__(self, config: Configs):
        """
        Args:
            config (Configs): Current configuration from args and file.
        """
        self._monitor = self.validate_monitor(config.read("monitor"))
        self._screenshot_only_mode = config.read("screenshot_only_mode")
        self._file = config.read("file")
        self._color = config.read("color")
        self._light = config.read("light")
        self._qdbus_executable = config.read("qdbus_executable") or "qdbus6"
        self._plugin = None
        self._type = None
        self._source = None
        self._error = None
        self._skip_screenshot = False
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

    def screenshot(self, skip_screenshot):
        self._type = "screenshot"
        if skip_screenshot:
            return
        if settings.SCREENSHOT_HELPER_PATH is None:
            self._error = "Screenshot helper is not installed. Use another wallpaper plugin or install the helper"
            return
        try:
            screenshot_taken = get_desktop_screenshot(
                self._monitor, self._qdbus_executable
            )
        except Exception as e:
            logging.exception(e)
            self._error = str(e)
            return

        if screenshot_taken:
            self._source = settings.SCREENSHOT_PATH
        else:
            error = "Could not take Desktop screenshot"
            logging.error(error)
            self._error = error

    def reload(self):
        """Reload current wallpaper"""
        if self._screenshot_only_mode:
            self.screenshot(self._skip_screenshot)
            return

        # Validate color
        self.validate_color()
        if self._source:
            return

        # Validate file
        self.validate_file()
        if self._source:
            return

        try:
            wallpaper_config = get_wallpaper_config(self._monitor)
        except dbus.DBusException as e:
            logging.error(e.get_dbus_message())
            self._error = e.get_dbus_message()
            return
        except Exception as e:
            logging.error(e)
            self._error = str(e)
            return

        plugin = wallpaper_config["wallpaperPlugin"]

        # special case for picture of the day plugin that requires a
        # directory, provider and sometimes a category
        self._plugin = plugin
        if plugin == settings.PICTURE_OF_DAY_PLUGIN:
            self._type = "image"
            potd = get_picture_of_the_day(wallpaper_config)
            if potd:
                self._source = potd
                return

        # wallpaper plugin that stores current image
        wallpaper = get_wallpaper_image(wallpaper_config, self._light)
        if wallpaper:
            self._type = "image"
            # if a single image wasn't returned show the error
            # and continue with screenshot method
            if isinstance(wallpaper, list):
                self._error = f"Could not get compatible image from plugin {plugin}, using screenshot method"
            else:
                self._source = wallpaper
                return

        # wallpaper plugin that stores current color
        color = wallpaper_config.get("color", wallpaper_config.get("Color"))
        if color:
            self._type = "color"
            color = color_utils.color2hex(int(color[0]))
            if color:
                self._source = color
                return

            error = f"Could not resolve color from {plugin}: {wallpaper_config}"
            logging.error(error)
            self._error = error

        # if everything fails, try taking a screenshot of the desktop
        self.screenshot(self._skip_screenshot)

    def update(self, config: Configs, skip_screenshot=False):
        """Update from config and reload wallpaper"""
        self._monitor = self.validate_monitor(config.read("monitor"))
        self._screenshot_only_mode = config.read("screenshot_only_mode")
        self._skip_screenshot = skip_screenshot
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


def get_desktop_screenshot(screen=0, qdbus_executable="qdbus6"):
    # take screenshot of desktop
    try:
        window_handle = kwin_utils.get_desktop_window_id(screen, qdbus_executable)
    except Exception as e:
        logging.exception(e)
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
    dbus_output = ""
    try:
        bus = dbus.SessionBus()
        plasma = dbus.Interface(
            bus.get_object("org.kde.plasmashell", "/PlasmaShell"),
            dbus_interface="org.kde.PlasmaShell",
        )
        dbus_output = plasma.wallpaper(monitor)
        # print(dbus_output)
    except dbus.DBusException as e:
        logging.exception(e.get_dbus_message(), "\n", e)
        raise
    except Exception as e:
        logging.error(e)
        raise

    try:
        if len(dbus_output) < 1:
            raise ValueError(f"Wallpaper DBus API says: {dbus_output}")
        return dbus_output
    except ValueError as e:
        logging.exception(e)
        raise


def get_picture_of_the_day(wallpaper_config):
    potd_cache_dir = settings.PICTURE_OF_DAY_PLUGIN_CACHE_DIR
    img_provider = wallpaper_config["Provider"]
    provider_category = wallpaper_config.get("Category")

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


def get_wallpaper_image(wallpaper_config, light):

    wallpaper = wallpaper_config.get("Image", wallpaper_config.get("image"))

    if wallpaper is None:
        return None

    wallpaper = wallpaper.replace("file://", "")
    if not os.path.isdir(wallpaper):
        return wallpaper

    dark_path = os.path.join(wallpaper, "contents/images_dark/")
    normal_path = os.path.join(wallpaper, "contents/images/")

    if not light and os.path.exists(dark_path):
        return file_utils.get_smallest_image(dark_path)
    if os.path.exists(normal_path):
        return file_utils.get_smallest_image(normal_path)

    return wallpaper
