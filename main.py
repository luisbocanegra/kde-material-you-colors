from multiprocessing.connection import wait
import subprocess
import json
from color_scheme import ColorScheme
import os
import pretty_errors
import dbus
import argparse


def get_wallpaper(plugin = 'org.kde.image', monitor=0):
    script = """
    var Desktops = desktops();
    //for (i=0;i<Desktops.length;i++) {
        d = Desktops[%s];
        d.wallpaperPlugin = "%s";
        d.currentConfigGroup = Array("Wallpaper", "%s", "General");
        print(d.readConfig("Image"));
    //}
    """
    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
    return str(plasma.evaluateScript(script % (monitor,plugin, plugin))).replace('file://','')
    
    
    

current_wallpaper = get_wallpaper('com.github.zren.inactiveblur',0)
print(current_wallpaper)
# Get current wallpaper
wallpaper_path = subprocess.Popen("cat '/home/luis/.config/plasma-org.kde.plasma.desktop-appletsrc' | sed '75q;d' | sed 's#Image=file://###'",
                                    shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
# print(wallpaper_path)
#wallpaper_path = wallpaper_path.split('\n', 1)[1]
copy_command = "cp -rfL '" + current_wallpaper + "' Test2/Resources/wallpaper.png"
print(copy_command)
os.system(copy_command)

colors_from_net = subprocess.Popen("cd /run/media/luis/Windows10/Users/luis/Documents/kde-material-you-colors/Test2 && dotnet run",
                                    shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip()

print(colors_from_net)

# print(colors_element[0].text)
if colors_from_net:
    # get text from element
    colors_str = colors_from_net

    # print(colors_str)

    # parse colors string to json
    colors_json = json.loads(colors_str)

    with open('putput.json', 'w', encoding='utf8') as light_scheme_file:
        # light_scheme_file.write(str(colors_json))
        light_scheme_file.write(json.dumps(
            colors_json, indent=4, sort_keys=False))

    # print(colors_json)
    colors_light = ColorScheme(colors_json)
    colors_light.make_light_scheme()
else:
    print('Error')
