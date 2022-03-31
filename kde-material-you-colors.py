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
find_colr = importlib.util.find_spec("colr")
USER_HAS_COLR = find_colr is not None
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
BOLD_TEXT = "\033[1m"
RESET_TEXT = "\033[0;0m"
# Get current wallpaper from plain file or plugin + containment combo


def get_wallpaper_path(plugin=DEFAULT_PLUGIN, monitor=0, file=None):

    if file:
        if os.path.exists(file):
            with open(file) as file:
                wallpaper = str(file.read()).replace('file://', '').strip()
                if wallpaper:
                    return wallpaper
                else:
                    return None
        else:
            print(f'File "{file}" does not exist')
            return None
    else:

        script = """
        var Desktops = desktops();
        //for (i=0;i<Desktops.length;i++) {
            d = Desktops[%s];
            d.wallpaperPlugin = "%s";
            d.currentConfigGroup = Array("Wallpaper", "%s", "General");
            print(d.readConfig("Image"));
        //}
        """
        try:
            bus = dbus.SessionBus()
            plasma = dbus.Interface(bus.get_object(
                'org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
            wallpaper_path = str(plasma.evaluateScript(
                script % (monitor, plugin, plugin))).replace('file://', '')
            return wallpaper_path
        except Exception as e:
            print(f'Error getting wallpaper from dbus:\n{e}')


def set_color_schemes(current_wallpaper, light, ncolor):
    if current_wallpaper != None:
        if os.path.exists(current_wallpaper):
            #print(f'Found wallpaper: "{current_wallpaper}"')
            current_wallpaper = f'"{current_wallpaper}"'
            # get colors from material-color-utility
            try:
                materialYouColors = subprocess.check_output("material-color-utility "+current_wallpaper+" "+str(ncolor),
                                                            shell=True,universal_newlines=True).strip()
                try:
                    # parse colors string to json
                    colors_json = json.loads(materialYouColors)
                    print(f'{BOLD_TEXT}Best colors:',end=' ')
                    for index,col in colors_json['bestColors'].items():
                        if USER_HAS_COLR:
                            print(f'{BOLD_TEXT}{index}:{color(col,fore=col)}',end=' ')
                        else:
                            print(f'{BOLD_TEXT}{index}:{col}',end=' ')
                    print(f'{BOLD_TEXT}')
                    seed = colors_json['seedColor']
                    sedColor = list(seed.values())[0]
                    seedNo = list(seed.keys())[0]
                    if USER_HAS_COLR:
                        print(BOLD_TEXT+"Using seed: "+seedNo+":"+color(sedColor,fore=sedColor))
                    else:
                        print(BOLD_TEXT+"Using seed: "+seedNo+":"+sedColor+RESET_TEXT)
                    # with open('output.json', 'w', encoding='utf8') as current_scheme:
                    #     current_scheme.write(json.dumps(
                    #         colors_json, indent=4, sort_keys=False))
                        
                    with open('/tmp/kde-material-you-colors.json', 'w', encoding='utf8') as current_scheme:
                        current_scheme.write(json.dumps(
                            colors_json, indent=4, sort_keys=False))

                    # generate and apply color schemes
                    colors_light = ColorScheme(colors_json)
                    colors_light.make_color_schemes(light)
                except Exception as e:
                        print(f'Error:\n {e}')
            except Exception as e:
                print(f'Error trying to get colors from {current_wallpaper}')
        else:
            print(
                f'''Error: File "{current_wallpaper}" does not exist''')


class Configs():
    def __init__(self, args):
        c_light = None
        c_monitor = None
        c_file = None
        c_plugin = None
        c_ncolor = None

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

            if args.dark == True:
                c_light = False

            elif args.light == True:
                c_light = args.light

            else:
                c_light = c_light

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

            self._options = {
                'light': c_light,
                'file': c_file,
                'monitor': c_monitor,
                'plugin': c_plugin,
                'ncolor': c_ncolor
            }

    @property
    def options(self):
        return self._options


def currentWallpaper(options):
    return get_wallpaper_path(plugin=options['plugin'], monitor=options['monitor'], file=options['file'])


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

    # Get arguments
    args = parser.parse_args()
    # Get config from file
    config = Configs(args)
    options_old = config.options
    print(
        f"Current config: Plugin: {options_old['plugin']} | Light: {options_old['light']} | File: {options_old['file']} | Monitor: {options_old['monitor']} | Ncolor: {options_old['ncolor']}")

    # Get the current wallpaper on startup
    wallpaper_old = currentWallpaper(options_old)
    if wallpaper_old != None:
        print(f'Settting color schemes for {wallpaper_old}')
        set_color_schemes(currentWallpaper(options_old), options_old['light'], options_old['ncolor'])

    # check wallpaper change
    while True:
        config = Configs(args)
        options_new = config.options
        wallpaper_new = currentWallpaper(options_new)

        wallpaper_changed = wallpaper_old != wallpaper_new
        options_changed = options_new != options_old

        if wallpaper_changed or options_changed:
            if options_changed:
                print(
                    f"Current config: Plugin: {options_new['plugin']} | Light: {options_new['light']} | File: {options_new['file']} | Monitor: {options_new['monitor']} | Ncolor: {options_new['ncolor']}")
            if wallpaper_changed:
                print(f'Wallpaper changed: {wallpaper_new}')
            set_color_schemes(wallpaper_new, options_new['light'],options_new['ncolor'])
        wallpaper_old = wallpaper_new
        options_old = options_new
        time.sleep(1)
