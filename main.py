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
wallpaper_path = subprocess.Popen("cat '/home/luis/.config/plasma-org.kde.plasma.desktop-appletsrc' | sed '75q;d' | sed 's#Image=file://###'", shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
#wallpaper_path = wallpaper_path.split('\n', 1)[1]
c_m = "cp -rfL '"+ wallpaper_path + "' current_wallpaper.png"
print(c_m)
os.system(c_m)
print('hola')
print(wallpaper_path)
print('hola')

#with open(wallpaper_path) as wallpaper:
# os.symlink('/home/luis/Pictures/Wallpapers/Elixir.png', 'tmpLink')
# os.rename('tmpLink', 'current_wallpaper.png')
# shutil.copy('/home/luis/Pictures/Wallpapers/Elixir.png','current_wallpaper.png')
# os.system("cp")
# create an HTML Session object
session = AsyncHTMLSession()
try:
    async def get_results():
        r = await session.get(url)
        await r.html.arender(timeout=30, sleep=10)
        return r
    
    # Use the object above to connect to needed webpage
    response =  session.run(get_results)
    # Run JavaScript code on webpage
    
except requests.exceptions.RequestException as e:
    print(e)

# find element with colors object
print(response[0].text)

colors_element = response[0].html.find("#colors_element")

print(colors_element[0].text)
if colors_element:
    # get text from element
    colors_str = colors_element[0].text

    #print(colors_str)

    # parse colors string to json
    colors_json = json.loads(colors_str)

    with open ('putput.json', 'w', encoding='utf8') as light_scheme_file:
            light_scheme_file.write(str(colors_json))

    #print(colors_json)
    colors_light = ColorScheme(colors_json)
    colors_light.make_light_scheme()
else:
    print('Error')
