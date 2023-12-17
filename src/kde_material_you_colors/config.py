import configparser
import logging
import os
from . import settings
from .utils import color_utils
from .utils import math_utils


def get_conf(conf_path: str):
    """Open the config file"""
    config = configparser.ConfigParser(empty_lines_in_values=True)
    if os.path.exists(conf_path):
        try:
            config.read(conf_path)
            if "CUSTOM" not in config:
                logging.warning(
                    "[CUSTOM] section not found in config file, ignoring it"
                )
                config.add_section("CUSTOM")
        except Exception as e:
            logging.error(f"{e}\n")
    else:
        logging.debug("No configuration file was found")
        config.add_section("CUSTOM")
    return config


def show_conf_err(exception, conf_name, fallback):
    """Show the error from a given config name"""
    logging.error(f'Config "{conf_name}": {exception}, using fallback: {fallback}')


def eval_conf(config: configparser.ConfigParser, val, conf_type, arg, fallback):
    """Get a config value depending on its type (0 = bool, 1 = int, 2 = float, 3 = str), with default value on error"""

    if config is not None:
        section = config["CUSTOM"]
        # check for empty configuration values and fallback right away
        res = section.get(val, fallback) if arg is None else arg
        if isinstance(res, str) and len(res) == 0:
            logging.debug(f'Config "{val}": empty, using fallback: {fallback}')
            return fallback
        try:
            if conf_type == 0:
                return section.getboolean(val, fallback) if arg is None else arg
            elif conf_type == 1:
                return section.getint(val, fallback) if arg is None else arg
            elif conf_type == 2:
                return section.getfloat(val, fallback) if arg is None else arg
            elif conf_type == 3:
                return section.get(val, fallback) if arg is None else arg
        except Exception as e:
            show_conf_err(e, val, fallback)
            return fallback
    else:
        return fallback if arg is None else arg


class Configs:
    """
    Select configuration based on arguments and config file

    Returns:
        dict: Settings dictionary
    """

    def __init__(self, args):
        if args.dark is True:
            light = False
        elif args.light is True:
            light = True
        else:
            light = None

        if args.pywaldark is True:
            pywal_light = False
        elif args.pywallight is True:
            pywal_light = True
        else:
            pywal_light = None

        # property : [value, fallback, type]
        # Types: 0 = bool, 1 = int, 2 = float, 3 = str
        defaults = {
            "light": [light, None, 0],
            "file": [args.file, None, 3],
            "monitor": [args.monitor, 0, 1],
            "ncolor": [args.ncolor, 0, 1],
            "iconslight": [args.iconslight, None, 3],
            "iconsdark": [args.iconsdark, None, 3],
            "pywal": [args.pywal, None, 0],
            "pywal_light": [pywal_light, None, 0],
            "light_blend_multiplier": [args.lbmultiplier, 1, 2],
            "dark_blend_multiplier": [args.dbmultiplier, 1, 2],
            "on_change_hook": [args.on_change_hook, None, 3],
            "sierra_breeze_buttons_color": [args.sierra_breeze_buttons_color, None, 0],
            "disable_konsole": [args.disable_konsole, False, 0],
            "titlebar_opacity": [args.titlebar_opacity, None, 1],
            "titlebar_opacity_dark": [args.titlebar_opacity_dark, None, 1],
            "toolbar_opacity": [args.toolbar_opacity, None, 1],
            "toolbar_opacity_dark": [args.toolbar_opacity_dark, None, 1],
            "konsole_opacity": [args.konsole_opacity, None, 1],
            "konsole_opacity_dark": [args.konsole_opacity_dark, None, 1],
            "color": [args.color, None, 3],
            "klassy_windeco_outline": [args.klassy_windeco_outline, None, 0],
            "custom_colors_list": [args.custom_colors_list, None, 3],
            "darker_window_list": [args.darker_window_list, None, 3],
            "use_startup_delay": [args.use_startup_delay, None, 0],
            "startup_delay": [args.startup_delay, 0, 1],
            "plasma_follows_scheme": [None, None, 0],
            "pywal_follows_scheme": [None, None, 0],
            "main_loop_delay": [args.main_loop_delay, 1, 2],
            "screenshot_delay": [args.screenshot_delay, 900, 2],
            "once_after_change": [args.once_after_change, False, 0],
            "pause_mode": [None, False, 0],
        }
        options = {}
        config = get_conf(settings.USER_CONFIG_PATH + settings.CONFIG_FILE)

        # loop and read configs
        for key, val in defaults.items():
            options[key] = eval_conf(
                config=config, val=key, conf_type=val[2], arg=val[0], fallback=val[1]
            )

        if options["plasma_follows_scheme"]:
            options["light"] = None

        if options["pywal_follows_scheme"]:
            options["pywal_light"] = None

        # Some logging for out of range values
        if options["monitor"] < 0:
            logging.warning(
                "Value for monitor must be a positive number, using default 0"
            )

        if options["ncolor"] < 0:
            logging.warning(
                "Value for ncolor must be a positive number, using default 0"
            )

        if options["dark_blend_multiplier"] < 0 or options["dark_blend_multiplier"] > 4:
            logging.warning(
                "Value for dark_blend_multiplier must be a number between 0.0 and 4.0, using default 1.0"
            )

        if (
            options["light_blend_multiplier"] < 0
            or options["light_blend_multiplier"] > 4
        ):
            logging.warning(
                "Value for light_blend_multiplier must be a number between 0.0 and 4.0, using default 1.0"
            )

        options["toolbar_opacity"] = math_utils.clip(
            options["toolbar_opacity"], 0, 100, 100
        )

        options["toolbar_opacity_dark"] = math_utils.clip(
            options["toolbar_opacity_dark"], 0, 100, 100
        )

        options["konsole_opacity"] = math_utils.clip(
            options["konsole_opacity"], 0, 100, 100
        )

        options["konsole_opacity_dark"] = math_utils.clip(
            options["konsole_opacity_dark"], 0, 100, 100
        )

        options["titlebar_opacity"] = math_utils.clip(
            options["titlebar_opacity"], 0, 100, 100
        )

        options["titlebar_opacity_dark"] = math_utils.clip(
            options["titlebar_opacity_dark"], 0, 100, 100
        )

        if options["startup_delay"] < 0:
            logging.warning(
                "Value for startup_delay must be an positive integer, using default 0"
            )
            options["startup_delay"] = 0

        try:
            if options["custom_colors_list"] is not None:
                options["custom_colors_list"] = options["custom_colors_list"].split(" ")
                if len(options["custom_colors_list"]) < 7:
                    raise TypeError(
                        "Value for custom_colors_list must contain 7 elements (rgb or hex colors), space separated"
                    )
                else:
                    for i, color in enumerate(options["custom_colors_list"]):
                        fmt = color_utils.validate_color(color)
                        if fmt is None:
                            raise TypeError(
                                "Value for custom_colors_list only accepts rgb or hex colors"
                            )
                        elif fmt == 1:
                            options["custom_colors_list"][i] = color_utils.color2hex(
                                color
                            )
        except Exception as e:
            options["custom_colors_list"] = None
            logging.error(f"Please fix your settings file: {e}, using wallpaper colors")

        if options["main_loop_delay"] > options["screenshot_delay"]:
            logging.warning(
                f"Value for main_loop_delay ({options['main_loop_delay']}) should be smaller than screenshot_delay ({options['screenshot_delay']}), will be set to {options['screenshot_delay']}"
            )

        self._options = options

    @property
    def options(self):
        return self._options

    def read(self, key: str):
        if key in self._options:
            return self._options[key]
