import logging
import configparser
import os
from .. import settings
from . import math_utils
from . import string_utils


def sierra_breeze_button_colors(schemes, light=None):
    if light == True:
        colors = schemes.get_sierra_breeze_light_colors()
    elif light == False:
        colors = schemes.get_sierra_breeze_dark_colors()

    breezerc = configparser.ConfigParser()
    # preserve case
    breezerc.optionxform = str
    if os.path.exists(settings.BREEZE_RC):
        try:
            breezerc.read(settings.BREEZE_RC)
            if "Windeco" in breezerc:
                breezerc["Windeco"]["ButtonCloseActiveColor"] = colors[
                    "btn_close_active_color"
                ]
                breezerc["Windeco"]["ButtonMaximizeActiveColor"] = colors[
                    "btn_maximize_active_color"
                ]
                breezerc["Windeco"]["ButtonMinimizeActiveColor"] = colors[
                    "btn_minimize_active_color"
                ]
                breezerc["Windeco"]["ButtonKeepAboveActiveColor"] = colors[
                    "btn_keep_above_active_color"
                ]
                breezerc["Windeco"]["ButtonKeepBelowActiveColor"] = colors[
                    "btn_keep_below_active_color"
                ]
                breezerc["Windeco"]["ButtonOnAllDesktopsActiveColor"] = colors[
                    "btn_on_all_desktops_active_color"
                ]
                breezerc["Windeco"]["ButtonShadeActiveColor"] = colors[
                    "btn_shade_active_color"
                ]

                # Inactive
                breezerc["Windeco"]["ButtonCloseInactiveColor"] = colors[
                    "btn_inactive_color"
                ]
                breezerc["Windeco"]["ButtonMaximizeInactiveColor"] = colors[
                    "btn_inactive_color"
                ]
                breezerc["Windeco"]["ButtonMinimizeInactiveColor"] = colors[
                    "btn_inactive_color"
                ]
                breezerc["Windeco"]["ButtonKeepAboveInactiveColor"] = colors[
                    "btn_inactive_color"
                ]
                breezerc["Windeco"]["ButtonKeepBelowInactiveColor"] = colors[
                    "btn_inactive_color"
                ]
                breezerc["Windeco"]["ButtonOnAllDesktopsInactiveColor"] = colors[
                    "btn_inactive_color"
                ]
                breezerc["Windeco"]["ButtonShadeInactiveColor"] = colors[
                    "btn_inactive_color"
                ]
                reload = True
            else:
                reload = False
            if reload == True:
                logging.info(f"Applying SierraBreeze window button colors")
                with open(settings.BREEZE_RC, "w") as configfile:
                    breezerc.write(configfile, space_around_delimiters=False)
        except Exception as e:
            logging.error(f"Error writing breeze window button colors:\n{e}")
    else:
        logging.warning(
            f"SierraBreeze config '{settings.BREEZE_RC}' not found, skipping"
        )


def titlebar_opacity(opacity_light, opacity_dark, light):
    opacity = opacity_light if light else opacity_dark
    if opacity is not None:
        opacity = math_utils.clip(opacity, 0, 100, 100)
        conf_file = configparser.ConfigParser()
        # preserve case
        conf_file.optionxform = str

        if os.path.exists(settings.SBE_RC):
            try:
                conf_file.read(settings.SBE_RC)
                if "Windeco" in conf_file:
                    conf_file["Windeco"]["BackgroundOpacity"] = str(int(opacity))
                    reload = True
                else:
                    reload = False
                if reload:
                    logging.info("Applying SierraBreezeEnhanced titlebar opacity")
                    with open(settings.SBE_RC, "w", encoding="utf-8") as configfile:
                        conf_file.write(configfile, space_around_delimiters=False)
            except Exception as e:
                logging.exception(
                    f"Error writing SierraBreezeEnhanced titlebar opacity:\n{e}"
                )

        if os.path.exists(settings.KLASSY_RC):
            try:
                conf_file.read(settings.KLASSY_RC)
                if "Common" in conf_file:
                    conf_file["Common"]["ActiveTitlebarOpacity"] = str(int(opacity))
                    conf_file["Common"]["InactiveTitlebarOpacity"] = str(int(opacity))
                    reload = True
                else:
                    reload = False
                if reload:
                    logging.info("Applying Klassy titlebar opacity")
                    with open(settings.KLASSY_RC, "w", encoding="utf-8") as configfile:
                        conf_file.write(configfile, space_around_delimiters=False)
            except Exception as e:
                logging.exception(f"Error writing Klassy titlebar opacity:\n{e}")


