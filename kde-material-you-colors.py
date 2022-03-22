from multiprocessing.connection import wait
import subprocess
import json
import time
from color_scheme import ColorScheme
import os
import dbus
import argparse
import configparser
from pathlib import Path
# Get current wallpaper from plain file or plugin + containment combo
def get_wallpaper_path(plugin = 'org.kde.image', monitor=0, file=None):
    
    if file:
        try: 
            with open (file, 'r', encoding='utf8') as wallpaper:
                wallpaper_path = str(wallpaper.read()).replace('file://','').strip()
                if wallpaper_path:    
                    return wallpaper_path
                else:
                    print (f'Error: "{file}" file seems empty')
                    quit(1)
        except Exception as e:
            #print (f'Error opening file file:\n{e}')
            quit(e)
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
            plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
            wallpaper_path = str(plasma.evaluateScript(script % (monitor,plugin, plugin))).replace('file://','')
            return wallpaper_path
        except Exception as e:
            print(f'Error getting wallpaper from dbus:\n{e}')
            quit()

if __name__ == '__main__':
    home = str(Path.home())
    parser = argparse.ArgumentParser(description='Wallpaper Material You colors for KDE')
    parser.add_argument('--monitor','-m', help='Monitor to get wallpaper (default is 0)', default=0)
    parser.add_argument('--light','-l', const=True, nargs='?', help='Enable Light mode (default is Dark)', default=False)
    parser.add_argument('--plugin', '-p', help=f'Wallpaper plugin id (default is org.kde.image) you can find them in: /usr/share/plasma/wallpapers/ or ~/.local/share/plasma/wallpapers', default='org.kde.image')
    parser.add_argument('--file','-f', help='Text file that contains wallpaper absolute path', default=None)
    
    SCHEMES_PATH=home+"/.local/share/color-schemes"
    CONFIG_PATH=home+"/.config/kde-material-you-colors/config.conf"
    c_light=None
    c_monitor=None
    c_file=None
    c_plugin=None
    args = parser.parse_args()
    if not os.path.exists(SCHEMES_PATH):
        os.makedirs(SCHEMES_PATH)

    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH)
        
        if 'CUSTOM' in config:
            custom=config['CUSTOM']
            print("Loading user config...")
            
            if 'light' in custom:
                c_light = custom['light']
                print(f"Config has light option: {c_light}")
            
            if 'file' in custom:
                c_file = custom['file']
                print(f"Config has file option: {c_file}")
                
            if 'monitor' in custom:
                c_monitor = custom['monitor']
                print(f"Config has monitor option: {c_monitor}")
                
            if 'plugin' in custom:
                c_plugin = custom['plugin']
                print(f"Config has plugin option: {c_plugin}")
                
    if c_light == None:
        c_light = args.light
        
    if c_file == None:
        c_file = args.file
        
    if c_monitor == None:
        c_monitor = args.monitor
        
    if c_plugin == None:
        c_plugin = args.plugin
        
    print(f'Current config: Plugin: {c_plugin} | Light mode: {c_light} | File: {c_file} | Monitor: {c_monitor}')

    def set_color_schemes(current_wallpaper):
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
                        
                        # with open('output.json', 'w', encoding='utf8') as current_scheme:
                        #     # light_scheme_file.write(str(colors_json))
                        #     current_scheme.write(json.dumps(
                        #         colors_json, indent=4, sort_keys=False))
                        
                        # generate and apply color schemes
                        colors_light = ColorScheme(colors_json)
                        colors_light.make_color_schemes(c_light)
                    else:
                        print(f'''Error: Couldn't get colors from "{current_wallpaper}"''')
                        quit(1)
                else:
                    print(f'''Error: File "{current_wallpaper}" from "{args.file}" does not exist''')
                    quit(1)
                    
                    
    def currentWallpaper():
        return  str(get_wallpaper_path(plugin=c_plugin, monitor=c_monitor, file=c_file))
    
    set_color_schemes(currentWallpaper())
        
    # check wallpaper change
    while True:
        current_wallpaper_old = currentWallpaper()
        time.sleep(1)
        current_wallpaper_new = currentWallpaper()
        
        if current_wallpaper_old !=current_wallpaper_new:
            set_color_schemes(current_wallpaper_new)
            
    

