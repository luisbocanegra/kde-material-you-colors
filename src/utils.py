import re
from schemeconfigs import ThemeConfig
import signal
from logging.handlers import RotatingFileHandler
import logging
import os
from pathlib import Path
import subprocess
import json
import configparser
import sys
import dbus
from color_utils import hex2rgb, rgb2hex
import importlib.util
from material_color_utilities_python.utils.theme_utils import *
from extra_image_utils import sourceColorsFromImage
USER_HAS_COLR = importlib.util.find_spec("colr") is not None
if USER_HAS_COLR:
    from colr import color
USER_HAS_PYWAL = importlib.util.find_spec("pywal") is not None
if USER_HAS_PYWAL:
    import pywal
# Set logging level for pillow
logging.getLogger('PIL').setLevel(logging.WARNING)
HOME = str(Path.home())
SAMPLE_CONFIG_FILE = "sample_config.conf"
CONFIG_FILE = "config.conf"
SAMPLE_CONFIG_PATH = "/usr/lib/kde-material-you-colors/"
USER_CONFIG_PATH = HOME+"/.config/kde-material-you-colors/"
USER_SCHEMES_PATH = HOME+"/.local/share/color-schemes"
THEME_LIGHT_PATH = USER_SCHEMES_PATH+"/MaterialYouLight"
THEME_DARK_PATH = USER_SCHEMES_PATH+"/MaterialYouDark"
AUTOSTART_SCRIPT = "kde-material-you-colors.desktop"
SAMPLE_AUTOSTART_SCRIPT_PATH = "/usr/lib/kde-material-you-colors/"
USER_AUTOSTART_SCRIPT_PATH = HOME+"/.config/autostart/"
DEFAULT_PLUGIN = 'org.kde.image'
PICTURE_OF_DAY_PLUGIN = 'org.kde.potd'
PLAIN_COLOR_PLUGIN = 'org.kde.color'
PICTURE_OF_DAY_PLUGIN_IMGS_DIR = HOME+'/.cache/plasma_engine_potd/'
PICTURE_OF_DAY_UNSPLASH_PROVIDER = 'unsplash'
PICTURE_OF_DAY_UNSPLASH_DEFAULT_CATEGORY = '1065976'
PICTURE_OF_DAY_DEFAULT_PROVIDER = 'apod'  # astronomy picture of the day
PICTURE_OF_DAY_BING_PROVIDER = 'bing'
KDE_GLOBALS = HOME+"/.config/kdeglobals"
BREEZE_RC = HOME+"/.config/breezerc"
SBE_RC = HOME+"/.config/sierrabreezeenhancedrc"
KLASSY_RC = HOME+"/.config/klassyrc"
KONSOLE_DIR = HOME+"/.local/share/konsole/"
KONSOLE_COLOR_SCHEME_PATH = KONSOLE_DIR+"MaterialYou.colorscheme"
KONSOLE_COLOR_SCHEME_ALT_PATH = KONSOLE_DIR+"MaterialYouAlt.colorscheme"
KONSOLE_TEMP_PROFILE = KONSOLE_DIR+"TempMyou.profile"
BOLD = "\033[1m"
COLOR_RESET = "\033[0;0m"
LOG_HINT = '\033[31m'
LOG_WHERE = BOLD+'\033[37m'
COLOR_ERROR = COLOR_RESET+'\033[36m'
COLOR_WARN = COLOR_RESET+'\033[35m'
COLOR_DEBUG = COLOR_RESET+'\033[34m'
COLOR_INFO = COLOR_RESET+'\033[33m'
BOLD_RESET = COLOR_RESET+BOLD
LOG_FILE_PATH = HOME+"/.local/share/kde-material-you-colors/"
LOG_FILE_NAME = "kde-material-you-colors.log"
MATERIAL_YOU_COLORS_JSON = "/tmp/kde-material-you-colors.json"
# Custom logging format (adapted from https://stackoverflow.com/a/14859558)


class MyFormatter(logging.Formatter):

    term_fmt = '{}[%(levelname).1s] {}%(module)s: %(funcName)s: {}%(message)s'
    file_fmt = '%(asctime)s.%(msecs)03d [%(levelname).1s] %(module)s: %(funcName)s: %(message)s'
    dbg_fmt = term_fmt.format(LOG_HINT, LOG_WHERE, COLOR_DEBUG)
    info_fmt = term_fmt.format(LOG_HINT, LOG_WHERE, COLOR_INFO)
    warn_fmt = term_fmt.format(LOG_HINT, LOG_WHERE, COLOR_WARN)
    err_fmt = term_fmt.format(LOG_HINT, LOG_WHERE, COLOR_ERROR)

    def __init__(self, to_file):
        self.to_file = to_file
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt="%Y-%m-%d %H:%M:%S", style='%')

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if self.to_file == False:
            if record.levelno == logging.DEBUG:
                self._style._fmt = MyFormatter.dbg_fmt

            elif record.levelno == logging.INFO:
                self._style._fmt = MyFormatter.info_fmt

            elif record.levelno == logging.WARNING:
                self._style._fmt = MyFormatter.warn_fmt

            elif record.levelno == logging.ERROR:
                self._style._fmt = MyFormatter.err_fmt
        else:
            self._style._fmt = MyFormatter.file_fmt
        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result


# Format for terminal
term_fmt = MyFormatter(to_file=False)
hdlr = logging.StreamHandler(sys.stdout)
hdlr.setFormatter(term_fmt)

# make sure that the folder for log exists
if not os.path.exists(LOG_FILE_PATH):
    os.makedirs(LOG_FILE_PATH)

# Format for log file
file_fmt = MyFormatter(to_file=True)
fh = RotatingFileHandler(LOG_FILE_PATH+LOG_FILE_NAME, mode='a',
                         maxBytes=1*1024*1024, backupCount=1, encoding=None, delay=0)
fh.setFormatter(file_fmt)

logging.root.addHandler(hdlr)
logging.root.addHandler(fh)
logging.root.setLevel(logging.DEBUG)


