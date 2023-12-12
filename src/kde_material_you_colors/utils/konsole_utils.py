import os
import subprocess
import configparser
import logging
import dbus
from .color_utils import hex2rgb
from .math_utils import clip
from .string_utils import tup2str
from .. import settings
from ..schemeconfigs import ThemeConfig


def export_scheme(
    light=None, pywal_light=None, schemes: ThemeConfig = None, konsole_opacity=100
):
    """Exports the color scheme files to the konsole configuration folder

    Args:
        light (_type_, optional): Light mode from plasma. Defaults to None.
        pywal_light (_type_, optional): Light mode from pywal setting. Defaults to None.
        schemes (ThemeConfig, optional): Theme configuration. Defaults to None.
        konsole_opacity (int, optional): Konsole background opacity. Defaults to 100.
    """
    # Make sure the konsole config path exists
    if not os.path.exists(settings.KONSOLE_DIR):
        os.makedirs(settings.KONSOLE_DIR)

    konsole_opacity = (
        100
        if konsole_opacity is None
        else float(clip(konsole_opacity, 0, 100, 100) / 100)
    )

    pywal_colors = (
        schemes.get_wal_light_scheme()
        if (pywal_light or light)
        else schemes.get_wal_dark_scheme()
    )

    config = configparser.ConfigParser()
    config.optionxform = str

    sections = [
        "Background",
        "BackgroundIntense",
        "BackgroundFaint",
        "Color",
        "Foreground",
        "ForegroundIntense",
        "ForegroundFaint",
        "General",
    ]

    for section in sections:
        if section == "Color":
            for n in range(8):
                config.add_section(str(f"Color{n}"))
                config.add_section(str(f"Color{n}Intense"))
                config.add_section(str(f"Color{n}Faint"))
        else:
            config.add_section(section)

    config["Background"]["Color"] = tup2str(
        hex2rgb(pywal_colors["special"]["background"])
    )
    config["BackgroundIntense"]["Color"] = tup2str(
        hex2rgb(pywal_colors["special"]["backgroundIntense"])
    )
    config["BackgroundFaint"]["Color"] = tup2str(
        hex2rgb(pywal_colors["special"]["backgroundFaint"])
    )

    for i in range(0, 8):
        config[f"Color{i}"]["Color"] = tup2str(
            hex2rgb(pywal_colors["colors"][f"color{i}"])
        )

    for i in range(0, 8):
        config[f"Color{i}Intense"]["Color"] = tup2str(
            hex2rgb(pywal_colors["colors"][f"color{i+8}"])
        )

    for i in range(0, 8):
        config[f"Color{i}Faint"]["Color"] = tup2str(
            hex2rgb(pywal_colors["colors"][f"color{i+16}"])
        )

    config["Foreground"]["Color"] = tup2str(
        hex2rgb(pywal_colors["special"]["foreground"])
    )
    config["ForegroundIntense"]["Color"] = tup2str(
        hex2rgb(pywal_colors["special"]["foregroundIntense"])
    )
    config["ForegroundFaint"]["Color"] = tup2str(
        hex2rgb(pywal_colors["special"]["foregroundFaint"])
    )

    config["General"]["Description"] = "MaterialYou"
    config["General"]["Opacity"] = str(konsole_opacity)

    with open(settings.KONSOLE_COLOR_SCHEME_PATH, "w", encoding="utf-8") as configfile:
        config.write(configfile, space_around_delimiters=False)

    # mirror color scheme
    config["General"]["Description"] = "MaterialYouAlt"

    with open(
        settings.KONSOLE_COLOR_SCHEME_ALT_PATH, "w", encoding="utf-8"
    ) as configfile:
        config.write(configfile, space_around_delimiters=False)


def apply_color_scheme():
    """Applies the color scheme to the existing default profile or a new one"""
    profile_name = set_default_profile(settings.KONSOLE_DEFAULT_THEMED_PROFILE)
    profile_path = settings.KONSOLE_DIR + profile_name + ".profile"
    create_profile(profile_path, profile_name)

    profile = configparser.ConfigParser()
    # preserve case
    profile.optionxform = str

    try:
        profile.read(profile_path)
        if "Appearance" not in profile:
            profile.add_section("Appearance")

        profile.set("Appearance", "ColorScheme", "MaterialYou")
        with open(profile_path, "w", encoding="utf-8") as configfile:
            profile.write(configfile, space_around_delimiters=False)

        # Clear the config settings and create the mirror profile as fallback
        # It will have the cloned color scheme (for color updating to work),
        # but inherit everything else from profile_name
        # Fixes the problem of configuration (like font) switching between the old and new
        # appearance when colors change and the profile switch kicks in.
        profile.clear()
        profile.add_section("Appearance")
        profile.add_section("General")
        profile.set("Appearance", "ColorScheme", "MaterialYouAlt")
        profile["General"]["Name"] = "TempMyou"
        profile["General"]["Parent"] = profile_name
        with open(settings.KONSOLE_TEMP_PROFILE, "w", encoding="utf-8") as configfile:
            profile.write(configfile, space_around_delimiters=False)

    except Exception as e:
        logging.exception(f"Error applying Konsole profile:\n{e}")

    reload_profile(profile_name)


