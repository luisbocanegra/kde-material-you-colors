import configparser
import logging
import os
import subprocess
import globals
from . import kwin_utils
from . import file_utils


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

    plasma_darker_header(schemes)


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
        # Get hash of the updated theme
        hash = file_utils.get_file_sha1(color_scheme+".colors")
        # Update ColorScheme hash in kdeglobals file
        if os.path.exists(globals.KDE_GLOBALS) and hash is not None:
            kdeglobals = configparser.ConfigParser()
            kdeglobals.optionxform = str
            try:
                kdeglobals.read(globals.KDE_GLOBALS)
                if 'General' not in kdeglobals:
                    kdeglobals.add_section('General')

                general = kdeglobals['General']
                general['ColorSchemeHash'] = hash

                with open(globals.KDE_GLOBALS, 'w') as configfile:
                    kdeglobals.write(
                        configfile, space_around_delimiters=False)
            except Exception as e:
                logging.error(f"Error:\n{e}")


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


def get_initial_mode():
    """Try to get the initial theme mode based based on the theme name
    or the stored hash against the current generated schemes.
    Fallback to dark mode if no previous mode is found.

    Returns:
        bool: Current mode light=True, dark=False
    """

    logging.info(f"Trying to get previous applied theme mode from {globals.KDE_GLOBALS}")
    theme_mode = kde_globals_light()

    if theme_mode is None:
        logging.info(
            "Couldn't find theme by name, trying to resolve theme from last stored hash...")

        current_theme_hash = None
        kdeglobals = configparser.ConfigParser()
        kdeglobals.optionxform = str
        try:
            kdeglobals.read(globals.KDE_GLOBALS)
            if 'General' in kdeglobals and 'ColorSchemeHash' in kdeglobals['General']:
                current_theme_hash = kdeglobals['General']['ColorSchemeHash']
        except Exception as e:
            logging.error(f"Error:\n{e}")

        if current_theme_hash is not None:
            logging.debug(f"Config file hash:  {current_theme_hash}")
            dark_scheme_hash = file_utils.get_file_sha1(
                globals.THEME_DARK_PATH+".colors")
            logging.debug(f"Dark scheme hash:  {dark_scheme_hash}")
            light_scheme_hash = file_utils.get_file_sha1(
                globals.THEME_LIGHT_PATH+".colors")
            logging.debug(f"Light scheme hash: {light_scheme_hash}")
            if current_theme_hash == dark_scheme_hash:
                theme_mode = False
            if current_theme_hash == light_scheme_hash:
                theme_mode = True
    
    if theme_mode is not None:
        logging.info(f"Found previous mode: {'light' if theme_mode else 'dark'}")
        return theme_mode
    
    logging.warning(
        "Couldn't find previus mode, falling back to dark theme")
    return False


def plasma_darker_header(schemes):
    """Make a copy of the generated plasma themes but with darker headers

    Args:
        schemes (ThemeConfig): generated color schemes
    """
    light_color = schemes.get_wal_light_scheme()['special']['background']
    dark_color = schemes.get_wal_dark_scheme()['special']['background']
    color_scheme = configparser.ConfigParser()
    color_scheme.optionxform = str
    try:
        # Edit titlebar of dark scheme
        color_scheme.read(globals.THEME_DARK_PATH+".colors")
        color_scheme['Colors:Header][Inactive']['BackgroundNormal'] = dark_color
        color_scheme['Colors:Header']['BackgroundNormal'] = dark_color
        color_scheme['General']['Name'] = "Material You Dark (darker titlebar)"

        with open(globals.THEME_DARK_PATH+"_darker_titlebar.colors", 'w') as configfile:
            color_scheme.write(
                configfile, space_around_delimiters=False)
        color_scheme['General']['Name'] = "Material You Dark (darker titlebar2)"
        with open(globals.THEME_DARK_PATH+"_darker_titlebar2.colors", 'w') as configfile:
            color_scheme.write(
                configfile, space_around_delimiters=False)

        # Edit titlebar of light scheme
        color_scheme.read(globals.THEME_LIGHT_PATH+".colors")
        color_scheme['Colors:Header][Inactive']['BackgroundNormal'] = light_color
        color_scheme['Colors:Header']['BackgroundNormal'] = light_color
        color_scheme['General']['Name'] = "Material You Light (darker titlebar)"

        with open(globals.THEME_LIGHT_PATH+"_darker_titlebar.colors", 'w') as configfile:
            color_scheme.write(
                configfile, space_around_delimiters=False)
        color_scheme['General']['Name'] = "Material You Light (darker titlebar2)"
        with open(globals.THEME_LIGHT_PATH+"_darker_titlebar2.colors", 'w') as configfile:
            color_scheme.write(
                configfile, space_around_delimiters=False)

    except Exception as e:
        logging.error(f"Error:\n{e}")