class Configs():
    """
    Select configuration based on arguments and config file

    Returns:
        dict: Settings dictionary
    """

    def __init__(self, args):
        c_monitor = 0
        c_plugin = DEFAULT_PLUGIN
        c_light = c_file = c_plugin = c_ncolor = c_iconsdark = c_iconslight = c_pywal = c_pywal_light = c_light_blend_multiplier = c_dark_blend_multiplier = c_on_change_hook = c_sierra_breeze_buttons_color = c_konsole_profile = c_titlebar_opacity = c_toolbar_opacity = c_konsole_opacity = c_color = None
        config = configparser.ConfigParser()
        if os.path.exists(USER_CONFIG_PATH+CONFIG_FILE):
            try:
                config.read(USER_CONFIG_PATH+CONFIG_FILE)
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
            c_light_blend_multiplier = clip(args.lbmultiplier, 0, 4, 1)
        elif c_light_blend_multiplier != None:
            c_light_blend_multiplier = clip(c_light_blend_multiplier, 0, 4, 1)

        if args.dbmultiplier != None:
            c_dark_blend_multiplier = clip(args.dbmultiplier, 0, 4, 1)
        elif c_dark_blend_multiplier != None:
            c_dark_blend_multiplier = clip(c_dark_blend_multiplier, 0, 4, 1)

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


def get_wallpaper_data(plugin=DEFAULT_PLUGIN, monitor=0, file=None, color=None):
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
        plugin = DEFAULT_PLUGIN
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
        if validate_color(color):
            return ("color", color)
        else:
            logging.error(f'Error: Color format "{color}" is incorrect')
    else:
        # special case for picture of the day plugin that requires a
        # directory, provider and a category
        if plugin == PICTURE_OF_DAY_PLUGIN:
            # wait a bit to for wallpaper update
            script = """
            var Desktops = desktops();
                d = Desktops[%s];
                d.wallpaperPlugin = "%s";
                d.currentConfigGroup = Array("Wallpaper", "%s", "General");
                print(d.readConfig("Provider")+","+d.readConfig("Category"));
            """

            try:
                script_output = tuple(evaluate_script(
                    script, monitor, plugin).split(","))
            except:
                script_output = ('', '')
            img_provider = script_output[0]
            provider_category = script_output[1]

            if img_provider:
                potd = PICTURE_OF_DAY_PLUGIN_IMGS_DIR+img_provider
            else:
                # default provider is astronomic picture of the day
                potd = PICTURE_OF_DAY_PLUGIN_IMGS_DIR+PICTURE_OF_DAY_DEFAULT_PROVIDER

            # unsplash also has a category
            if img_provider == PICTURE_OF_DAY_UNSPLASH_PROVIDER:
                # defaul category doesnt doesnt return id, add it
                if not provider_category:
                    provider_category = PICTURE_OF_DAY_UNSPLASH_DEFAULT_CATEGORY
                potd = f"{potd}:{provider_category}"

            # Bing file now has the wallpaper resolution in the name
            if img_provider == PICTURE_OF_DAY_BING_PROVIDER:
                # find and return files that start with bing and don't end with json and use the biggest one
                potd = [file for file in os.listdir(PICTURE_OF_DAY_PLUGIN_IMGS_DIR) if os.path.isfile(os.path.join(
                    PICTURE_OF_DAY_PLUGIN_IMGS_DIR, file)) if file.startswith(PICTURE_OF_DAY_BING_PROVIDER) and not file.endswith('json')]
                potd = PICTURE_OF_DAY_PLUGIN_IMGS_DIR+max(potd)

            if os.path.exists(potd):
                return ("image", potd)
            else:
                return None
        elif plugin == PLAIN_COLOR_PLUGIN:
            script = """
            var Desktops = desktops();
                d = Desktops[%s];
                d.wallpaperPlugin = "%s";
                d.currentConfigGroup = Array("Wallpaper", "%s", "General");
                print(d.readConfig("Color"));
            """
            try:
                color_rgb = tuple(
                    (evaluate_script(script, monitor, plugin)).split(","))
                return ("color", rgb2hex(int(r=color_rgb[0]), g=int(color_rgb[1]), b=int(color_rgb[2])))
            except:
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
            try:
                wallpaper = evaluate_script(script, monitor, plugin)
                return ("image", wallpaper)
            except:
                return None


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
        exit(1)


def get_last_modification(file):
    """get time of last modification of passed file

    Args:
        file (str): absolute path of file
    """
    if file is not None:
        if os.path.exists(file):
            return os.stat(file).st_mtime
        else:
            return None
    else:
        return None