def reload_profile(profile: str):
    """Reload the konsole profile for all running konsole sessions

    Args:
        profile (str): Konsole profile
    """
    bus = dbus.SessionBus()
    konsole_dbus_services = bus.list_names() or []
    # Get konsole instances (windows)
    konsole_dbus_services = [
        service for service in konsole_dbus_services if "org.kde.konsole" in service
    ]

    if konsole_dbus_services:
        logging.debug(
            f"Konsole services (windows) running ({len(konsole_dbus_services)}):"
        )
        for service in konsole_dbus_services:
            try:
                # get open sessions (tabs and splits)
                cmd = ["qdbus", service]
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    check=True,
                )

                sessions = [
                    line
                    for line in result.stdout.splitlines()
                    if line.startswith("/Sessions/")
                ]
                logging.debug(f"{service} ({len(sessions)} sessions)")

                # reload colors by switching profiles
                for session in sessions:
                    session_obj = bus.get_object(service, session)
                    session_iface = dbus.Interface(
                        session_obj, "org.kde.konsole.Session"
                    )
                    # logging.debug(f"{service}, {session} reading profile...")
                    current_profile = session_iface.profile()
                    # logging.debug(f"{current_profile}")
                    new_profile = "TempMyou" if profile == current_profile else profile

                    # logging.debug(f"{service}, {session} setting profile...")
                    session_iface.setProfile(new_profile)
                    # logging.debug("done")

            except dbus.exceptions.DBusException as e:
                logging.exception(f"{e}")
            except (FileNotFoundError, subprocess.CalledProcessError) as e:
                logging.exception(f"{e}")


def create_profile(profile_path, profile_name: str):
    """If the profile doesn't exist make it

    Args:
        profile_name (str): _description_
    """

    if not os.path.exists(profile_path):
        logging.info(f"Konsole profile '{profile_name}' doesn't exist, creating it")
        profile = configparser.ConfigParser()
        profile.optionxform = str
        profile.read(profile_path)
        profile.add_section("General")
        profile.add_section("Appearance")

        profile.set("General", "Name", profile_name)
        profile.set("General", "Parent", "FALLBACK/")

        profile.set("Appearance", "ColorScheme", "MaterialYou")

        with open(profile_path, "w", encoding="utf-8") as configfile:
            profile.write(configfile, space_around_delimiters=False)


def set_default_profile(profile_name):
    """If there is not default profile, set the generated one,
    if there is a default profile defined return it
    """

    if os.path.exists(settings.KONSOLE_RC):
        default_profile = get_default_profile()

        with open(settings.KONSOLE_RC, "r", encoding="utf-8") as f:
            contents = f.read()

            if default_profile:
                # it was defined, we will use it
                profile_name = default_profile
            else:
                if default_profile is None:
                    # means not defined
                    # we will add it
                    if "[Desktop Entry]" in contents:
                        logging.debug(
                            f"[Desktop Entry] found, appending profile '{profile_name}'"
                        )
                        contents = contents.replace(
                            "[Desktop Entry]",
                            f"[Desktop Entry]\nDefaultProfile={profile_name}.profile\n",
                        )
                    else:
                        logging.debug(
                            f"[Desktop Entry] not found, adding with profile '{profile_name}'"
                        )
                        contents += (
                            f"[Desktop Entry]\nDefaultProfile={profile_name}.profile\n"
                        )
                else:
                    # means it was empty
                    # we will set it
                    logging.debug(f"Setting default profile '{profile_name}'")
                    contents = contents.replace(
                        "DefaultProfile=", f"DefaultProfile={profile_name}.profile"
                    )

                with open(settings.KONSOLE_RC, "w", encoding="utf-8") as f:
                    f.write(contents)
    else:
        # konsolerc doesn't exist add it with the profile
        logging.debug(
            f"konsolerc wasn't found, creating it with default profile '{profile_name}.profile'"
        )
        with open(settings.KONSOLE_RC, "w", encoding="utf-8") as f:
            f.write(f"[Desktop Entry]\nDefaultProfile={profile_name}.profile\n")

    return profile_name


def get_default_profile() -> str | None:
    """Get default profile

    Returns:
        str|None: Default profile, empty string if not found, None if DefaultProfile is not in config
    """
    default_profile = None

    with open(settings.KONSOLE_RC, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("DefaultProfile="):
                part = line.split("=")[1].strip()
                if part:
                    logging.info(f"Found default profile '{part}'")
                default_profile = part.replace(".profile", "")

    return default_profile
