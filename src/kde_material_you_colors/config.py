import configparser
import logging
import os
from .utils import color_utils
from .utils import math_utils


class Configs:
    """Create configuration based on arguments and config file"""

    def __init__(self, args, config_file):
        self._args = args
        self._config_file = config_file
        self._light = None
        self._pywal_light = None
        self._config = configparser.ConfigParser(allow_no_value=False)
        self._options = {}

        if args.dark is True:
            self._light = False
        elif args.light is True:
            self._light = True
        else:
            self._light = None

        if args.pywaldark is True:
            self._pywal_light = False
        elif args.pywallight is True:
            self._pywal_light = True
        else:
            self._pywal_light = None

        self.update_config()

    def update_config(self):
        self.get_conf()

        # loop and read configs
        self.parse_conf()

        options = self._options

        if options["plasma_follows_scheme"]:
            options["light"] = None

        if options["pywal_follows_scheme"]:
            options["pywal_light"] = None

        # silently limit out of range values

        options["monitor"] = math_utils.clip(
            options["monitor"], 0, options["monitor"], 0
        )

        options["ncolor"] = math_utils.clip(options["ncolor"], 0, options["ncolor"], 0)

        options["dark_blend_multiplier"] = math_utils.clip(
            options["dark_blend_multiplier"], 0, 4, 1
        )

        options["light_blend_multiplier"] = math_utils.clip(
            options["light_blend_multiplier"], 0, 4, 1
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

        options["startup_delay"] = math_utils.clip(
            options["startup_delay"], 0, options["startup_delay"], 0
        )

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
                                "Value for custom_colors_list only accepts colors in rgb or hex format"
                            )
                        elif fmt == 1:
                            options["custom_colors_list"][i] = color_utils.color2hex(
                                color
                            )
        except Exception as e:
            options["custom_colors_list"] = None
            logging.exception(
                f"Please fix your settings file: {e}, using wallpaper colors"
            )

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

    @property
    def defaults(self):
        # property : [value, fallback, type]
        # Types: 0 = bool, 1 = int, 2 = float, 3 = str
        args = self._args
        return {
            "light": [self._light, None, 0],
            "file": [args.file, None, 3],
            "monitor": [args.monitor, 0, 1],
            "ncolor": [args.ncolor, 0, 1],
            "iconslight": [args.iconslight, None, 3],
            "iconsdark": [args.iconsdark, None, 3],
            "pywal": [args.pywal, None, 0],
            "pywal_light": [self._pywal_light, None, 0],
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

    def parse_conf(self):
        """Create options dictionary from configuration or arguments/defaults"""
        for key, val in self.defaults.items():
            self._options[key] = self.eval_conf(
                key=key,
                conf_type=val[2],
                value=val[0],
                fallback=val[1],
            )

    def get_conf(self):
        """Open the config file"""
        if os.path.exists(self._config_file):
            try:
                self._config.read(self._config_file)
                if "CUSTOM" not in self._config:
                    logging.warning(
                        "[CUSTOM] section not found in config file, ignoring it"
                    )
                    self._config.add_section("CUSTOM")
            except Exception as e:
                logging.exception(f"{e}\n")
        else:
            logging.debug("No configuration file was found")
            self._config.add_section("CUSTOM")

    def eval_conf(self, key, conf_type, value, fallback):
        """Get a config value depending on its type (0 = bool, 1 = int, 2 = float, 3 = str), with default value on error"""

        if self._config is not None:
            section = self._config["CUSTOM"]
            # check for empty configuration values and fallback right away
            res = section.get(key, fallback) if value is None else value
            if isinstance(res, str) and len(res) == 0:
                logging.debug(f'Config "{key}": empty, using fallback: {fallback}')
                return fallback
            try:
                if conf_type == 0:
                    return section.getboolean(key, fallback) if value is None else value
                if conf_type == 1:
                    return section.getint(key, fallback) if value is None else value
                if conf_type == 2:
                    return section.getfloat(key, fallback) if value is None else value
                if conf_type == 3:
                    return section.get(key, fallback) if value is None else value
            except Exception as e:
                logging.exception(f'Config "{key}": {e}, using fallback: {fallback}')
                return fallback
        else:
            return fallback if value is None else value