def get_material_you_colors(wallpaper_data, ncolor, source_type):
    """ Get material you colors from wallpaper or hex color using material-color-utility

    Args:
        wallpaper_data (tuple): wallpaper (type and data)
        ncolor (int): Alternative color number flag passed to material-color-utility
        source_type (str): image or color string passed to material-color-utility

    Returns:
        str: string data from material-color-utility
    """

    try:
        seedColor = 0
        if source_type == "image":
            # open image file
            img = Image.open(wallpaper_data)
            # resize image proportionally
            basewidth = 64
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            # get best colors
            source_colors = sourceColorsFromImage(img, top=False)
            # close image file
            img.close()
            seed_color = source_colors[0]
        else:
            seed_color = argbFromHex(wallpaper_data)
            source_colors = [seed_color]

        # best colors
        best_colors = {}
        for i, color in enumerate(source_colors):
            best_colors.update({str(i): hexFromArgb(color)})
        # generate theme from seed color
        theme = themeFromSourceColor(seed_color)

        # Given a image, the alt color and hex color
        # return a selected color or a single color for hex code
        totalColors = len(best_colors)
        if ncolor and ncolor != None:
            ncolor = ncolor
        else:
            ncolor = 0

        if totalColors > ncolor:
            seedColor = hexFromArgb(source_colors[ncolor])
            seedNo = ncolor
        else:
            seedColor = hexFromArgb(source_colors[-1])
            seedNo = totalColors-1
        if seedColor != 0:
            theme = themeFromSourceColor(argbFromHex(seedColor))

        dark_scheme = json.loads(theme['schemes']['dark'].toJSON())
        light_scheme = json.loads(theme['schemes']['light'].toJSON())
        primary_palete = theme['palettes']['primary']
        secondary_palete = theme['palettes']['secondary']
        tertiary_palete = theme['palettes']['tertiary']
        neutral_palete = theme['palettes']['neutral']
        neutral_variant_palete = theme['palettes']['neutralVariant']
        error_palette = theme['palettes']['error']
        custom_colors = theme['customColors']

        materialYouColors = {
            'best': best_colors,
            'seed': {
                seedNo: hexFromArgb(theme['source']),
            },
            'schemes': {
                'light': dict_to_rgb(light_scheme),
                'dark': dict_to_rgb(dark_scheme),
            },
            'palettes': {
                'primary': dict_to_rgb(tones_from_palette(primary_palete)),
                'secondary': dict_to_rgb(tones_from_palette(secondary_palete)),
                'tertiary': dict_to_rgb(tones_from_palette(tertiary_palete)),
                'neutral': dict_to_rgb(tones_from_palette(neutral_palete)),
                'neutralVariant': dict_to_rgb(tones_from_palette(neutral_variant_palete)),
                'error': dict_to_rgb(tones_from_palette(error_palette)),
            },
            'custom': [
                get_custom_colors(custom_colors)
            ]
        }
        return materialYouColors

    except Exception as e:
        logging.error(
            f'Error trying to get colors from {wallpaper_data}:\n{e}')
        return None


def get_color_schemes(wallpaper, ncolor=None):
    """ Display best colors, allow to select alternative color,
    and make and apply color schemes for dark and light mode

    Args:
        wallpaper (tuple): wallpaper (type and data)
        light (bool): wether use or not light scheme
        ncolor (int): Alternative color number flag passed to material-color-utility
    """
    if wallpaper != None:
        materialYouColors = None
        wallpaper_type = wallpaper[0]
        wallpaper_data = wallpaper[1]
        if wallpaper_type == "image":
            source_type = "image"
            if os.path.exists(wallpaper_data):
                if not os.path.isdir(wallpaper_data):
                    # get colors from material-color-utility
                    materialYouColors = get_material_you_colors(
                        wallpaper_data, ncolor=ncolor, source_type=source_type)
                else:
                    logging.warning(
                        f'"{wallpaper_data}" is a directory, aborting')

        elif wallpaper_type == "color":
            source_type = "color"
            wallpaper_data = color2hex(wallpaper_data)
            materialYouColors = get_material_you_colors(
                wallpaper_data, ncolor=ncolor, source_type=source_type)

        if materialYouColors != None:
            try:
                if len(materialYouColors['best']) > 1:
                    best_colors = f'Best colors:'

                    for index, col in materialYouColors['best'].items():
                        if USER_HAS_COLR:
                            best_colors += f' {BOLD_RESET}{index}:{color(col,fore=col)}'
                        else:
                            best_colors += f' {BOLD_RESET}{index}:{COLOR_INFO}{col}'
                    logging.info(best_colors)

                seed = materialYouColors['seed']
                sedColor = list(seed.values())[0]
                seedNo = list(seed.keys())[0]
                if USER_HAS_COLR:
                    logging.info(
                        f'Using seed: {BOLD_RESET}{seedNo}:{color(sedColor, fore=sedColor)}')
                else:
                    logging.info(
                        f'{BOLD}Using seed: {BOLD_RESET}{seedNo}:{COLOR_INFO}{sedColor}')

                return materialYouColors

            except Exception as e:
                logging.error(f'Error:\n{e}')
                return None

    else:
        logging.error(
            f'''Error: Couldn't set schemes with "{wallpaper_data}"''')
        return None


def set_icons(icons_light, icons_dark, light=False):
    """ Set icon theme with plasma-changeicons for light and dark schemes

    Args:
        icons_light (str): Light mode icon theme
        icons_dark (str): Dark mode icon theme
        light (bool): wether using light or dark mode
    """
    if light and icons_light != None:
        icons = icons_light
    elif not light and icons_dark != None:
        icons = icons_dark
    else:
        icons = None
    if icons != None:
        changeicons_error = subprocess.check_output("/usr/lib/plasma-changeicons "+icons,
                                                    shell=True, stderr=subprocess.STDOUT, universal_newlines=True).strip()
        logging.info(f'{icons} {changeicons_error}')


def make_plasma_scheme(schemes=None):
    # Make sure the schemes path exists
    if not os.path.exists(USER_SCHEMES_PATH):
        os.makedirs(USER_SCHEMES_PATH)
    light_scheme = schemes.get_light_scheme()
    dark_scheme = schemes.get_dark_scheme()
    # plasma-apply-colorscheme doesnt allow to apply the same theme twice to reload
    # since I don't know how to reaload it with code lets make a copy and switch between them
    # sadly color settings will show copies too

    with open(THEME_LIGHT_PATH+"2.colors", 'w', encoding='utf8') as light_scheme_file:
        light_scheme_file.write(light_scheme)
    with open(THEME_LIGHT_PATH+".colors", 'w', encoding='utf8') as light_scheme_file:
        light_scheme_file.write(light_scheme)
    with open(THEME_DARK_PATH+"2.colors", 'w', encoding='utf8') as dark_scheme_file:
        dark_scheme_file.write(dark_scheme)
    with open(THEME_DARK_PATH+".colors", 'w', encoding='utf8') as dark_scheme_file:
        dark_scheme_file.write(dark_scheme)


