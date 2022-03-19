from multiprocessing.connection import wait
import subprocess
import requests
from requests_html import AsyncHTMLSession
import json
from color_scheme import ColorScheme
import os
from subprocess import check_output
import shutil
import pretty_errors

url = "http://localhost/kde-material-you-colors/"


def remove_last_line_from_string(s):
    return s[:s.rfind('\n')]


# Set current wallpaper
wallpaper_path = subprocess.Popen("cat '/home/luis/.config/plasma-org.kde.plasma.desktop-appletsrc' | sed '74q;d' | sed 's#Image=file://###'",
                                  shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
# print(wallpaper_path)
#wallpaper_path = wallpaper_path.split('\n', 1)[1]
copy_command = "cp -rfL '" + wallpaper_path + "' Test2/Resources/wallpaper.png"
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
