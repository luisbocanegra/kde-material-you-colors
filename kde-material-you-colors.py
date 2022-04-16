import subprocess
import json
import time
import os
import dbus
import argparse
import configparser
import importlib.util
from color_scheme import ColorScheme
from pathlib import Path
from color_utils import rgb2hex
import numpy as np

USER_HAS_COLR = importlib.util.find_spec("colr") is not None
if USER_HAS_COLR:
    from colr import color

HOME = str(Path.home())
SAMPLE_CONFIG_FILE = "sample_config.conf"
CONFIG_FILE = "config.conf"
SAMPLE_CONFIG_PATH = "/usr/lib/kde-material-you-colors/"
USER_CONFIG_PATH = HOME+"/.config/kde-material-you-colors/"
USER_SCHEMES_PATH = HOME+"/.local/share/color-schemes/"
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
BOLD_TEXT = "\033[1m"
RESET_TEXT = "\033[0;0m"


def get_wallpaper_data(plugin=DEFAULT_PLUGIN, monitor=0, file=None):
    """Get current wallpaper or color from text file or plugin + containment combo
    and return a string with its type (color or image file)

    Args:
        script (str): javascript to evaluate
        monitor (int): containment (monitor) number
        plugin (str): wallpaper plugin id

    Returns:
        tuple: (type (int), data (str))
    """
    if file:
        if os.path.exists(file):
            with open(file) as file:
                wallpaper = str(file.read()).replace('file://', '').strip()
                if wallpaper:
                    return ("image",wallpaper)
                else:
                    return None
        else:
            print(f'File "{file}" does not exist')
            return None
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
                script_output = ('','')
            img_provider = script_output[0]
            provider_category = script_output[1]
            
            if img_provider:
                potd = PICTURE_OF_DAY_PLUGIN_IMGS_DIR+img_provider
            else:
                # default provider is astronomic photo of the day
                potd = PICTURE_OF_DAY_PLUGIN_IMGS_DIR+PICTURE_OF_DAY_DEFAULT_PROVIDER

            # unsplash also has a category
            if img_provider == PICTURE_OF_DAY_UNSPLASH_PROVIDER:
                # defaul category doesnt doesnt return id, add it
                if not provider_category:
                    provider_category = PICTURE_OF_DAY_UNSPLASH_DEFAULT_CATEGORY
                potd = f"{potd}:{provider_category}"
                
            if os.path.exists(potd):
                return ("image",potd)
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
                color_rgb =  tuple((evaluate_script(script, monitor, plugin)).split(","))
                r = int(color_rgb[0])
                g = int(color_rgb[1])
                b = int(color_rgb[2])
                
                return ("color",rgb2hex(r, g, b))
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
                wallpaper =  evaluate_script(script, monitor, plugin)
                return ("image",wallpaper)
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
        plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
        wallpaper_data = str(plasma.evaluateScript(
            script % (monitor, plugin, plugin))).replace('file://', '')
        return wallpaper_data
    except Exception as e:
        print(f'Error getting wallpaper from dbus:\n{e}')
        return None


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
    
def get_material_you_colors(wallpaper_data, ncolor, flag):
    """ Get material you colors from wallpaper or hex color using material-color-utility

    Args:
        wallpaper_data (tuple): wallpaper (type and data)
        ncolor (int): Alternative color number flag passed to material-color-utility
        flag (str): image or color flag passed to material-color-utility

    Returns:
        str: string data from material-color-utility
    """
    try:
        materialYouColors = subprocess.check_output("material-color-utility "+flag+" '"+wallpaper_data+"' -n "+str(ncolor),
                                                    shell=True, universal_newlines=True).strip()
        return materialYouColors
    except Exception as e:
        print(f'Error trying to get colors from {wallpaper_data}')
        return None

