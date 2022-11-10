import configparser
import logging
import os
import subprocess
import globals
from . import kwin_utils


def make_scheme(schemes=None):
    # Make sure the schemes path exists
    if not os.path.exists(globals.USER_SCHEMES_PATH):
        os.makedirs(globals.USER_SCHEMES_PATH)
    light_scheme = schemes.get_light_scheme()
    dark_scheme = schemes.get_dark_scheme()
    # plasma-apply-colorscheme doesnt allow to apply the same theme twice to reload
    # since I don't know how to reaload it with code lets make a copy and switch between them
    # sadly color settings will show copies too

    with open(globals.THEME_LIGHT_PATH+"2.colors", 'w', encoding='utf8') as light_scheme_file:
        light_scheme_file.write(light_scheme)
    with open(globals.THEME_LIGHT_PATH+".colors", 'w', encoding='utf8') as light_scheme_file:
        light_scheme_file.write(light_scheme)
    with open(globals.THEME_DARK_PATH+"2.colors", 'w', encoding='utf8') as dark_scheme_file:
        dark_scheme_file.write(dark_scheme)
    with open(globals.THEME_DARK_PATH+".colors", 'w', encoding='utf8') as dark_scheme_file:
        dark_scheme_file.write(dark_scheme)


def apply_color_schemes(light=False):
    if light == None:
        light = False
    if light != None:
        if light == True:
            color_scheme = globals.THEME_LIGHT_PATH
        elif light == False:
            color_scheme = globals.THEME_DARK_PATH
        kwin_utils.blend_changes()
        subprocess.run("plasma-apply-colorscheme "+color_scheme+"2.colors",
                       shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        colorscheme_out = subprocess.check_output("plasma-apply-colorscheme "+color_scheme+".colors",
                                                  shell=True, stderr=subprocess.PIPE, universal_newlines=True).strip()
        logging.info(colorscheme_out)


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


def kde_globals_light():
    kdeglobals = configparser.ConfigParser()
    if os.path.exists(globals.KDE_GLOBALS):
        try:
            kdeglobals.read(globals.KDE_GLOBALS)
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