def apply_color_schemes(light=False):
    if light == None:
        light = False
    if light != None:
        if light == True:
            color_scheme = THEME_LIGHT_PATH
        elif light == False:
            color_scheme = THEME_DARK_PATH
        kwin_blend_changes()
        subprocess.run("plasma-apply-colorscheme "+color_scheme+"2.colors",
                       shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        colorscheme_out = subprocess.check_output("plasma-apply-colorscheme "+color_scheme+".colors",
                                                  shell=True, stderr=subprocess.PIPE, universal_newlines=True).strip()
        logging.info(colorscheme_out)


def apply_pywal_schemes(light=None, pywal_light=None, use_pywal=False, schemes=None):
    pywal_colors = None
    if pywal_light != None:
        if pywal_light == True:
            pywal_colors = schemes.get_wal_light_scheme()
        else:
            pywal_light = False
            pywal_colors = schemes.get_wal_dark_scheme()
    elif light != None:
        if light == True:
            pywal_colors = schemes.get_wal_light_scheme()
        elif light == False:
            pywal_colors = schemes.get_wal_dark_scheme()
    else:
        pywal_colors = schemes.get_wal_dark_scheme()
    if pywal_colors != None:
        if use_pywal != None and use_pywal == True:
            if USER_HAS_PYWAL:
                # On very rare occassions pywal will hang, add a timeout to it
                timeout_set(3)
                try:
                    # Apply the palette to all open terminals.
                    # Second argument is a boolean for VTE terminals.
                    # Set it to true if the terminal you're using is
                    # VTE based. (xfce4-terminal, termite, gnome-terminal.)
                    pywal.sequences.send(pywal_colors, vte_fix=False)
                    # Export all template files.
                    pywal.export.every(pywal_colors)
                    # Reload xrdb, i3 and polybar.
                    pywal.reload.env()
                except Exception as e:
                    pass
                finally:
                    timeout_reset()
            else:
                logging.warning(
                    "pywal option enabled but python module is not installed")
        # print palette
        print_color_palette(pywal_colors)


def kde_globals_light():
    kdeglobals = configparser.ConfigParser()
    if os.path.exists(KDE_GLOBALS):
        try:
            kdeglobals.read(KDE_GLOBALS)
            if 'General' in kdeglobals:
                general = kdeglobals['General']
                if 'ColorScheme' in general:
                    if "MaterialYouDark" in general['ColorScheme']:
                        return False
                    elif "MaterialYouLight" in general['ColorScheme']:
                        return True
            else:
                return None
        except Exception as e:
            logging.error(f"Error:\n{e}")
            return None
    else:
        return None


def run_hook(hook):
    if hook != None:
        subprocess.Popen(hook, shell=True)


def clip(number, min, max, fallback):
    if number != None:
        return min if number < min else max if number > max else number
    else:
        return fallback


def kwin_reload():
    logging.info(f"Reloading KWin...")
    subprocess.Popen("qdbus org.kde.KWin /KWin reconfigure", shell=True,
                     stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


def sierra_breeze_button_colors(schemes, light=None):
    if light == True:
        colors = schemes.get_sierra_breeze_light_colors()
    elif light == False:
        colors = schemes.get_sierra_breeze_dark_colors()

    breezerc = configparser.ConfigParser()
    # preserve case
    breezerc.optionxform = str
    if os.path.exists(BREEZE_RC):
        try:
            breezerc.read(BREEZE_RC)
            if 'Windeco' in breezerc:
                breezerc['Windeco']['ButtonCloseActiveColor'] = colors['btn_close_active_color']
                breezerc['Windeco']['ButtonMaximizeActiveColor'] = colors['btn_maximize_active_color']
                breezerc['Windeco']['ButtonMinimizeActiveColor'] = colors['btn_minimize_active_color']
                breezerc['Windeco']['ButtonKeepAboveActiveColor'] = colors['btn_keep_above_active_color']
                breezerc['Windeco']['ButtonKeepBelowActiveColor'] = colors['btn_keep_below_active_color']
                breezerc['Windeco']['ButtonOnAllDesktopsActiveColor'] = colors['btn_on_all_desktops_active_color']
                breezerc['Windeco']['ButtonShadeActiveColor'] = colors['btn_shade_active_color']

                # Inactive
                breezerc['Windeco']['ButtonCloseInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonMaximizeInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonMinimizeInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonKeepAboveInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonKeepBelowInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonOnAllDesktopsInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonShadeInactiveColor'] = colors['btn_inactive_color']
                reload = True
            else:
                reload = False
            if reload == True:
                logging.info(f"Applying SierraBreeze window button colors")
                with open(BREEZE_RC, 'w') as configfile:
                    breezerc.write(configfile, space_around_delimiters=False)
        except Exception as e:
            logging.error(f"Error writing breeze window button colors:\n{e}")
    else:
        logging.warning(
            f"SierraBreeze config '{BREEZE_RC}' not found, skipping")


def tup2str(tup):
    return ','.join(map(str, tup))


def print_color_palette(pywal_colors):
    if USER_HAS_COLR:
        i = 0
        for index, col in pywal_colors['colors'].items():
            if i % 8 == 0:
                print()
            print(f'{color("    ",back=hex2rgb(col))}', end='')
            i += 1
        print(f'{BOLD}')
    else:
        logging.debug(
            "Install colr python module to tint color codes and palette as they update")
        # Print color palette from pywal.colors.palette
        for i in range(0, 16):
            if i % 8 == 0:
                print()

            if i > 7:
                i = "8;5;%s" % i

            print("\033[4%sm%s\033[0m" % (i, " " * (80 // 20)), end="")
        print("\n", end="")


def konsole_export_scheme(light=None, pywal_light=None, schemes=None, konsole_opacity=100):
    if konsole_opacity == None:
        konsole_opacity = 1.0
    else:
        konsole_opacity = float(konsole_opacity/100)
    konsole_opacity = clip(konsole_opacity, 0.0, 1.0, 1.0)
    # print(f"konsole_opacity: {konsole_opacity}")
    if pywal_light != None:
        if pywal_light == True:
            pywal_colors = schemes.get_wal_light_scheme()
        else:
            pywal_colors = schemes.get_wal_dark_scheme()
    elif light != None:
        if light == True:
            pywal_colors = schemes.get_wal_light_scheme()
        elif light == False:
            pywal_colors = schemes.get_wal_dark_scheme()
    else:
        pywal_colors = schemes.get_wal_dark_scheme()
    config = configparser.ConfigParser()
    config.optionxform = str
    if os.path.exists(KONSOLE_COLOR_SCHEME_PATH):
        config.read(KONSOLE_COLOR_SCHEME_PATH)

    sections = ['Background',
                'BackgroundIntense',
                'BackgroundFaint',
                'Color',
                'Foreground',
                'ForegroundIntense',
                'ForegroundFaint',
                'General']
    exp = []
    for section in sections:
        if section == 'Color':
            for n in range(8):
                exp.append(str(f'Color{n}'))
                exp.append(str(f'Color{n}Intense'))
                exp.append(str(f'Color{n}Faint'))
        else:
            exp.append(section)

    for section in exp:
        if not config.has_section(section):
            config.add_section(section)
    config['Background']['Color'] = tup2str(
        hex2rgb(pywal_colors['special']['background']))
    config['BackgroundIntense']['Color'] = tup2str(
        hex2rgb(pywal_colors['special']['backgroundIntense']))
    config['BackgroundFaint']['Color'] = tup2str(
        hex2rgb(pywal_colors['special']['backgroundFaint']))
    config['Color0']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color0']))
    config['Color1']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color1']))
    config['Color2']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color2']))
    config['Color3']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color3']))
    config['Color4']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color4']))
    config['Color5']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color5']))
    config['Color6']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color6']))
    config['Color7']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color7']))

    config['Color0Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color8']))
    config['Color1Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color9']))
    config['Color2Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color10']))
    config['Color3Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color11']))
    config['Color4Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color12']))
    config['Color5Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color13']))
    config['Color6Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color14']))
    config['Color7Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color15']))

    config['Color0Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color16']))
    config['Color1Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color17']))
    config['Color2Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color18']))
    config['Color3Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color19']))
    config['Color4Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color20']))
    config['Color5Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color21']))
    config['Color6Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color22']))
    config['Color7Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color23']))

    config['Foreground']['Color'] = tup2str(
        hex2rgb(pywal_colors['special']['foreground']))
    config['ForegroundIntense']['Color'] = tup2str(
        hex2rgb(pywal_colors['special']['foregroundIntense']))
    config['ForegroundFaint']['Color'] = tup2str(
        hex2rgb(pywal_colors['special']['foregroundFaint']))

    config['General']['Description'] = "MaterialYou"
    config['General']['Opacity'] = str(konsole_opacity)

    with open(KONSOLE_COLOR_SCHEME_PATH, 'w') as configfile:
        config.write(configfile, space_around_delimiters=False)

    config['General']['Description'] = "MaterialYouAlt"

    with open(KONSOLE_COLOR_SCHEME_ALT_PATH, 'w') as configfile:
        config.write(configfile, space_around_delimiters=False)


