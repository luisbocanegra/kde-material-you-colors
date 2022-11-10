
from utils import math_utils
import configparser
import logging
import globals
import os


class Configs():
    """
    Select configuration based on arguments and config file

    Returns:
        dict: Settings dictionary
    """

    def __init__(self, args):
        c_monitor = 0
        c_plugin = globals.DEFAULT_PLUGIN
        c_light = c_file = c_plugin = c_ncolor = c_iconsdark = c_iconslight = c_pywal = c_pywal_light = c_light_blend_multiplier = c_dark_blend_multiplier = c_on_change_hook = c_sierra_breeze_buttons_color = c_konsole_profile = c_titlebar_opacity = c_toolbar_opacity = c_konsole_opacity = c_color = None
        config = configparser.ConfigParser()
        if os.path.exists(globals.USER_CONFIG_PATH+globals.CONFIG_FILE):
            try:
                config.read(globals.USER_CONFIG_PATH+globals.CONFIG_FILE)
                if 'CUSTOM' in config:
                    custom = config['CUSTOM']
                    try:
                        c_light = custom.getboolean('light', None)
                    except:
                        logging.error(
                            'Value for light must be a boolean, using default None')
                        c_light = None

                    c_file = custom.get('file')

                    c_monitor = custom.getint('monitor', 0)
                    if c_monitor < 0:
                        c_monitor = 0
                        logging.error(
                            'Value for monitor must be a positive integer, using default 0')

                    c_ncolor = custom.getint('ncolor', 0)
                    if c_ncolor < 0:
                        c_ncolor = None
                        logging.error(
                            'Value for ncolor must be a positive integer, using default 0')

                    c_plugin = custom.get('plugin')
                    c_color = custom.get('color')
                    c_iconslight = custom.get('iconslight')
                    c_iconsdark = custom.get('iconsdark')

                    try:
                        c_pywal = custom.getboolean('pywal', None)
                    except:
                        logging.error(
                            'Value for pywal must be a boolean, using default None')
                        c_pywal = None

                    try:
                        c_pywal_light = custom.getboolean('pywal_light', None)
                    except:
                        logging.error(
                            'Value for pywal_light must be a boolean, using default None')
                        c_pywal_light = None

                    try:
                        c_light_blend_multiplier = custom.getfloat(
                            'light_blend_multiplier')
                    except:
                        logging.error(
                            'Value for light_blend_multiplier must be a number between 0.0 and 4.0 , using default 1.0')
                        c_light_blend_multiplier = 1

                    try:
                        c_dark_blend_multiplier = custom.getfloat(
                            'dark_blend_multiplier')
                    except:
                        logging.error(
                            'Value for dark_blend_multiplier must be a number between 0.0 and 4.0, using default 1.0')
                        c_dark_blend_multiplier = 1

                    c_on_change_hook = custom.get('on_change_hook')

                    try:
                        c_sierra_breeze_buttons_color = custom.getboolean(
                            'sierra_breeze_buttons_color', None)
                    except:
                        logging.error(
                            'Value for sierra_breeze_buttons_color must be a boolean, using default None')
                        c_sierra_breeze_buttons_color = None

                    c_konsole_profile = custom.get('konsole_profile')

                    c_titlebar_opacity = custom.getint(
                        'titlebar_opacity', None)
                    if c_titlebar_opacity != None:
                        if c_titlebar_opacity < 0 or c_titlebar_opacity > 100:
                            logging.error(
                                'Value for titlebar_opacity must be an integer between 0 and 100, using default 100')
                            c_titlebar_opacity = 100

                    c_toolbar_opacity = custom.getint('toolbar_opacity', None)
                    if c_toolbar_opacity != None:
                        if c_toolbar_opacity < 0 or c_toolbar_opacity > 100:
                            logging.error(
                                'Value for toolbar_opacity must be an integer between 0 and 100, using default 100')
                            c_toolbar_opacity = 100

                    c_konsole_opacity = custom.getint('konsole_opacity', None)
                    if c_konsole_opacity != None:
                        if c_konsole_opacity < 0 or c_konsole_opacity > 100:
                            logging.error(
                                'Value for konsole_opacity must be an integer between 0 and 100, using default 100')
                            c_konsole_opacity = 100

            except Exception as e:
                logging.error(f"Please fix your settings file:\n{e}\n")

        if args.dark == True:
            c_light = False
        elif args.light == True:
            c_light = args.light

        if args.pywal == True:
            c_pywal = args.pywal
        elif c_pywal == None:
            c_pywal = args.pywal

        if args.pywaldark == True:
            c_pywal_light = False
        elif args.pywallight == True:
            c_pywal_light = args.pywallight

        if args.lbmultiplier != None:
            c_light_blend_multiplier = math_utils.clip(
                args.lbmultiplier, 0, 4, 1)
        elif c_light_blend_multiplier != None:
            c_light_blend_multiplier = math_utils.clip(
                c_light_blend_multiplier, 0, 4, 1)

        if args.dbmultiplier != None:
            c_dark_blend_multiplier = math_utils.clip(
                args.dbmultiplier, 0, 4, 1)
        elif c_dark_blend_multiplier != None:
            c_dark_blend_multiplier = math_utils.clip(
                c_dark_blend_multiplier, 0, 4, 1)

        if args.file != None:
            c_file = args.file

        if args.monitor != None:
            if args.monitor < 0:
                logging.error(
                    'Value for --monitor must be a positive integer, using default 0')
                logging.error
            else:
                c_monitor = args.monitor

        if args.ncolor != None:
            if args.ncolor < 0:
                logging.error(
                    'Value for --ncolor must be a positive integer, using default 0')
                logging.error
            else:
                c_ncolor = args.ncolor

        if args.plugin != None:
            c_plugin = args.plugin

        if args.color != None:
            c_color = args.color

        if args.iconslight != None:
            c_iconslight = args.iconslight

        if args.iconsdark != None:
            c_iconsdark = args.iconsdark

        if args.on_change_hook != None:
            c_on_change_hook = args.on_change_hook

        if args.sierra_breeze_buttons_color == True:
            c_sierra_breeze_buttons_color = args.sierra_breeze_buttons_color

        if args.konsole_profile != None:
            c_konsole_profile = args.konsole_profile

        if args.titlebar_opacity != None:
            if args.titlebar_opacity < 0 or args.titlebar_opacity > 100:
                logging.error(
                    'Value for --sbe-titlebar-opacity must be an integer between 0 and 100, using default 100')

            else:
                c_titlebar_opacity = args.titlebar_opacity

        if args.toolbar_opacity != None:
            if args.toolbar_opacity < 0 or args.toolbar_opacity > 100:
                logging.error(
                    'Value for --toolbar-opacity must be an integer between 0 and 100, using default 100')

            else:
                c_toolbar_opacity = args.toolbar_opacity

        if args.konsole_opacity != None:
            if args.konsole_opacity < 0 or args.konsole_opacity > 100:
                logging.error(
                    'Value for --konsole-opacity must be an integer between 0 and 100, using default 100')
            else:
                c_konsole_opacity = args.konsole_opacity
        elif args.konsole_opacity == None and c_konsole_opacity == None:
            c_konsole_opacity = None

        self._options = {
            'light': c_light,
            'file': c_file,
            'monitor': c_monitor,
            'plugin': c_plugin,
            'ncolor': c_ncolor,
            'iconslight': c_iconslight,
            'iconsdark': c_iconsdark,
            "pywal": c_pywal,
            "pywal_light":  c_pywal_light,
            "lbm": c_light_blend_multiplier,
            "dbm": c_dark_blend_multiplier,
            "on_change_hook": c_on_change_hook,
            "sierra_breeze_buttons_color": c_sierra_breeze_buttons_color,
            "konsole_profile": c_konsole_profile,
            "titlebar_opacity": c_titlebar_opacity,
            "toolbar_opacity": c_toolbar_opacity,
            "konsole_opacity": c_konsole_opacity,
            "color": c_color
        }

    @property
    def options(self):
        return self._options
