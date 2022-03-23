import subprocess,json,time,os,dbus,argparse,configparser
from color_scheme import ColorScheme
from pathlib import Path
HOME = str(Path.home())
CONFIG_PATH = HOME+"/.config/kde-material-you-colors/config.conf"
SCHEMES_PATH = HOME+"/.local/share/color-schemes"
# Get current wallpaper from plain file or plugin + containment combo


def get_wallpaper_path(plugin='org.kde.image', monitor=0, file=None):

    if file:
        while not os.path.exists(file):
            print(f'Text file {file} not found waiting 5 seconds to try again')
            time.sleep(5)
        try:
            with open(file, 'r', encoding='utf8') as wallpaper:
                wallpaper_path = str(wallpaper.read()).replace(
                    'file://', '').strip()
                if wallpaper_path:
                    return wallpaper_path
                else:
                    print(f'Error: "{file}" file seems empty')
                    quit(1)
        except Exception as e:
            print(f'Error opening file file:\n{e}')
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
            quit()


def set_color_schemes(current_wallpaper, light):
    if os.path.exists(current_wallpaper):
        #print(f'Found wallpaper: "{current_wallpaper}"')
        current_wallpaper = f'"{current_wallpaper}"'
        # get colors from material-color-utility
        materialYouColors = subprocess.Popen("material-color-utility "+current_wallpaper,
                                             shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
        # make sure that we got colors from MaterialColorUtilities
        if materialYouColors:
            # parse colors string to json
            colors_json = json.loads(materialYouColors)

            with open('output.json', 'w', encoding='utf8') as current_scheme:
                # light_scheme_file.write(str(colors_json))
                current_scheme.write(json.dumps(
                    colors_json, indent=4, sort_keys=False))

            # generate and apply color schemes
            colors_light = ColorScheme(colors_json)
            colors_light.make_color_schemes(light)
        else:
            print(f'''Error: Couldn't get colors from "{current_wallpaper}"''')
            quit(1)
    else:
        print(
            f'''Error: File "{current_wallpaper}" from "{args.file}" does not exist''')
        quit(1)


class Configs():
    def __init__(self, args):
        c_light = None
        c_monitor = None
        c_file = None
        c_plugin = None
        if not os.path.exists(SCHEMES_PATH):
            os.makedirs(SCHEMES_PATH)

        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_PATH):
            config.read(CONFIG_PATH)

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

                if 'plugin' in custom:
                    c_plugin = custom['plugin']

        if args.dark == True:
            c_light = False
        elif args.light == False or c_light != None:
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

        if args.plugin != None:
            c_plugin = args.plugin
        elif args.plugin == None and c_plugin == None:
            c_plugin = 'org.kde.image'
        else:
            c_plugin = c_plugin

        self._options = {
            'light': c_light,
            'file': c_file,
            'monitor': c_monitor,
            'plugin': c_plugin
        }

    @property
    def options(self):
        return self._options


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Wallpaper Material You colors for KDE')
    parser.add_argument('--monitor', '-m', type=int,
                        help='Monitor to get wallpaper (default is 0)', default=None)
    parser.add_argument('--light', '-l', type=bool, const=True, nargs='?',
                        help='Enable Light mode (default is Dark)', default=False)
    parser.add_argument('--dark', '-d', type=bool, const=True, nargs='?',
                        help='Enable Dark mode (default is Dark)', default=False)
    parser.add_argument('--plugin', '-p', type=str,
                        help=f'Wallpaper plugin id (default is org.kde.image) you can find them in: /usr/share/plasma/wallpapers/ or ~/.local/share/plasma/wallpapers', default=None)
    parser.add_argument('--file', '-f', type=str,
                        help='Text file that contains wallpaper absolute path', default=None)

    args = parser.parse_args()
    config = Configs(args)
    options = config.options
    print(
        f"Current config: Plugin: {options['plugin']} | Light mode: {options['light']} | File: {options['file']} | Monitor: {options['monitor']}")

    def currentWallpaper(options):
        return str(get_wallpaper_path(plugin=options['plugin'], monitor=options['monitor'], file=options['file']))

    set_color_schemes(currentWallpaper(options), options['light'])

    # check wallpaper change
    while True:
        config = Configs(args)
        options = config.options
        wallpaper_old = currentWallpaper(options)
        time.sleep(1)
        config = Configs(args)
        new_options = config.options
        wallpaper_new = currentWallpaper(options)
        wallpaper_changed = wallpaper_old != wallpaper_new
        options_changed = options != new_options
        
        if options_changed:
            print(
                f"New config: Plugin: {new_options['plugin']} | Light mode: {new_options['light']} | File: {new_options['file']} | Monitor: {new_options['monitor']}")
        if wallpaper_changed:
            print(f'Wallpaper changed: {wallpaper_new}')

        if wallpaper_changed or options_changed:
            set_color_schemes(wallpaper_new, new_options['light'])