def make_konsole_mirror_profile(profile=None):
    if profile != None:
        profile_path = KONSOLE_DIR+profile+".profile"
        if os.path.exists(profile_path):
            logging.debug(f"konsole: mirror profile ({profile})")
            subprocess.check_output(
                "cp -f '"+profile_path+"' "+KONSOLE_TEMP_PROFILE, shell=True)
            profile = configparser.ConfigParser()
            # preserve case
            profile.optionxform = str
            if os.path.exists(profile_path):
                try:
                    profile.read(profile_path)
                    if 'Appearance' in profile:
                        if profile['Appearance']['ColorScheme'] != "MaterialYou":
                            profile['Appearance']['ColorScheme'] = "MaterialYou"
                            with open(profile_path, 'w') as configfile:
                                profile.write(
                                    configfile, space_around_delimiters=False)
                except Exception as e:
                    logging.error(f"Error applying Konsole profile:\n{e}")

            # Mirror profile
            profile = configparser.ConfigParser()
            profile.optionxform = str
            if os.path.exists(KONSOLE_TEMP_PROFILE):
                try:
                    profile.read(KONSOLE_TEMP_PROFILE)
                    if 'Appearance' in profile:
                        profile['Appearance']['ColorScheme'] = "MaterialYouAlt"
                        profile['General']['Name'] = "TempMyou"
                except Exception as e:
                    logging.error(f"Error applying Konsole profile:\n{e}")
                with open(KONSOLE_TEMP_PROFILE, 'w') as configfile:
                    profile.write(configfile, space_around_delimiters=False)


def konsole_reload_profile(profile=None):
    if profile != None:
        logging.info(f"konsole: reload profile ({profile})")
        konsole_dbus_services = subprocess.check_output(
            "qdbus org.kde.konsole*", shell=True, universal_newlines=True).strip().splitlines()
        if konsole_dbus_services:
            for service in konsole_dbus_services:
                try:
                    konsole_sessions = subprocess.check_output(
                        "qdbus "+service+" | grep 'Sessions/'", shell=True, universal_newlines=True).strip().splitlines()
                    for session in konsole_sessions:
                        #print(f"service: {service} -> {session}")
                        current_profile = subprocess.check_output(
                            "qdbus "+service+" "+session+" org.kde.konsole.Session.profile", shell=True, universal_newlines=True).strip()
                        # print(current_profile)
                        if current_profile == profile:
                            subprocess.check_output(
                                "qdbus "+service+" "+session+" org.kde.konsole.Session.setProfile 'TempMyou'", shell=True)
                        else:
                            subprocess.check_output(
                                "qdbus "+service+" "+session+" org.kde.konsole.Session.setProfile 'TempMyou'", shell=True)
                            subprocess.check_output(
                                "qdbus "+service+" "+session+" org.kde.konsole.Session.setProfile '"+profile + "'", shell=True)
                except:
                    pass


def konsole_apply_color_scheme(light=None, pywal_light=None, schemes=None, profile=None, konsole_opacity=None):
    if profile != None:
        profile_path = KONSOLE_DIR+profile+".profile"
        if os.path.exists(profile_path):
            konsole_export_scheme(light, pywal_light, schemes, konsole_opacity)
            konsole_reload_profile(profile)
        else:
            logging.error(f"Konsole Profile: {profile_path} does not exist")


