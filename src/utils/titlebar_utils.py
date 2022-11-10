import logging
import configparser
import os
from . import math_utils
import globals


def sierra_breeze_button_colors(schemes, light=None):
    if light == True:
        colors = schemes.get_sierra_breeze_light_colors()
    elif light == False:
        colors = schemes.get_sierra_breeze_dark_colors()

    breezerc = configparser.ConfigParser()
    # preserve case
    breezerc.optionxform = str
    if os.path.exists(globals.BREEZE_RC):
        try:
            breezerc.read(globals.BREEZE_RC)
            if 'Windeco' in breezerc:
                breezerc['Windeco']['ButtonCloseActiveColor'] = colors['btn_close_active_color']
                breezerc['Windeco']['ButtonMaximizeActiveColor'] = colors['btn_maximize_active_color']
                breezerc['Windeco']['ButtonMinimizeActiveColor'] = colors['btn_minimize_active_color']
                breezerc['Windeco']['ButtonKeepAboveActiveColor'] = colors['btn_keep_above_active_color']
                breezerc['Windeco']['ButtonKeepBelowActiveColor'] = colors['btn_keep_below_active_color']
                breezerc['Windeco']['ButtonOnAllDesktopsActiveColor'] = colors['btn_on_all_desktops_active_color']
                breezerc['Windeco']['ButtonShadeActiveColor'] = colors['btn_shade_active_color']

                # Inactive
                breezerc['Windeco']['ButtonCloseInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonMaximizeInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonMinimizeInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonKeepAboveInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonKeepBelowInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonOnAllDesktopsInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonShadeInactiveColor'] = colors['btn_inactive_color']
                reload = True
            else:
                reload = False
            if reload == True:
                logging.info(f"Applying SierraBreeze window button colors")
                with open(globals.BREEZE_RC, 'w') as configfile:
                    breezerc.write(configfile, space_around_delimiters=False)
        except Exception as e:
            logging.error(f"Error writing breeze window button colors:\n{e}")
    else:
        logging.warning(
            f"SierraBreeze config '{globals.BREEZE_RC}' not found, skipping")


def titlebar_opacity(opacity):
    if opacity != None:
        opacity = math_utils.clip(opacity, 0, 100, 100)
        conf_file = configparser.ConfigParser()
        # preserve case
        conf_file.optionxform = str

        if os.path.exists(globals.SBE_RC):
            try:
                conf_file.read(globals.SBE_RC)
                if 'Windeco' in conf_file:
                    conf_file['Windeco']['BackgroundOpacity'] = str(
                        int(opacity))
                    reload = True
                else:
                    reload = False
                if reload == True:
                    logging.info(
                        f"Applying SierraBreezeEnhanced titlebar opacity")
                    with open(globals.SBE_RC, 'w') as configfile:
                        conf_file.write(
                            configfile, space_around_delimiters=False)
            except Exception as e:
                logging.error(
                    f"Error writing SierraBreezeEnhanced titlebar opacity:\n{e}")

        if os.path.exists(globals.KLASSY_RC):
            try:
                conf_file.read(globals.KLASSY_RC)
                if 'Common' in conf_file:
                    conf_file['Common']['ActiveTitlebarOpacity'] = str(
                        int(opacity))
                    conf_file['Common']['InactiveTitlebarOpacity'] = str(
                        int(opacity))
                    reload = True
                else:
                    reload = False
                if reload == True:
                    logging.info(f"Applying Klassy titlebar opacity")
                    with open(globals.KLASSY_RC, 'w') as configfile:
                        conf_file.write(
                            configfile, space_around_delimiters=False)
            except Exception as e:
                logging.error(f"Error writing Klassy titlebar opacity:\n{e}")
