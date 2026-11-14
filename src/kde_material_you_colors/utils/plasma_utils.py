import configparser
import logging
import os
import subprocess
from kde_material_you_colors import settings
from kde_material_you_colors.utils import file_utils
from kde_material_you_colors.schemeconfigs import ThemeConfig
from kde_material_you_colors.config import Configs
from kde_material_you_colors.utils.utils import Watcher
from kde_material_you_colors.utils import plasma_utils


def make_scheme(schemes: ThemeConfig):
    # Make sure the schemes path exists
    if not os.path.exists(settings.USER_SCHEMES_PATH):
        os.makedirs(settings.USER_SCHEMES_PATH)
    light_scheme = schemes.get_light_scheme()
    dark_scheme = schemes.get_dark_scheme()
    # plasma-apply-colorscheme doesnt allow to apply the same theme twice to reload
    # since I don't know how to reaload it with code lets make a copy and switch between them
    # sadly color settings will show copies too

    with open(
        settings.THEME_LIGHT_PATH + "2.colors", "w", encoding="utf8"
    ) as light_scheme_file:
        light_scheme_file.write(light_scheme)
    with open(
        settings.THEME_LIGHT_PATH + ".colors", "w", encoding="utf8"
    ) as light_scheme_file:
        light_scheme_file.write(light_scheme)
    with open(
        settings.THEME_DARK_PATH + "2.colors", "w", encoding="utf8"
    ) as dark_scheme_file:
        dark_scheme_file.write(dark_scheme)
    with open(
        settings.THEME_DARK_PATH + ".colors", "w", encoding="utf8"
    ) as dark_scheme_file:
        dark_scheme_file.write(dark_scheme)

    plasma_darker_header(schemes)


def apply_color_schemes(light=False):
    color_scheme = settings.THEME_LIGHT_PATH if light else settings.THEME_DARK_PATH
    subprocess.run(
        "plasma-apply-colorscheme " + color_scheme + "2.colors",
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        check=False,
    )
    colorscheme_out = subprocess.check_output(
        "plasma-apply-colorscheme " + color_scheme + ".colors",
        shell=True,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    ).strip()
    logging.info(colorscheme_out)

    # Get hash of the updated theme
    colors_hash = file_utils.get_file_sha1(color_scheme + ".colors")

    # Update ColorSchemeHash using KDE configuration utility
    if colors_hash is not None:
        write_kde_config("ColorSchemeHash", colors_hash)


def set_icons(icons_light, icons_dark, light=False):
    """Set icon theme with plasma-changeicons for light and dark schemes

    Args:
        icons_light (str): Light mode icon theme
        icons_dark (str): Dark mode icon theme
        light (bool): wether using light or dark mode
    """

    icons = icons_light if light else icons_dark

    if icons and settings.PLASMA_CHANGEICONS_PATH:
        try:
            # Execute the command to change icons.
            changeicons_output = subprocess.check_output(
                [settings.PLASMA_CHANGEICONS_PATH, icons],
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            ).strip()
            logging.info(f"Icon theme changed to {icons}: {changeicons_output}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error changing icon theme to {icons}: {e.output}")
    else:
        if not icons:
            logging.debug("No icon theme specified.")
        if not settings.PLASMA_CHANGEICONS_PATH:
            logging.warning(
                f"{settings.CHANGE_ICONS_PROGRAM} wasn't found, can't apply icon themes."
            )


def set_plasma_style(style_light, style_dark, light=False):
    """Set plasma style with plasma-apply-desktoptheme

    Args:
        style_light (str): Light mode plasma style
        style_dark (str): Dark mode plasma style
        light (bool): wether using light or dark mode
    """

    style = style_light if light else style_dark

    if style:
        try:
            output = subprocess.check_output(
                [settings.PLASMA_APPLY_DESKTOP_THEME_BIN, style],
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            ).strip()
            logging.info(f"Plasma style changed to {style}: {output}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error changing plasma style to {style}: {e.output}")
    else:
        if not style:
            logging.debug("No plasma style theme specified.")

def kde_globals_light():
    """Return True for Material You Light, False for Dark, None if unknown."""
    color_scheme = read_kde_config("ColorScheme")

    if color_scheme is None:
        logging.warning("Could not detect KDE color scheme")
        return None

    if "MaterialYouLight" in color_scheme:
        return True

    if "MaterialYouDark" in color_scheme:
        return False

    logging.info(f"Unknown KDE color scheme: {color_scheme}")
    return None