def set_color_schemes(wallpaper, light=None, ncolor=None, pywal=None, pywal_light=None,lbmult=1,dbmult=1):

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
            use_flag = "-i"
            if os.path.exists(wallpaper_data):
                if not os.path.isdir(wallpaper_data):
                    # get colors from material-color-utility
                    materialYouColors = get_material_you_colors(wallpaper_data,ncolor=ncolor,flag=use_flag)
                else:
                    print(f"{wallpaper_data} is a directory, aborting :)")
        
        elif wallpaper_type == "color":
            use_flag = "-c"
            materialYouColors = get_material_you_colors(wallpaper_data,ncolor=ncolor,flag=use_flag)
            
        if materialYouColors != None:
            try:
                # parse colors string to json
                colors_json = json.loads(materialYouColors)

                if wallpaper_type != "color":
                    print(f'{BOLD_TEXT}Best colors:', end=' ')
                    for index, col in colors_json['bestColors'].items():
                        if USER_HAS_COLR:
                            print(
                                f'{BOLD_TEXT}{index}:{color(col,fore=col)}', end=' ')
                        else:
                            print(f'{BOLD_TEXT}{index}:{col}', end=' ')
                    print(f'{BOLD_TEXT}')

                seed = colors_json['seedColor']
                sedColor = list(seed.values())[0]
                seedNo = list(seed.keys())[0]
                if USER_HAS_COLR:
                    print(BOLD_TEXT+"Using seed: "+seedNo +
                        ":"+color(sedColor, fore=sedColor))
                else:
                    print(BOLD_TEXT+"Using seed: " +
                        seedNo+":"+sedColor+RESET_TEXT)

                with open('/tmp/kde-material-you-colors.json', 'w', encoding='utf8') as current_scheme:
                    current_scheme.write(json.dumps(
                        colors_json, indent=4, sort_keys=False))

                # generate and apply Plasma color schemes
                #print(f'Settting color schemes for {wallpaper_data}')
                colors_schemes = ColorScheme(colors_json,lbmult,dbmult)
                colors_schemes.make_color_schemes(light=light, pywal_light=pywal_light, wallpaper=wallpaper,use_pywal=pywal)
                
            except Exception as e:
                print(f'Error:\n {e}')

    else:
        print(
            f'''Error: Couldn't set schemes with "{wallpaper_data}"''')




def set_icons(icons_light, icons_dark, light):
    """ Set icon theme with plasma-changeicons for light and dark schemes

    Args:
        icons_light (str): Light mode icon theme
        icons_dark (str): Dark mode icon theme
        light (bool): wether using light or dark mode
    """
    if light and icons_light != None:
        subprocess.run("/usr/lib/plasma-changeicons "+icons_light,
                       shell=True)
    if not light and icons_dark != None:
        subprocess.run("/usr/lib/plasma-changeicons "+icons_dark,
                       shell=True)