def klassy_windeco_outline_color(schemes, light=None):
    """Tint Klassy window decoration outline https://github.com/paulmcauley/klassy

    Args:
        schemes (ThemeConfig): generated color schemes
        light (bool, optional): Light or dark mode. Defaults to None.
    """
    if light == True:
        outline_color = schemes.get_extras()["dark"]["selectionAlt"]
    elif light == False:
        outline_color = schemes.get_extras()["dark"]["selectionAlt"]

    klassyrc = configparser.ConfigParser()
    # preserve case
    klassyrc.optionxform = str
    if os.path.exists(settings.KLASSY_RC):
        try:
            klassyrc.read(settings.KLASSY_RC)
            if "Windeco" in klassyrc:
                klassyrc["Windeco"][
                    "ThinWindowOutlineStyle"
                ] = "WindowOutlineCustomColor"
                klassyrc["Windeco"]["ThinWindowOutlineCustomColor"] = outline_color
                reload = True
            else:
                reload = False
            if reload == True:
                logging.info(f"Applying Klassy outline color")
                with open(settings.KLASSY_RC, "w") as configfile:
                    klassyrc.write(configfile, space_around_delimiters=False)
        except Exception as e:
            logging.error(f"Error writing Klassy outline color:\n{e}")
    else:
        logging.warning(f"Klassy config '{settings.KLASSY_RC}' not found, skipping")


def kwin_rule_darker_titlebar(light, darker_window_list):
    """Make the titlebar darker for the specified window class list

    Args:
        light (bool): Wether use light or dark theme
        darker_window_list (str): Space separated windo class names
    """
    if darker_window_list is None:
        darker_window_list = "--not-configured--"
    else:
        logging.info(f"Setting window rule [{darker_window_list}], light: {light}")
    if light is not None and light is True:
        scheme_name = "MaterialYouLight_darker_titlebar"
    else:
        scheme_name = "MaterialYouDark_darker_titlebar"
    # open kwinrulesrc file
    kwin_rules = configparser.ConfigParser(allow_no_value=True)
    kwin_rules.optionxform = str
    kwin_rules.read(settings.KWIN_RULES_RC)
    # Handle incomplete structure
    if "General" not in kwin_rules:
        kwin_rules.add_section("General")
    if "rules" not in kwin_rules["General"]:
        kwin_rules.set("General", "rules", None)
    # Get active rules
    active_rules = kwin_rules["General"]["rules"]
    if active_rules is None:
        active_rules = []
    else:
        active_rules = active_rules.split(",")

    # Check if rule already exists, if not make it
    rule_exists = False
    for rule in active_rules:
        try:
            rule_description = kwin_rules[rule]["Description"]
            # if rule description matches save the rule id
            if (
                rule_description
                == "Darker Titlebar - generated by kde-material-you-colors, do not rename"
            ):
                rule_id = rule
                rule_exists = True
                break
        except:
            pass
        # print(rule_description)

    # increment rules counter if the rule is being created
    if not rule_exists:
        rule_id = str(len(active_rules) + 1)
        kwin_rules["General"]["count"] = rule_id
        active_rules.append(rule_id)

    # add the new rule if doesn't exist
    if not kwin_rules.has_section(rule_id):
        kwin_rules.add_section(rule_id)
    # set the Description
    kwin_rules[rule_id][
        "Description"
    ] = "Darker Titlebar - generated by kde-material-you-colors, do not rename"
    # Set the scheme name
    # iterate between the color scheme and its copy
    # eliminating the necessity of a second kwin reload
    # tough a bit uglier to show yet another copy in the system settings...
    if "decocolor" in kwin_rules[rule_id]:
        if kwin_rules[rule_id]["decocolor"] == scheme_name:
            scheme_name = scheme_name + "2"
    kwin_rules[rule_id]["decocolor"] = scheme_name
    # Force color rule
    kwin_rules[rule_id]["decocolorrule"] = "2"
    # Use regular expression
    kwin_rules[rule_id]["wmclassmatch"] = "3"
    # Set regular expression
    kwin_rules[rule_id]["wmclass"] = f"({darker_window_list.replace(' ','|')})"
    # Update active rules list
    kwin_rules["General"]["rules"] = string_utils.tup2str(active_rules)
    # Write

    with open(settings.KWIN_RULES_RC, "w") as configfile:
        kwin_rules.write(configfile, space_around_delimiters=False)
