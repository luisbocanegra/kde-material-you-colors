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
    if konsole_opacity is None:
        konsole_opacity = 100
    else:
        konsole_opacity = float(clip(konsole_opacity, 0, 100, 100) / 100)
    # print(f"konsole_opacity: {konsole_opacity}")
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

    config["General"]["Description"] = "MaterialYouAlt"

    with open(
        settings.KONSOLE_COLOR_SCHEME_ALT_PATH, "w", encoding="utf-8"
    ) as configfile:
        config.write(configfile, space_around_delimiters=False)


def make_mirror_profile(profile=None):
    if profile is not None:
        profile_path = settings.KONSOLE_DIR + profile + ".profile"
        if os.path.exists(profile_path):
            logging.info(f"Konsole profile: ({profile})")
            subprocess.check_output(
                "cp -f '" + profile_path + "' " + settings.KONSOLE_TEMP_PROFILE,
                shell=True,
            )
            profile = configparser.ConfigParser()
            # preserve case
            profile.optionxform = str
            if os.path.exists(profile_path):
                try:
                    profile.read(profile_path)
                    if "Appearance" not in profile:
                        profile.add_section("Appearance")

                    if profile["Appearance"]["ColorScheme"] != "MaterialYou":
                        profile["Appearance"]["ColorScheme"] = "MaterialYou"
                        with open(profile_path, "w", encoding="utf-8") as configfile:
                            profile.write(configfile, space_around_delimiters=False)
                except Exception as e:
                    logging.error(f"Error applying Konsole profile:\n{e}")

            # Mirror profile
            profile = configparser.ConfigParser()
            profile.optionxform = str
            if os.path.exists(settings.KONSOLE_TEMP_PROFILE):
                try:
                    profile.read(settings.KONSOLE_TEMP_PROFILE)
                    if "Appearance" not in profile:
                        profile.add_section("Appearance")
                    profile["Appearance"]["ColorScheme"] = "MaterialYouAlt"
                    profile["General"]["Name"] = "TempMyou"
                except Exception as e:
                    logging.error(f"Error applying Konsole profile:\n{e}")
                with open(
                    settings.KONSOLE_TEMP_PROFILE, "w", encoding="utf-8"
                ) as configfile:
                    profile.write(configfile, space_around_delimiters=False)


def reload_profile(profile=None):
    if profile is not None:
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
                        new_profile = (
                            "TempMyou" if profile == current_profile else profile
                        )

                        # logging.debug(f"{service}, {session} setting profile...")
                        session_iface.setProfile(new_profile)
                        # logging.debug("done")

                except dbus.exceptions.DBusException:
                    pass
                except (FileNotFoundError, subprocess.CalledProcessError) as e:
                    logging.error(f"{e}")


def apply_color_scheme(
    light=None, pywal_light=None, schemes=None, profile=None, konsole_opacity=None
):
    if profile is not None:
        profile_path = settings.KONSOLE_DIR + profile + ".profile"
        if os.path.exists(profile_path):
            export_scheme(light, pywal_light, schemes, konsole_opacity)
            reload_profile(profile)
        else:
            logging.error(f"Konsole Profile: {profile_path} does not exist")
