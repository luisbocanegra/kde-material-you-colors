import time
import os
import argparse
import utils
from schemeconfigs import ThemeConfig
if __name__ == '__main__':
    # Make sure the schemes path exists
    if not os.path.exists(utils.USER_SCHEMES_PATH):
        os.makedirs(utils.USER_SCHEMES_PATH)
    parser = argparse.ArgumentParser(
        description='Automatic Material You Colors Generator from your wallpaper for the Plasma Desktop')
    parser.add_argument('--monitor', '-m', type=int,
                        help='Monitor to get wallpaper (default is 0) but second one is 6 in my case, play with this to find yours', default=None)
    parser.add_argument('--plugin', '-p', type=str,
                        help=f'Wallpaper plugin id (default is {utils.DEFAULT_PLUGIN}) you can find them in: /usr/share/plasma/wallpapers/ or ~/.local/share/plasma/wallpapers', default=None)
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
    parser.add_argument('--on-change-hook', type=str,
                        help='A script/command that will be executed on start or wallpaper/dark/light/settings change',default=None)

    # Get arguments
    args = parser.parse_args()
    # Get config from file
    config = utils.Configs(args)
    options_old = config.options
    print(f"Config: {options_old}")
    icons_old = [options_old['iconslight'], options_old['iconsdark']]
    light_old = options_old['light']
    # Get the current wallpaper on startup
    wallpaper_old = utils.currentWallpaper(options_old)
    kde_globals_light_old=utils.kde_globals_light()
    pywal_light_old=options_old['pywal_light']
    if wallpaper_old != None and wallpaper_old[1] != None:
        wallpaper_old_type = wallpaper_old[0]
        wallpaper_old_data = wallpaper_old[1]
        print(f'Using wallpaper: {wallpaper_old_data}')
        colors = utils.get_color_schemes(wallpaper_old,options_old['ncolor'])
        schemes = ThemeConfig(colors,wallpaper_old_data,light_blend_multiplier=options_old['lbm'], dark_blend_multiplier=options_old['dbm'])
        utils.make_plasma_scheme(schemes=schemes)
        # if wallpaper is image save time of last modification
        if wallpaper_old_type == "image":
            wallpaper_mod_time_old = utils.get_last_modification(wallpaper_old_data)
        else: 
            wallpaper_mod_time_old = None
        light = None
        if options_old['light'] == None:
            if kde_globals_light_old != None:
                light=kde_globals_light_old
        else:
            light = options_old['light']
            
        utils.apply_color_schemes(
                    light=light)
        utils.apply_pywal_schemes(
                    light=light, use_pywal=options_old['pywal'], pywal_light=options_old['pywal_light'], schemes=schemes)

        utils.set_icons(icons_light=options_old['iconslight'],
             icons_dark=options_old['iconsdark'], light=options_old['light'])
        utils.run_hook(options_old['on_change_hook'])
    #fix borked terminal idk...
    print("---------------------")

    # check wallpaper change
    while True:
        # reload config file
        config = utils.Configs(args)
        options_new = config.options
        #print(f"pywal: {options_new['pywal']}")
        wallpaper_new = utils.currentWallpaper(options_new)
        kde_globals_light_new=utils.kde_globals_light()
        pywal_light_new=options_new['pywal_light']
        if wallpaper_new != None and wallpaper_new[1] != None:
            wallpaper_new_type = wallpaper_new[0]
            wallpaper_new_data = wallpaper_new[1]
            # if wallpaper is image save time of last modification
            if wallpaper_new_type == "image":
                wallpaper_mod_time_new = utils.get_last_modification(wallpaper_new_data)
            else: 
                wallpaper_mod_time_new = None
            
            icons_new = [options_new['iconslight'], options_new['iconsdark']]
            light_new = options_new['light']

            wallpaper_changed = wallpaper_old != wallpaper_new
            wallpaper_modified = wallpaper_mod_time_old != wallpaper_mod_time_new
            options_changed = options_new != options_old
            icons_changed = icons_new != icons_old
            light_changed = light_new != light_old
            kde_globals_light_changed = kde_globals_light_old != kde_globals_light_new
            pywal_light_changed = pywal_light_old != pywal_light_new
            
            if options_new['light'] == None:
                if kde_globals_light_new != None:
                    light=kde_globals_light_new
            else:
                light = options_new['light']

            if wallpaper_changed or options_changed or wallpaper_modified:
                colors = utils.get_color_schemes(wallpaper_new,options_new['ncolor'])
                schemes = ThemeConfig(colors,wallpaper_new_data,light_blend_multiplier=options_new['lbm'], dark_blend_multiplier=options_new['dbm'])
                utils.make_plasma_scheme(schemes=schemes)
                if options_changed:
                    print(f"New Config: {options_new}")
                    if icons_changed or light_changed:
                        utils.set_icons(
                            icons_light=options_new['iconslight'], icons_dark=options_new['iconsdark'], light=light)
                
                if wallpaper_changed or wallpaper_modified:
                    print(f'Wallpaper changed: {wallpaper_new_data}')
                
                utils.apply_color_schemes(
                    light=light)
                utils.apply_pywal_schemes(
                    light=light, use_pywal=options_new['pywal'], pywal_light=options_new['pywal_light'], schemes=schemes)
                utils.run_hook(options_new['on_change_hook'])
                print("---------------------")
            elif kde_globals_light_changed and kde_globals_light_new != None:
                    utils.apply_pywal_schemes(
                        light=kde_globals_light_new, use_pywal=options_new['pywal'], pywal_light=options_new['pywal_light'], schemes=schemes)
                    utils.set_icons(icons_light=options_new['iconslight'],
                        icons_dark=options_new['iconsdark'], light=kde_globals_light_new)
                    utils.run_hook(options_new['on_change_hook'])

            wallpaper_old = wallpaper_new
            wallpaper_mod_time_old = wallpaper_mod_time_new
            options_old = options_new
            icons_old = icons_new
            light_old = light_new
            kde_globals_light_old = kde_globals_light_new
            pywal_light_old = pywal_light_new
        time.sleep(1)
