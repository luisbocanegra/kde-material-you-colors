
from utils import color_utils
import configparser
import logging
import globals
import os


def get_conf(conf_path):
    """Open the config file and do simple checks on it"""
    if os.path.exists(conf_path):
        try:
            config = configparser.ConfigParser()
            config.read(conf_path)
            return config
        except Exception as e:
            logging.error(f"{e}\n")
        if 'CUSTOM' not in config:
            logging.error(
                f"Config file {conf_path} doesn't have a ['CUSTOM'] section")
    else:
        pass


def show_conf_err(exception, conf_name, default):
    """Show the error from a given config name"""
    logging.error(
        f"Error for {conf_name} value: {exception}, using default {default}")


def eval_conf(config: configparser.ConfigParser, val, conf_type, default):
    """Get a config value depending on its type (0 = bool, 1 = int, 2 = float, 3 = str), with default value on error"""

    if config is not None:
        section = config['CUSTOM']
        try:
            if conf_type == 0:
                return section.getboolean(
                    val, default)
            elif conf_type == 1:
                return section.getint(
                    val, default
                )
            elif conf_type == 2:
                return section.getfloat(
                    val, default
                )
            elif conf_type == 3:
                return section.get(
                    val, default
                )
        except Exception as e:
            show_conf_err(e, val, default)
            return default
    else:
        return default


class Configs():
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

        # 'config' : [value,type[0=bool,1=int,2=float,3=str]]
        defaults = {
            'light': [light, 0],
            'file': [args.file or None, 3],
            'monitor': [args.monitor or 0, 1],
            'plugin': [args.plugin or globals.DEFAULT_PLUGIN, 3],
            'ncolor': [args.ncolor if args.ncolor else 0, 1],
            'iconslight': [args.iconslight or None, 3],
            'iconsdark': [args.iconsdark or None, 3],
            'pywal': [args.pywal, 0],
            'pywal_light': [pywal_light, 0],
            'light_blend_multiplier': [args.lbmultiplier or 1, 2],
            'dark_blend_multiplier': [args.dbmultiplier or 1, 2],
            'on_change_hook': [args.on_change_hook or None, 3],
            'sierra_breeze_buttons_color': [args.sierra_breeze_buttons_color, 0],
            'konsole_profile': [args.konsole_profile or None, 3],
            'titlebar_opacity': [args.titlebar_opacity or None, 1],
            'toolbar_opacity': [args.toolbar_opacity or 100, 1],
            'konsole_opacity': [args.konsole_opacity or 100, 1],
            'color': [args.color or None, 3],
            'klassy_windeco_outline': [args.klassy_windeco_outline, 0],
            'custom_colors_list': [args.custom_colors_list or None, 3],
            'darker_window_list': [args.darker_window_list or None, 3],
            'use_startup_delay': [args.use_startup_delay or None, 0],
            'startup_delay': [args.startup_delay or 0, 1]
        }
        options = defaults
        config = get_conf(globals.USER_CONFIG_PATH + globals.CONFIG_FILE)

        # loop and read configs
        for k, v in defaults.items():
            options[k] = eval_conf(config, k, v[1], defaults[k][0])
        # Some logging for incorrect values
        if options['monitor'] < 0:
            logging.warning(
                "Value for monitor must be a positive number, using default 0")
        if options['ncolor'] < 0:
            logging.warning(
                "Value for ncolor must be a positive number, using default 0")
        if options['dark_blend_multiplier'] < 0 or options['dark_blend_multiplier'] > 4:
            logging.warning(
                "Value for dark_blend_multiplier must be a number between 0.0 and 4.0, using default 1.0")
        if options['light_blend_multiplier'] < 0 or options['light_blend_multiplier'] > 4:
            logging.warning(
                "Value for light_blend_multiplier must be a number between 0.0 and 4.0, using default 1.0")
        if options['toolbar_opacity'] < 0 or options['toolbar_opacity'] > 100:
            logging.error(
                'Value for toolbar_opacity must be an integer between 0 and 100, using default 100')
            options['toolbar_opacity'] = 100
        if options['konsole_opacity'] < 0 or options['konsole_opacity'] > 100:
            logging.error(
                'Value for konsole_opacity must be an integer between 0 and 100, using default 100')
            options['konsole_opacity'] = 100

        try:
            if options['custom_colors_list'] is not None:
                options['custom_colors_list'] = options['custom_colors_list'].split(
                    ' ')
                if len(options['custom_colors_list']) < 7:
                    raise TypeError(
                        "Value for custom_colors_list must contain 7 elements (rgb or hex colors), space separated")
                else:
                    for i, color in enumerate(options['custom_colors_list']):
                        fmt = color_utils.validate_color(color)
                        if fmt is None:
                            raise TypeError(
                                "Value for custom_colors_list only accepts rgb or hex colors")
                        elif fmt == 1:
                            options['custom_colors_list'][i] = color_utils.color2hex(
                                color)
        except Exception as e:
            options['custom_colors_list'] = None
            logging.error(
                f'Please fix your settings file: {e}, using wallpaper colors')

        self._options = options

    @property
    def options(self):
        return self._options
