import subprocess
import logging
from .color_utils import hex2rgb
from .math_utils import clip
from .string_utils import tup2str
import configparser
import os
import globals


def export_scheme(light=None, pywal_light=None, schemes=None, konsole_opacity=100):
    if konsole_opacity == None:
        konsole_opacity = 100
    else:
        konsole_opacity = float(clip(konsole_opacity, 0, 100, 100)/100)
    # print(f"konsole_opacity: {konsole_opacity}")
    if pywal_light != None:
        if pywal_light == True:
            pywal_colors = schemes.get_wal_light_scheme()
        else:
            pywal_colors = schemes.get_wal_dark_scheme()
    elif light != None:
        if light == True:
            pywal_colors = schemes.get_wal_light_scheme()
        elif light == False:
            pywal_colors = schemes.get_wal_dark_scheme()
    else:
        pywal_colors = schemes.get_wal_dark_scheme()
    config = configparser.ConfigParser()
    config.optionxform = str
    if os.path.exists(globals.KONSOLE_COLOR_SCHEME_PATH):
        config.read(globals.KONSOLE_COLOR_SCHEME_PATH)

    sections = ['Background',
                'BackgroundIntense',
                'BackgroundFaint',
                'Color',
                'Foreground',
                'ForegroundIntense',
                'ForegroundFaint',
                'General']
    exp = []
    for section in sections:
        if section == 'Color':
            for n in range(8):
                exp.append(str(f'Color{n}'))
                exp.append(str(f'Color{n}Intense'))
                exp.append(str(f'Color{n}Faint'))
        else:
            exp.append(section)

    for section in exp:
        if not config.has_section(section):
            config.add_section(section)
    config['Background']['Color'] = tup2str(
        hex2rgb(pywal_colors['special']['background']))
    config['BackgroundIntense']['Color'] = tup2str(
        hex2rgb(pywal_colors['special']['backgroundIntense']))
    config['BackgroundFaint']['Color'] = tup2str(
        hex2rgb(pywal_colors['special']['backgroundFaint']))
    config['Color0']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color0']))
    config['Color1']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color1']))
    config['Color2']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color2']))
    config['Color3']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color3']))
    config['Color4']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color4']))
    config['Color5']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color5']))
    config['Color6']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color6']))
    config['Color7']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color7']))

    config['Color0Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color8']))
    config['Color1Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color9']))
    config['Color2Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color10']))
    config['Color3Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color11']))
    config['Color4Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color12']))
    config['Color5Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color13']))
    config['Color6Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color14']))
    config['Color7Intense']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color15']))

    config['Color0Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color16']))
    config['Color1Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color17']))
    config['Color2Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color18']))
    config['Color3Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color19']))
    config['Color4Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color20']))
    config['Color5Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color21']))
    config['Color6Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color22']))
    config['Color7Faint']['Color'] = tup2str(
        hex2rgb(pywal_colors['colors']['color23']))

    config['Foreground']['Color'] = tup2str(
        hex2rgb(pywal_colors['special']['foreground']))
    config['ForegroundIntense']['Color'] = tup2str(
        hex2rgb(pywal_colors['special']['foregroundIntense']))
    config['ForegroundFaint']['Color'] = tup2str(
        hex2rgb(pywal_colors['special']['foregroundFaint']))

    config['General']['Description'] = "MaterialYou"
    config['General']['Opacity'] = str(konsole_opacity)

    with open(globals.KONSOLE_COLOR_SCHEME_PATH, 'w') as configfile:
        config.write(configfile, space_around_delimiters=False)

    config['General']['Description'] = "MaterialYouAlt"

    with open(globals.KONSOLE_COLOR_SCHEME_ALT_PATH, 'w') as configfile:
        config.write(configfile, space_around_delimiters=False)


def make_mirror_profile(profile=None):
    if profile != None:
        profile_path = globals.KONSOLE_DIR+profile+".profile"
        if os.path.exists(profile_path):
            logging.debug(f"konsole: mirror profile ({profile})")
            subprocess.check_output(
                "cp -f '"+profile_path+"' "+globals.KONSOLE_TEMP_PROFILE, shell=True)
            profile = configparser.ConfigParser()
            # preserve case
            profile.optionxform = str
            if os.path.exists(profile_path):
                try:
                    profile.read(profile_path)
                    if 'Appearance' in profile:
                        if profile['Appearance']['ColorScheme'] != "MaterialYou":
                            profile['Appearance']['ColorScheme'] = "MaterialYou"
                            with open(profile_path, 'w') as configfile:
                                profile.write(
                                    configfile, space_around_delimiters=False)
                except Exception as e:
                    logging.error(f"Error applying Konsole profile:\n{e}")

            # Mirror profile
            profile = configparser.ConfigParser()
            profile.optionxform = str
            if os.path.exists(globals.KONSOLE_TEMP_PROFILE):
                try:
                    profile.read(globals.KONSOLE_TEMP_PROFILE)
                    if 'Appearance' in profile:
                        profile['Appearance']['ColorScheme'] = "MaterialYouAlt"
                        profile['General']['Name'] = "TempMyou"
                except Exception as e:
                    logging.error(f"Error applying Konsole profile:\n{e}")
                with open(globals.KONSOLE_TEMP_PROFILE, 'w') as configfile:
                    profile.write(configfile, space_around_delimiters=False)


def reload_profile(profile=None):
    if profile != None:
        logging.info(f"konsole: reload profile ({profile})")
        konsole_dbus_services = subprocess.check_output(
            "qdbus org.kde.konsole*", shell=True, universal_newlines=True).strip().splitlines()
        if konsole_dbus_services:
            for service in konsole_dbus_services:
                try:
                    konsole_sessions = subprocess.check_output(
                        "qdbus "+service+" | grep 'Sessions/'", shell=True, universal_newlines=True).strip().splitlines()
                    for session in konsole_sessions:
                        #print(f"service: {service} -> {session}")
                        current_profile = subprocess.check_output(
                            "qdbus "+service+" "+session+" org.kde.konsole.Session.profile", shell=True, universal_newlines=True).strip()
                        # print(current_profile)
                        if current_profile == profile:
                            subprocess.check_output(
                                "qdbus "+service+" "+session+" org.kde.konsole.Session.setProfile 'TempMyou'", shell=True)
                        else:
                            subprocess.check_output(
                                "qdbus "+service+" "+session+" org.kde.konsole.Session.setProfile '"+profile + "'", shell=True)
                except:
                    pass


def apply_color_scheme(light=None, pywal_light=None, schemes=None, profile=None, konsole_opacity=None):
    if profile != None:
        profile_path = globals.KONSOLE_DIR+profile+".profile"
        if os.path.exists(profile_path):
            export_scheme(light, pywal_light, schemes, konsole_opacity)
            reload_profile(profile)
        else:
            logging.error(f"Konsole Profile: {profile_path} does not exist")