def get_initial_mode():
    """Try to get the initial theme mode based based on the theme name,
    if failed try to get it from the stored hash and the current
    generated schemes.

    Returns:
        bool: Current mode light=True, dark=False
    """

    theme_from_name = kde_globals_light()

    if theme_from_name is not None:
        logging.info("Using theme from stored name")
        return theme_from_name

    logging.info(
        "Couldn't find theme by name, trying to resolve theme from last stored hash..."
    )

    current_theme_hash = read_kde_config("ColorSchemeHash")

    if current_theme_hash is not None:
        logging.debug(f"Config file hash: {current_theme_hash}")
        dark_scheme_hash = file_utils.get_file_sha1(
            settings.THEME_DARK_PATH + ".colors"
        )
        logging.debug(f"Dark scheme hash: {dark_scheme_hash}")
        light_scheme_hash = file_utils.get_file_sha1(
            settings.THEME_LIGHT_PATH + ".colors"
        )
        logging.debug(f"Light scheme hash: {light_scheme_hash}")
        if current_theme_hash == dark_scheme_hash:
            return False
        if current_theme_hash == light_scheme_hash:
            return True

    logging.warning("Couldn't find previus theme, falling back to dark mode...")
    return False


def plasma_darker_header(schemes):
    """Make a copy of the generated plasma themes but with darker headers

    Args:
        schemes (ThemeConfig): generated color schemes
    """
    light_color = schemes.get_wal_light_scheme()["special"]["background"]
    dark_color = schemes.get_wal_dark_scheme()["special"]["background"]
    color_scheme = configparser.ConfigParser()
    color_scheme.optionxform = str
    try:
        # Edit titlebar of dark scheme
        color_scheme.read(settings.THEME_DARK_PATH + ".colors")
        color_scheme["Colors:Header][Inactive"]["BackgroundNormal"] = dark_color
        color_scheme["Colors:Header"]["BackgroundNormal"] = dark_color
        color_scheme["General"]["Name"] = "Material You Dark (darker titlebar)"

        with open(
            settings.THEME_DARK_PATH + "_darker_titlebar.colors", "w", encoding="utf-8"
        ) as configfile:
            color_scheme.write(configfile, space_around_delimiters=False)
        color_scheme["General"]["Name"] = "Material You Dark (darker titlebar2)"
        with open(
            settings.THEME_DARK_PATH + "_darker_titlebar2.colors", "w", encoding="utf-8"
        ) as configfile:
            color_scheme.write(configfile, space_around_delimiters=False)

        # Edit titlebar of light scheme
        color_scheme.read(settings.THEME_LIGHT_PATH + ".colors")
        color_scheme["Colors:Header][Inactive"]["BackgroundNormal"] = light_color
        color_scheme["Colors:Header"]["BackgroundNormal"] = light_color
        color_scheme["General"]["Name"] = "Material You Light (darker titlebar)"

        with open(
            settings.THEME_LIGHT_PATH + "_darker_titlebar.colors", "w", encoding="utf-8"
        ) as configfile:
            color_scheme.write(configfile, space_around_delimiters=False)
        color_scheme["General"]["Name"] = "Material You Light (darker titlebar2)"
        with open(
            settings.THEME_LIGHT_PATH + "_darker_titlebar2.colors",
            "w",
            encoding="utf-8",
        ) as configfile:
            color_scheme.write(configfile, space_around_delimiters=False)

    except Exception as e:
        logging.error(f"Error:\n{e}")


def update_light_mode(config: Configs, light_mode_watcher: Watcher, first_run: bool):
    if config.read("light") is not None:
        light_mode_watcher.set_value(config.read("light"))

    elif first_run is True:
        light_mode_watcher.set_value(plasma_utils.get_initial_mode())

    else:
        detected_mode = plasma_utils.kde_globals_light()

        if detected_mode is not None:
            light_mode_watcher.set_value(detected_mode)

    return light_mode_watcher


def read_kde_config(key):
    """Read a value from KDE configuration.

    User configuration takes precedence over default configuration.
    """
    defaults_path = settings.KDE_GLOBALS_DEFAULTS
    user_path = settings.KDE_GLOBALS

    config = configparser.ConfigParser(interpolation=None)
    config.optionxform = str

    try:
        config.read(
            [defaults_path, user_path],
            encoding="utf-8",
        )

        value = config.get("General", key, fallback=None)

        return value.strip() if value else None

    except (configparser.Error, OSError) as e:
        logging.error(f"Error reading KDE config key '{key}': {e}")
        return None


def write_kde_config(key, value):
    """Write a value to the user KDE configuration."""
    user_path = settings.KDE_GLOBALS

    config = configparser.ConfigParser(interpolation=None)
    config.optionxform = str

    try:
        config.read(user_path, encoding="utf-8")

        if not config.has_section("General"):
            config.add_section("General")

        config.set("General", key, str(value))

        with open(user_path, "w", encoding="utf-8") as configfile:
            config.write(configfile, space_around_delimiters=False)

        return True

    except (configparser.Error, OSError) as e:
        logging.error(f"Error writing KDE config key '{key}': {e}")
        return False
