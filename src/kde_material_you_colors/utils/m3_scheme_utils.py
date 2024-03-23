import logging
import os
import json
from PIL import Image

from materialyoucolor.hct import Hct
from kde_material_you_colors.utils.color_utils import argbFromHex
from kde_material_you_colors.utils.color_utils import hexFromArgb
from kde_material_you_colors.utils.color_utils import rgb2hex
from materialyoucolor.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot
from materialyoucolor.scheme.scheme_expressive import SchemeExpressive
from materialyoucolor.scheme.scheme_fruit_salad import SchemeFruitSalad
from materialyoucolor.scheme.scheme_monochrome import SchemeMonochrome
from materialyoucolor.scheme.scheme_rainbow import SchemeRainbow
from materialyoucolor.scheme.scheme_vibrant import SchemeVibrant
from materialyoucolor.scheme.scheme_neutral import SchemeNeutral
from materialyoucolor.scheme.scheme_fidelity import SchemeFidelity
from materialyoucolor.scheme.scheme_content import SchemeContent


from .. import settings
from . import color_utils
from . import math_utils
from . import notify
from .wallpaper_utils import WallpaperReader
from .extra_image_utils import sourceColorsFromImage


def dict_to_hex(dark_scheme):
    out = {}
    # print(dark_scheme)
    for key, [r, g, b, a] in dark_scheme.items():
        out.update({key: rgb2hex(r, g, b)})
    return out


def tones_from_palette(palette):
    tones = {}
    for x in range(100):
        tones.update({x: palette.tone(x)})
    return tones


schemes = [
    SchemeContent,
    SchemeExpressive,
    SchemeFidelity,
    SchemeMonochrome,
    SchemeNeutral,
    SchemeTonalSpot,
    SchemeVibrant,
    SchemeRainbow,
    SchemeFruitSalad,
]


def getScheme(scheme_type, source, isDark, contrastLevel):
    schene_class = schemes[scheme_type]
    return schene_class(source, isDark, contrastLevel)


def getColors(scheme):
    colors = {}
    for color in vars(MaterialDynamicColors).keys():
        color_name = getattr(MaterialDynamicColors, color)
        if hasattr(color_name, "get_hct"):  # is a color
            # print(color, hexFromArgb(color_name.get_argb(scheme)))
            colors[color] = hexFromArgb(color_name.get_argb(scheme))

    return colors


def themeFromSourceColor(seed_color):
    source = Hct.from_int(seed_color)
    scheme_type = 5
    scheme = getScheme(scheme_type, source, False, 0)
    schemeDark = getScheme(scheme_type, source, True, 0)
    colorsLight = getColors(scheme)
    colorsDark = getColors(schemeDark)

    out = {
        "source": seed_color,
        "schemes": {"light": colorsLight, "dark": colorsDark},
        "palettes": {
            "light": {
                "primary": dict_to_hex(tones_from_palette(scheme.primary_palette)),
                "secondary": dict_to_hex(tones_from_palette(scheme.secondary_palette)),
                "tertiary": dict_to_hex(tones_from_palette(scheme.tertiary_palette)),
                "neutral": dict_to_hex(tones_from_palette(scheme.neutral_palette)),
                "neutralVariant": dict_to_hex(
                    tones_from_palette(scheme.neutral_variant_palette)
                ),
                "error": dict_to_hex(tones_from_palette(scheme.error_palette)),
            },
            "dark": {
                "primary": dict_to_hex(tones_from_palette(schemeDark.primary_palette)),
                "secondary": dict_to_hex(
                    tones_from_palette(schemeDark.secondary_palette)
                ),
                "tertiary": dict_to_hex(
                    tones_from_palette(schemeDark.tertiary_palette)
                ),
                "neutral": dict_to_hex(tones_from_palette(schemeDark.neutral_palette)),
                "neutralVariant": dict_to_hex(
                    tones_from_palette(schemeDark.neutral_variant_palette)
                ),
                "error": dict_to_hex(tones_from_palette(schemeDark.error_palette)),
            },
        },
        "customColors": [],
    }
    return out


def get_custom_colors(custom_colors):
    colors = {}
    for custom_color in custom_colors:
        value = hexFromArgb(custom_color["color"]["value"])
        colors.update(
            {
                value: {
                    "color": dict_to_hex(custom_color["color"]),
                    "value": hexFromArgb(custom_color["value"]),
                    "light": dict_to_hex(custom_color["light"]),
                    "dark": dict_to_hex(custom_color["dark"]),
                }
            },
        )
    return colors