# Current function name from https://stackoverflow.com/a/31615605
# for current func name, specify 0 or no argument.
# for name of caller of current func, specify 1.
# for name of caller of caller of current func, specify 2. etc.
def currentFuncName(n=0): return sys._getframe(n + 1).f_code.co_name

# Register a timeout handler


def timeout_handler(signum, frame):
    logging.error(
        f"{currentFuncName(1)}: took too much time, aborted, reboot if the problem persists")
    raise TimeoutError


def timeout_set(time_s=3):
    # Register the signal handler
    signal.signal(signal.SIGALRM, timeout_handler)
    # Define a timeout for the function
    signal.alarm(time_s)


def timeout_reset():
    signal.alarm(0)


def kill_existing():
    get_pids = subprocess.check_output("ps -e -f | grep [/]usr/bin/kde-material-you-colors | awk '{print $2}'",
                                       shell=True, stderr=subprocess.PIPE, universal_newlines=True).strip().splitlines()
    current_pid = os.getpid()
    for pid in get_pids:
        pid = int(pid)
        if pid != current_pid:
            logging.debug(
                f"Found existing process with PID: '{pid}' killing...")
            subprocess.Popen("kill -9 "+str(pid), shell=True)


def export_schemes(schemes):
    """Export generated schemes to MATERIAL_YOU_COLORS_JSON

    Args:
        schemes (ThemeConfig): generated color schemes
    """
    colors = schemes.get_material_schemes()
    colors.update({
        "extras": schemes.get_extras(),
        "pywal": {
            "light": schemes.get_wal_light_scheme(),
            "dark": schemes.get_wal_dark_scheme()
        }
    })

    with open(MATERIAL_YOU_COLORS_JSON, 'w', encoding='utf8') as material_you_colors:
        json.dump(colors, material_you_colors, indent=4, ensure_ascii=False)


def kwin_blend_changes():
    try:
        bus = dbus.SessionBus()
        kwin = dbus.Interface(bus.get_object(
            'org.kde.KWin', '/org/kde/KWin/BlendChanges'), dbus_interface='org.kde.KWin.BlendChanges')
        kwin.start()
    except Exception as e:
        logging.warning(
            f'Could not start blend effect (requires Plasma 5.25 or later):\n{e}')
        return None


def titlebar_opacity(opacity):
    if opacity != None:
        opacity = clip(opacity, 0, 100, 100)
        conf_file = configparser.ConfigParser()
        # preserve case
        conf_file.optionxform = str

        if os.path.exists(SBE_RC):
            try:
                conf_file.read(SBE_RC)
                if 'Windeco' in conf_file:
                    conf_file['Windeco']['BackgroundOpacity'] = str(
                        int(opacity))
                    reload = True
                else:
                    reload = False
                if reload == True:
                    logging.info(
                        f"Applying SierraBreezeEnhanced titlebar opacity")
                    with open(SBE_RC, 'w') as configfile:
                        conf_file.write(
                            configfile, space_around_delimiters=False)
            except Exception as e:
                logging.error(
                    f"Error writing SierraBreezeEnhanced titlebar opacity:\n{e}")

        if os.path.exists(KLASSY_RC):
            try:
                conf_file.read(KLASSY_RC)
                if 'Common' in conf_file:
                    conf_file['Common']['ActiveTitlebarOpacity'] = str(
                        int(opacity))
                    conf_file['Common']['InactiveTitlebarOpacity'] = str(
                        int(opacity))
                    reload = True
                else:
                    reload = False
                if reload == True:
                    logging.info(f"Applying Klassy titlebar opacity")
                    with open(KLASSY_RC, 'w') as configfile:
                        conf_file.write(
                            configfile, space_around_delimiters=False)
            except Exception as e:
                logging.error(f"Error writing Klassy titlebar opacity:\n{e}")


def dict_to_rgb(dark_scheme):
    out = {}
    for key, color in dark_scheme.items():
        out.update({key: hexFromArgb(color)})
    return out


def tones_from_palette(palette):
    tones = {}
    for x in range(100):
        tones.update({x: palette.tone(x)})
    return tones


def get_custom_colors(custom_colors):
    colors = {}
    for custom_color in custom_colors:
        value = hexFromArgb(custom_color['color']['value'])
        colors.update(
            {
                value: {
                    'color': dict_to_rgb(custom_color['color']),
                    'value': hexFromArgb(custom_color['value']),
                    'light': dict_to_rgb(custom_color['light']),
                    'dark': dict_to_rgb(custom_color['dark']),
                }
            },
        )
    return colors


def one_shot_actions(args):
    # User may just want to set the startup script / default config, do that only and terminate the script
    if args.autostart == True:
        if not os.path.exists(USER_AUTOSTART_SCRIPT_PATH):
            os.makedirs(USER_AUTOSTART_SCRIPT_PATH)
        if not os.path.exists(USER_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT):
            try:
                subprocess.check_output("cp "+SAMPLE_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT+" "+USER_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT,
                                        shell=True)
                logging.info(
                    f"Autostart script copied to: {USER_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT}")
            except Exception:
                quit(1)
        else:
            logging.error(
                f"Autostart script already exists in: {USER_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT}")
        quit(0)
    elif args.copyconfig == True:
        if not os.path.exists(USER_CONFIG_PATH):
            os.makedirs(USER_CONFIG_PATH)
        if not os.path.exists(USER_CONFIG_PATH+CONFIG_FILE):
            try:
                subprocess.check_output("cp "+SAMPLE_CONFIG_PATH+SAMPLE_CONFIG_FILE+" "+USER_CONFIG_PATH+CONFIG_FILE,
                                        shell=True)
                logging.info(
                    f"Config copied to: {USER_CONFIG_PATH+CONFIG_FILE}")
            except Exception:
                quit(1)
        else:
            logging.error(
                f"Config already exists in: {USER_CONFIG_PATH+CONFIG_FILE}")
        quit(0)
    elif args.stop == True:
        kill_existing()
        quit(0)