class Configs():
    """
    Select configuration based on arguments and config file
    
    Returns:
        dict: Settings dictionary
    """
    def __init__(self, args):
        c_light = c_monitor = c_file = c_plugin = c_ncolor = c_iconsdark = c_iconslight = c_pywal = c_pywal_light = c_light_blend_multiplier = c_dark_blend_multiplier= None 
        # User may just want to set the startup script / default config, do that only and exit
        if args.autostart == True:
            if not os.path.exists(USER_AUTOSTART_SCRIPT_PATH):
                os.makedirs(USER_AUTOSTART_SCRIPT_PATH)
            if not os.path.exists(USER_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT):
                try:
                    subprocess.check_output("cp "+SAMPLE_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT+" "+USER_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT,
                                            shell=True)
                    print(
                        f"Autostart script copied to: {USER_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT}")
                except Exception:
                    quit(1)
            else:
                print(
                    f"Autostart script already exists in: {USER_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT}")
            quit(0)
        elif args.copyconfig == True:
            if not os.path.exists(USER_CONFIG_PATH):
                os.makedirs(USER_CONFIG_PATH)
            if not os.path.exists(USER_CONFIG_PATH+CONFIG_FILE):
                try:
                    subprocess.check_output("cp "+SAMPLE_CONFIG_PATH+SAMPLE_CONFIG_FILE+" "+USER_CONFIG_PATH+CONFIG_FILE,
                                            shell=True)
                    print(f"Config copied to: {USER_CONFIG_PATH+CONFIG_FILE}")
                except Exception:
                    quit(1)
            else:
                print(
                    f"Config already exists in: {USER_CONFIG_PATH+CONFIG_FILE}")
            quit(0)
        else:
            config = configparser.ConfigParser()
            if os.path.exists(USER_CONFIG_PATH+CONFIG_FILE):
                try:
                    config.read(USER_CONFIG_PATH+CONFIG_FILE)
                    if 'CUSTOM' in config:
                        custom = config['CUSTOM']

                        if 'light' in custom:
                            c_light = custom.getboolean('light')

                        if 'file' in custom:
                            c_file = custom['file']

                        if 'monitor' in custom:
                            c_monitor = custom.getint('monitor')
                            if c_monitor < 0:
                                raise ValueError(
                                    'Config for monitor must be a positive integer')

                        if 'ncolor' in custom:
                            c_ncolor = custom.getint('ncolor')
                            if c_ncolor < 0:
                                raise ValueError(
                                    'Config for ncolor must be a positive integer')

                        if 'plugin' in custom:
                            c_plugin = custom['plugin']

                        if 'iconslight' in custom:
                            c_iconslight = custom['iconslight']

                        if 'iconsdark' in custom:
                            c_iconsdark = custom['iconsdark']
                            
                        if 'pywal' in custom:
                            c_pywal = custom.getboolean('pywal')
                        
                        if 'pywal_light' in custom:
                            c_pywal_light = custom.getboolean('pywal_light')
                            
                        if 'light_blend_multiplier' in custom:
                            c_light_blend_multiplier = custom.getfloat('light_blend_multiplier')
                            
                        if 'dark_blend_multiplier' in custom:
                            c_dark_blend_multiplier = custom.getfloat('dark_blend_multiplier')
                except Exception as e:
                    print(f"Please fix your settings file:\n {e}\n")
            if args.dark == True:
                c_light = False
            elif args.light == True:
                c_light = args.light
            else:
                c_light = c_light
                
            if args.pywal == True:
                c_pywal = args.pywal
            elif c_pywal != None:
                c_pywal = c_pywal
                
            if args.pywaldark == True:
                c_pywal_light = False
            elif args.pywallight == True:
                c_pywal_light = args.pywallight
            else:
                c_pywal_light = c_pywal_light

            if args.lbmultiplier != None:
                c_light_blend_multiplier = np.clip(args.lbmultiplier, 0, 4)
            elif c_light_blend_multiplier != None:
                c_light_blend_multiplier = np.clip(c_light_blend_multiplier, 0, 4)
                
            if args.dbmultiplier != None:
                c_dark_blend_multiplier = np.clip(args.dbmultiplier, 0, 4)
            elif c_dark_blend_multiplier != None:
                c_dark_blend_multiplier = np.clip(c_dark_blend_multiplier, 0, 4)
                
            if args.file != None:
                c_file = args.file
            elif c_file == None:
                c_file = args.file

            if args.monitor != None:
                if args.monitor < 0:
                    raise ValueError(
                        'Value for --monitor must be a positive integer')
                else:
                    c_monitor = args.monitor
            elif args.monitor == None and c_monitor == None:
                c_monitor = 0
            else:
                c_monitor = c_monitor

            if args.ncolor != None:
                if args.ncolor < 0:
                    raise ValueError(
                        'Value for --ncolor must be a positive integer')
                else:
                    c_ncolor = args.ncolor
            elif args.ncolor == None and c_ncolor == None:
                c_ncolor = 0
            else:
                c_ncolor = c_ncolor

            if args.plugin != None:
                c_plugin = args.plugin
            elif args.plugin == None and c_plugin == None:
                c_plugin = DEFAULT_PLUGIN
            else:
                c_plugin = c_plugin

            if args.iconslight != None:
                c_iconslight = args.iconslight
            elif c_iconslight == None:
                c_iconslight = args.iconslight

            if args.iconsdark != None:
                c_iconsdark = args.iconsdark
            elif c_iconsdark == None:
                c_iconsdark = args.iconsdark

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
                "dbm": c_dark_blend_multiplier
            }

    @property
    def options(self):
        return self._options


def currentWallpaper(options):
    return get_wallpaper_data(plugin=options['plugin'], monitor=options['monitor'], file=options['file'])


