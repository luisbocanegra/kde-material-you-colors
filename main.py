from multiprocessing.connection import wait
import subprocess
import json
import time
from color_scheme import ColorScheme
import os
import dbus
import argparse

# Get current wallpaper from plain file or plugin + containment combo
def get_wallpaper(plugin = 'org.kde.image', monitor=0, file=None):
    
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
    
    parser = argparse.ArgumentParser(description='KDE Wallpaper setter')
    parser.add_argument('--monitor','-m', help='Monitor to get wallpaper (default is 0)', default=0)
    parser.add_argument('--plugin', '-p', help='Wallpaper plugin (default is org.kde.image)', default='org.kde.image')
    parser.add_argument('--file','-f', help='File that contains wallpaper path', default=None)

    args = parser.parse_args()


    def set_color_schemes(current_wallpaper):
                if os.path.exists(current_wallpaper):
                    print(f'Found wallpaper: "{current_wallpaper}"')
                    current_wallpaper = f'"{current_wallpaper}"'
                    # get colors from materialYouColors 
                    materialYouColors = subprocess.Popen("./material-you-colors-binary "+current_wallpaper,
                                                        shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
    
                    # make sure that we got colors from MaterialColorUtilities 
                    if materialYouColors:
                        # parse colors string to json
                        colors_json = json.loads(materialYouColors)
                        
                        # generate and apply color schemes
                        colors_light = ColorScheme(colors_json)
                        colors_light.make_color_schemes()
                    else:
                        print(f'''Error: Couldn't get colors from "{current_wallpaper}"''')
                        quit(1)
                else:
                    print(f'''Error: File "{current_wallpaper}" from "{args.file}" does not exist''')
                    quit(1)
    
    
    while True:
        current_wallpaper_old = str(get_wallpaper(plugin=args.plugin, monitor=args.monitor, file=args.file))
        time.sleep(1)
        current_wallpaper_new = str(get_wallpaper(plugin=args.plugin, monitor=args.monitor, file=args.file))
        
        if current_wallpaper_old !=current_wallpaper_new:
            set_color_schemes(current_wallpaper_new)
            
    