def get_config_value(config, config_name: str):
    if config != None:
        if config_name in config:
            return config[config_name]


class Watcher:
    """ A simple class to watch variable changes."""

    def __init__(self, value: any):
        self.value = value
        self.has_changed = False
        self.old_value = None

    def set_value(self, new_value: any) -> None:
        if self.value != new_value:
            self.old_value = self.value
            self.value = new_value
            self.has_changed = True
        else:
            self.has_changed = False

    def has_changed(self):
        return self.has_changed

    def get_old_value(self):
        return self.old_value

    def get_new_value(self):
        return self.value


def apply_themes(
        config_watcher: Watcher,
        wallpaper_watcher: Watcher,
        wallpaper_modified: Watcher,
        group1_watcher: Watcher,
        light_mode_watcher: Watcher,
        schemes_watcher: Watcher,
        material_colors: Watcher,
        first_run_watcher: Watcher,
        konsole_profile_modified: Watcher,
        plasma_scheme_watcher: Watcher):
    # Print new config after change
    if config_watcher.has_changed:
        logging.debug(f"Config: {config_watcher.get_new_value()}")
    needs_kwin_reload = False
    group1_watcher.set_value([
        get_config_value(config_watcher.get_new_value(), 'ncolor'),
        get_config_value(config_watcher.get_new_value(), 'lbm'),
        get_config_value(config_watcher.get_new_value(), 'dbm'),
    ])

    light_mode_watcher.set_value(get_config_value(
        config_watcher.get_new_value(), 'light'))

    # Get wallpaper type and data
    if wallpaper_watcher.get_new_value() != None and wallpaper_watcher.get_new_value()[1] != None:
        wallpaper_new_type = wallpaper_watcher.get_new_value()[0]
        wallpaper_new_data = wallpaper_watcher.get_new_value()[1]
    # if wallpaper is image save time of last modification
    if wallpaper_new_type == "image":
        wallpaper_modified.set_value(
            get_last_modification(wallpaper_new_data))
    else:
        wallpaper_modified.set_value(None)

    if config_watcher.get_new_value()['konsole_profile'] != None:
        konsole_profile_modified.set_value(get_last_modification(
            KONSOLE_DIR+config_watcher.get_new_value()['konsole_profile']+".profile"))

    # decide light or dark
    dark_light = False
    if light_mode_watcher.get_new_value() == None:
        if plasma_scheme_watcher.get_new_value() != None:
            dark_light = plasma_scheme_watcher.get_new_value()
    else:
        dark_light = light_mode_watcher.get_new_value()

    if wallpaper_watcher.has_changed or group1_watcher.has_changed or wallpaper_modified.has_changed:
        if wallpaper_watcher.has_changed:
            logging.info(
                f'Using source ({wallpaper_new_type}): {wallpaper_new_data}')
        material_colors.set_value(
            get_color_schemes(
                wallpaper_watcher.get_new_value(),
                config_watcher.get_new_value()['ncolor'])
        )
        if material_colors.get_new_value() != None:
            # Genrate color schemes from MYou colors
            schemes_watcher.set_value(ThemeConfig(
                material_colors.get_new_value(),
                wallpaper_new_data,
                config_watcher.get_new_value()['lbm'],
                config_watcher.get_new_value()['dbm'],
                config_watcher.get_new_value()['toolbar_opacity']))
            # Export generated schemes to output file
            export_schemes(schemes_watcher.get_new_value())
            # Make plasma color schemes
            make_plasma_scheme(schemes_watcher.get_new_value())
            # Apply plasma color schemes
            apply_color_schemes(dark_light)
            # Export and apply color scheme to konsole profile
            if config_watcher.get_new_value()['konsole_profile'] != None:
                konsole_apply_color_scheme(
                    dark_light,
                    config_watcher.get_new_value()['pywal_light'],
                    schemes_watcher.get_new_value(),
                    config_watcher.get_new_value()['konsole_profile'],
                    konsole_opacity=config_watcher.get_new_value()[
                        'konsole_opacity']
                )

            set_icons(
                config_watcher.get_new_value()['iconslight'],
                config_watcher.get_new_value()['iconsdark'],
                light_mode_watcher.get_new_value())

            if config_watcher.get_new_value()['sierra_breeze_buttons_color'] == True:
                needs_kwin_reload = True
                sierra_breeze_button_colors(
                    schemes_watcher.get_new_value(),
                    light_mode_watcher.get_new_value())

            if first_run_watcher.get_new_value() == True:
                if config_watcher.get_new_value()['titlebar_opacity'] != None:
                    needs_kwin_reload = True
                    titlebar_opacity(
                        config_watcher.get_new_value()['titlebar_opacity'])
            if needs_kwin_reload == True:
                kwin_reload()
                needs_kwin_reload == False
            # Apply pywal color scheme with MYou colors
            if config_watcher.get_new_value()['pywal'] == True:
                apply_pywal_schemes(
                    dark_light,
                    use_pywal=config_watcher.get_new_value()['pywal'],
                    pywal_light=config_watcher.get_new_value()['pywal_light'],
                    schemes=schemes_watcher.get_new_value())
            print("---------------------")
            run_hook(config_watcher.get_new_value()['on_change_hook'])

    if first_run_watcher.get_new_value() == False:
        if light_mode_watcher.has_changed or plasma_scheme_watcher.has_changed and plasma_scheme_watcher.get_old_value() != None and light_mode_watcher.get_new_value() != plasma_scheme_watcher.get_new_value():

            # Apply plasma color schemes
            apply_color_schemes(dark_light)
            # Export and apply color scheme to konsole profile
            konsole_apply_color_scheme(
                dark_light,
                config_watcher.get_new_value()['pywal_light'],
                schemes_watcher.get_new_value(),
                config_watcher.get_new_value()['konsole_profile'],
                konsole_opacity=config_watcher.get_new_value()[
                    'konsole_opacity']
            )
            set_icons(
                config_watcher.get_new_value()['iconslight'],
                config_watcher.get_new_value()['iconsdark'],
                light_mode_watcher.get_new_value())
            if config_watcher.get_new_value()['pywal'] == True:
                if config_watcher.get_new_value()['pywal_light'] == None:
                    apply_pywal_schemes(
                        dark_light,
                        use_pywal=config_watcher.get_new_value()['pywal'],
                        pywal_light=config_watcher.get_new_value()[
                            'pywal_light'],
                        schemes=schemes_watcher.get_new_value())
            print("---------------------")

    if konsole_profile_modified.has_changed and konsole_profile_modified.get_old_value() != None:
        make_konsole_mirror_profile(
            config_watcher.get_new_value()['konsole_profile'])

    if config_watcher.has_changed and config_watcher.get_old_value() != None:
        icons_new = [
            get_config_value(config_watcher.get_new_value(), 'iconslight'),
            get_config_value(config_watcher.get_new_value(), 'iconsdark')
        ]
        icons_old = [
            get_config_value(config_watcher.get_old_value(), 'iconslight'),
            get_config_value(config_watcher.get_old_value(), 'iconsdark')
        ]

        if icons_new != icons_old:
            set_icons(icons_new[0], icons_new[1])

        if get_config_value(config_watcher.get_new_value(), 'pywal') != get_config_value(config_watcher.get_old_value(), 'pywal') and get_config_value(config_watcher.get_new_value(), 'pywal') != None:
            if config_watcher.get_new_value()['pywal'] == True:
                apply_pywal_schemes(
                    dark_light,
                    use_pywal=config_watcher.get_new_value()['pywal'],
                    pywal_light=config_watcher.get_new_value()['pywal_light'],
                    schemes=schemes_watcher.get_new_value())

        if get_config_value(config_watcher.get_new_value(), 'pywal_light') != get_config_value(config_watcher.get_old_value(), 'pywal_light'):
            konsole_apply_color_scheme(
                dark_light,
                config_watcher.get_new_value()['pywal_light'],
                schemes_watcher.get_new_value(),
                config_watcher.get_new_value()['konsole_profile'],
                konsole_opacity=config_watcher.get_new_value()[
                    'konsole_opacity']
            )
            if config_watcher.get_new_value()['pywal'] == True:
                apply_pywal_schemes(
                    dark_light,
                    use_pywal=config_watcher.get_new_value()['pywal'],
                    pywal_light=config_watcher.get_new_value()['pywal_light'],
                    schemes=schemes_watcher.get_new_value())

        if get_config_value(config_watcher.get_new_value(), 'konsole_opacity') != get_config_value(config_watcher.get_old_value(), 'konsole_opacity') or get_config_value(config_watcher.get_new_value(), 'konsole_profile') != get_config_value(config_watcher.get_old_value(), 'konsole_profile'):
            if config_watcher.get_new_value()['konsole_opacity'] != None:
                konsole_apply_color_scheme(
                    dark_light,
                    config_watcher.get_new_value()['pywal_light'],
                    schemes_watcher.get_new_value(),
                    config_watcher.get_new_value()['konsole_profile'],
                    konsole_opacity=config_watcher.get_new_value()[
                        'konsole_opacity']
                )
        if get_config_value(config_watcher.get_new_value(), 'titlebar_opacity') != get_config_value(config_watcher.get_old_value(), 'titlebar_opacity'):
            if get_config_value(config_watcher.get_new_value(), 'titlebar_opacity') != None:
                needs_kwin_reload = True
                titlebar_opacity(
                    config_watcher.get_new_value()['titlebar_opacity'])

        if get_config_value(config_watcher.get_new_value(), 'toolbar_opacity') != get_config_value(config_watcher.get_old_value(), 'toolbar_opacity'):
            if config_watcher.get_new_value()['toolbar_opacity'] != None:
                material_colors.set_value(get_color_schemes(
                    wallpaper_watcher.get_new_value(),
                    config_watcher.get_new_value()['ncolor']))
            if material_colors.get_new_value() != None:
                # Genrate color schemes from MYou colors
                schemes_watcher.set_value(ThemeConfig(
                    material_colors.get_new_value(),
                    wallpaper_new_data,
                    config_watcher.get_new_value()['lbm'],
                    config_watcher.get_new_value()['dbm'],
                    config_watcher.get_new_value()['toolbar_opacity']))
                # Export generated schemes to output file
                export_schemes(schemes_watcher.get_new_value())
                # Make plasma color schemes
                make_plasma_scheme(schemes_watcher.get_new_value())
                # Apply plasma color schemes
                apply_color_schemes(dark_light)

        if get_config_value(config_watcher.get_new_value(), 'sierra_breeze_buttons_color') != get_config_value(config_watcher.get_old_value(), 'sierra_breeze_buttons_color'):
            if config_watcher.get_new_value()['sierra_breeze_buttons_color'] == True:
                needs_kwin_reload = True
                sierra_breeze_button_colors(
                    schemes_watcher.get_new_value(),
                    light_mode_watcher.get_new_value())

        run_hook(config_watcher.get_new_value()['on_change_hook'])

        if needs_kwin_reload == True:
            kwin_reload()
            needs_kwin_reload == False
    first_run_watcher.set_value(False)


def validate_color(color):
    """check if a color is either a valid hex or rgb format

    Args:
        color (str): Hex or rgb color

    Returns:
        int: color type rgb(1) or hex(2)
        None: for invalid color
    """
    is_hex = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)
    is_rgb = re.search(
        r'^(?:(?:^|,\s*)([01]?\d\d?|2[0-4]\d|25[0-5])){3}$', color)
    if is_rgb:
        return 1
    elif is_hex:
        return 2
    else:
        return None


def color2hex(color):
    format = validate_color(color)
    if format == 1:
        r, g, b = [int(c) for c in color.split(",")]
        return rgb2hex(r, g, b)
    elif format == 2:
        return color