if __name__ == '__main__':
    # Make sure the schemes path exists
    if not os.path.exists(USER_SCHEMES_PATH):
        os.makedirs(USER_SCHEMES_PATH)
    parser = argparse.ArgumentParser(
        description='Automatic Material You Colors Generator from your wallpaper for the Plasma Desktop')
    parser.add_argument('--monitor', '-m', type=int,
                        help='Monitor to get wallpaper (default is 0) but second one is 6 in my case, play with this to find yours', default=None)
    parser.add_argument('--plugin', '-p', type=str,
                        help=f'Wallpaper plugin id (default is {DEFAULT_PLUGIN}) you can find them in: /usr/share/plasma/wallpapers/ or ~/.local/share/plasma/wallpapers', default=None)
    parser.add_argument('--file', '-f', type=str,
                        help='Text file that contains wallpaper absolute path (Takes precedence over the above options)', default=None)
    parser.add_argument('--ncolor', '-n', type=int,
                        help='Alternative color mode (default is 0), some images return more than one color, this will use either the matched or last one', default=None)
    parser.add_argument('--light', '-l', action='store_true',
                        help='Enable Light mode (default is Dark)')
    parser.add_argument('--dark', '-d', action='store_true',
                        help='Enable Dark mode (ignores user config)')
    parser.add_argument('--autostart', '-a', action='store_true',
                        help='Enable (copies) the startup script to automatically start with KDE')
    parser.add_argument('--copyconfig', '-c', action='store_true',
                        help='Copies the default config to ~/.config/kde-material-you-colors/config.conf')
    parser.add_argument('--iconslight', type=str,
                        help='Icons for Dark scheme', default=None)
    parser.add_argument('--iconsdark', type=str,
                        help='Icons for Light scheme', default=None)
    parser.add_argument('--pywal', '-wal', action='store_true',
                        help='Use pywal to theme other apps with Material You')
    parser.add_argument('--pywallight', '-wall', action='store_true',
                        help='Use Light mode for pywal controlled apps')
    parser.add_argument('--pywaldark', '-wald', action='store_true',
                        help='Use Dark mode for pywal controlled apps')
    parser.add_argument('--lbmultiplier', '-lbm', type=float,
                        help='The amount of color for backgrounds in Light mode (value from 0 to 4.0, default is 1)',default=None)
    parser.add_argument('--dbmultiplier', '-dbm', type=float,
                        help='The amount of color for backgrounds in Dark mode (value from 0 to 4.0, default is 1)',default=None)

    # Get arguments
    args = parser.parse_args()
    # Get config from file
    config = Configs(args)
    options_old = config.options
    print(f"Config: {options_old}")
    icons_old = [options_old['iconslight'], options_old['iconsdark']]
    light_old = options_old['light']
    # Get the current wallpaper on startup
    wallpaper_old = currentWallpaper(options_old)
        
    if wallpaper_old != None and wallpaper_old[1] != None:
        wallpaper_old_type = wallpaper_old[0]
        wallpaper_old_data = wallpaper_old[1]
        print(f'Using wallpaper: {wallpaper_old_data}')
        
        # if wallpaper is image save time of last modification
        if wallpaper_old_type == "image":
            wallpaper_mod_time_old = get_last_modification(wallpaper_old_data)
        else: 
            wallpaper_mod_time_old = None
        
        set_color_schemes(
                    wallpaper=wallpaper_old, light=options_old['light'], ncolor=options_old['ncolor'], pywal=options_old['pywal'], pywal_light=options_old['pywal_light'],lbmult=options_old['lbm'],dbmult=options_old['dbm'])

    set_icons(icons_light=options_old['iconslight'],
             icons_dark=options_old['iconsdark'], light=options_old['light'])
    #fix borked terminal idk...
    print("---------------------")

    # check wallpaper change
    while True:
        # reload config file
        config = Configs(args)
        options_new = config.options
        #print(f"pywal: {options_new['pywal']}")
        wallpaper_new = currentWallpaper(options_new)
        if wallpaper_new != None and wallpaper_new[1] != None:
            wallpaper_new_type = wallpaper_new[0]
            wallpaper_new_data = wallpaper_new[1]
            
            # if wallpaper is image save time of last modification
            if wallpaper_new_type == "image":
                wallpaper_mod_time_new = get_last_modification(wallpaper_new_data)
            else: 
                wallpaper_mod_time_new = None
            
            icons_new = [options_new['iconslight'], options_new['iconsdark']]
            light_new = options_new['light']

            wallpaper_changed = wallpaper_old != wallpaper_new
            wallpaper_modified = wallpaper_mod_time_old != wallpaper_mod_time_new
            options_changed = options_new != options_old
            icons_changed = icons_new != icons_old
            light_changed = light_new != light_old

            if wallpaper_changed or options_changed or wallpaper_modified:
                if options_changed:
                    print(f"New Config: {options_new}")
                    if icons_changed or light_changed:
                        set_icons(
                            icons_light=options_new['iconslight'], icons_dark=options_new['iconsdark'], light=options_new['light'])
                
                if wallpaper_changed or wallpaper_modified:
                    print(f'Wallpaper changed: {wallpaper_new_data}')
                
                set_color_schemes(
                    wallpaper=wallpaper_new, light=options_new['light'], ncolor=options_new['ncolor'], pywal=options_new['pywal'], pywal_light=options_new['pywal_light'],lbmult=options_new['lbm'],dbmult=options_new['dbm'])
                #fix borked terminal idk...
                print("---------------------")
                
            wallpaper_old = wallpaper_new
            wallpaper_mod_time_old = wallpaper_mod_time_new
            options_old = options_new
            icons_old = icons_new
            light_old = light_new
        time.sleep(1)