def get_material_you_colors(wallpaper_data, ncolor, source_type):
    """Get material you colors from wallpaper or hex color using material-color-utility

    Args:
        wallpaper_data (tuple): wallpaper (type and data)
        ncolor (int): Alternative color number flag passed to material-color-utility
        source_type (str): image or color string passed to material-color-utility

    Returns:
        str: string data from python-material-color-utilities
    """

    try:
        seedColor = 0
        if source_type == "image":
            # open image file
            img = Image.open(wallpaper_data)
            # resize image proportionally
            basewidth = 128
            wpercent = basewidth / float(img.size[0])
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            # get best colors
            source_colors = sourceColorsFromImage(img)
            # close image file
            img.close()
            seed_color = source_colors[0]
        else:
            seed_color = argbFromHex(wallpaper_data)
            source_colors = [seed_color]

        # best colors
        best_colors = {}
        for i, color in enumerate(source_colors):
            best_colors.update({str(i): hexFromArgb(color)})
        # generate theme from seed color

        # Given the best colors and the alt color index
        # return a selected color or the first one if index is out of bounds
        totalColors = len(best_colors)
        if ncolor is None:
            ncolor = 0
        if ncolor > totalColors - 1:
            ncolor = 0
        seedColor = hexFromArgb(source_colors[ncolor])

        theme = themeFromSourceColor(argbFromHex(seedColor))

        dark_scheme = theme["schemes"]["dark"]
        light_scheme = theme["schemes"]["light"]

        primary_palete_dark = theme["palettes"]["dark"]["primary"]
        secondary_palete_dark = theme["palettes"]["dark"]["secondary"]
        tertiary_palete_dark = theme["palettes"]["dark"]["tertiary"]
        neutral_palete_dark = theme["palettes"]["dark"]["neutral"]
        neutral_variant_palete_dark = theme["palettes"]["dark"]["neutralVariant"]
        error_palette_dark = theme["palettes"]["dark"]["error"]

        primary_palete = theme["palettes"]["dark"]["primary"]
        secondary_palete = theme["palettes"]["dark"]["secondary"]
        tertiary_palete = theme["palettes"]["dark"]["tertiary"]
        neutral_palete = theme["palettes"]["dark"]["neutral"]
        neutral_variant_palete = theme["palettes"]["dark"]["neutralVariant"]
        error_palette = theme["palettes"]["dark"]["error"]
        custom_colors = theme["customColors"]

        materialYouColors = {
            "best": best_colors,
            "seed": {
                ncolor: hexFromArgb(theme["source"]),
            },
            "schemes": {
                "light": light_scheme,
                "dark": dark_scheme,
            },
            "palettes": {
                "light": {
                    "primary": primary_palete,
                    "secondary": secondary_palete,
                    "tertiary": tertiary_palete,
                    "neutral": neutral_palete,
                    "neutralVariant": neutral_variant_palete,
                    "error": error_palette,
                },
                "dark": {
                    "primary": primary_palete_dark,
                    "secondary": secondary_palete_dark,
                    "tertiary": tertiary_palete_dark,
                    "neutral": neutral_palete_dark,
                    "neutralVariant": neutral_variant_palete_dark,
                    "error": error_palette_dark,
                },
            },
            "custom": [get_custom_colors(custom_colors)],
        }
        return materialYouColors

    except Exception as e:
        error = f"Error trying to get colors from {wallpaper_data}: {e}"
        logging.exception(error)
        notify.send_notification("Could not get colors", error)
        return None


def get_color_schemes(wallpaper: WallpaperReader, ncolor=None):
    """Display best colors, allow to select alternative color,
    and make and apply color schemes for dark and light mode

    Args:
        wallpaper (tuple): wallpaper (type and data)
        ncolor (int): Alternative color number flag passed to material-color-utility

    Returns:

    """
    if wallpaper is not None:
        materialYouColors = None
        wallpaper_type = wallpaper.type
        wallpaper_data = wallpaper.source
        if wallpaper_type in ["image", "screenshot"]:
            if wallpaper_data and os.path.exists(wallpaper_data):
                if not os.path.isdir(wallpaper_data):
                    materialYouColors = get_material_you_colors(
                        wallpaper_data, ncolor=ncolor, source_type="image"
                    )
                else:
                    logging.error(f'"{wallpaper_data}" is a directory, aborting')

        elif wallpaper_type == "color":
            if wallpaper_data:
                wallpaper_data = color_utils.color2hex(wallpaper_data)
                materialYouColors = get_material_you_colors(
                    wallpaper_data, ncolor=ncolor, source_type=wallpaper_type
                )

        if materialYouColors is not None:
            try:
                if len(materialYouColors["best"]) > 1:
                    best_colors = f"Best colors: {settings.TERM_STY_BOLD}"

                    for i, color in materialYouColors["best"].items():
                        rgb = color_utils.hex2rgb(color)
                        preview = (
                            f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]};1m{color} \033[0m"
                        )
                        best_colors += f"{settings.TERM_COLOR_DEF+settings.TERM_STY_BOLD}{i}:{preview}"
                    logging.info(best_colors[:-5])

                seed = materialYouColors["seed"]
                sedColor = list(seed.values())[0]
                seedNo = list(seed.keys())[0]
                rgb = color_utils.hex2rgb(sedColor)
                preview = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]};1m{sedColor}\033[0m"
                logging.info(
                    f"Using seed: {settings.TERM_COLOR_DEF+settings.TERM_STY_BOLD}{seedNo}:{preview}"
                )
                return materialYouColors

            except Exception as e:
                logging.exception(f"Error:\n{e}")
                return None


def export_schemes(schemes):
    """Export generated schemes to MATERIAL_YOU_COLORS_JSON

    Args:
        schemes (ThemeConfig): generated color schemes
    """
    colors = schemes.get_material_schemes()
    colors.update(
        {
            "extras": schemes.get_extras(),
            "pywal": {
                "light": schemes.get_wal_light_scheme(),
                "dark": schemes.get_wal_dark_scheme(),
            },
        }
    )

    with open(
        settings.MATERIAL_YOU_COLORS_JSON, "w", encoding="utf8"
    ) as material_you_colors:
        json.dump(colors, material_you_colors, indent=4, ensure_ascii=False)
