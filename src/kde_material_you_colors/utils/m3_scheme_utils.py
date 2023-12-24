import json
import logging
import os
from PIL import Image
from .. import settings
from . import color_utils
from . import math_utils
from . import notify
from .wallpaper_utils import WallpaperReader
from .extra_image_utils import pixelsFromImage

from .m3_theme_utils import themeFromSourceColorCli


def dict_to_rgb(dark_scheme):
    out = {}
    for key, color in dark_scheme.items():
        out.update({key: color_utils.hexFromArgb(color)})
    return out


def tones_from_palette(palette):
    # print(palette)
    tones = {}
    for x in range(100):
        tones.update({x: palette[str(x)]})
    return tones


def get_custom_colors(custom_colors):
    colors = {}
    for custom_color in custom_colors:
        value = color_utils.hexFromArgb(custom_color["color"]["value"])
        colors.update(
            {
                value: {
                    "color": dict_to_rgb(custom_color["color"]),
                    "value": color_utils.hexFromArgb(custom_color["value"]),
                    "light": dict_to_rgb(custom_color["light"]),
                    "dark": dict_to_rgb(custom_color["dark"]),
                }
            },
        )
    return colors


def get_material_you_colors(
    wallpaper_data,
    ncolor,
    source_type,
    custom_colors,
    scheme_type,
    light_chroma_multiplier=1,
    dark_chroma_multiplier=1,
):
    """Get material you colors from wallpaper or hex color using material_color_utilities

    Args:
        wallpaper_data (tuple): wallpaper (type and data)
        ncolor (int): Alternative color number flag passed to material_color_utilities
        source_type (str): image or color string passed to material_color_utilities

    Returns:
        str: string data from python-material-color-utilities
    """
    logging.warning(f"{light_chroma_multiplier}, {dark_chroma_multiplier}")
    try:
        if source_type == "image":
            # open image file
            img = Image.open(wallpaper_data)
            # resize image proportionally
            basewidth = 128
            wpercent = basewidth / float(img.size[0])
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            # get pixels
            source_pixels = pixelsFromImage(img)
            # close image file
            img.close()
        else:
            source_pixels = [color_utils.argbFromHex(wallpaper_data)]

        # logging.warning(source_pixels)
        source_info = {
            "pixels": source_pixels,
            "ncolor": ncolor,
            "custom_colors": [
                color_utils.argbFromHex(color) for color in custom_colors
            ],
            "scheme_type": scheme_type,
            "mult": {
                "chroma": {
                    "light": light_chroma_multiplier,
                    "dark": dark_chroma_multiplier,
                },
                "tone": 1,
            },
        }
        theme = themeFromSourceColorCli(source_info)

        dark_scheme = theme["schemes"]["dark"]
        light_scheme = theme["schemes"]["light"]
        # primary_palete = theme["palettes"]["light"]["primary"]
        # secondary_palete = theme["palettes"]["light"]["secondary"]
        # tertiary_palete = theme["palettes"]["light"]["tertiary"]
        # neutral_palete = theme["palettes"]["light"]["neutral"]
        # neutral_variant_palete = theme["palettes"]["light"]["neutralVariant"]
        # error_palette = theme["palettes"]["light"]["error"]

        materialYouColors = {
            "best": theme["best"],
            "source": theme["source"],
            "schemes": {
                "light": light_scheme,
                "dark": dark_scheme,
            },
            "palettes": {
                "light": {
                    "primary": theme["palettes"]["light"]["primary"],
                    "secondary": theme["palettes"]["light"]["secondary"],
                    "tertiary": theme["palettes"]["light"]["tertiary"],
                    "neutral": theme["palettes"]["light"]["neutral"],
                    "neutralVariant": theme["palettes"]["light"]["neutralVariant"],
                    "error": theme["palettes"]["light"]["error"],
                },
                "dark": {
                    "primary": theme["palettes"]["dark"]["primary"],
                    "secondary": theme["palettes"]["dark"]["secondary"],
                    "tertiary": theme["palettes"]["dark"]["tertiary"],
                    "neutral": theme["palettes"]["dark"]["neutral"],
                    "neutralVariant": theme["palettes"]["dark"]["neutralVariant"],
                    "error": theme["palettes"]["dark"]["error"],
                },
            },
            "custom": theme["customColors"],
        }
        return materialYouColors

    except Exception as e:
        error = f"Error trying to get colors from {wallpaper_data}: {e}"
        logging.exception(error)
        notify.send_notification("Could not get colors", error)
        return None


def get_color_schemes(
    wallpaper: WallpaperReader,
    ncolor=None,
    custom_colors=None,
    scheme_type=0,
    light_chroma_multiplier=1,
    dark_chroma_multiplier=1,
):
    """Display best colors, allow to select alternative color,light_chroma_multiplier,
                        dark_chroma_multiplier,
    and make and apply color schemes for dark and light mode

    Args:
        wallpaper (tuple): wallpaper (type and data)
        ncolor (int): Alternative color number flag passed to material-color-utility

    Returns:

    """
    if custom_colors is None:
        custom_colors = []
    if wallpaper is not None:
        materialYouColors = None
        wallpaper_type = wallpaper.type
        wallpaper_data = wallpaper.source
        if wallpaper_type in ["image", "screenshot"]:
            if wallpaper_data and os.path.exists(wallpaper_data):
                if not os.path.isdir(wallpaper_data):
                    materialYouColors = get_material_you_colors(
                        wallpaper_data,
                        ncolor=ncolor,
                        source_type="image",
                        custom_colors=custom_colors,
                        scheme_type=scheme_type,
                        light_chroma_multiplier=light_chroma_multiplier,
                        dark_chroma_multiplier=dark_chroma_multiplier,
                    )
                else:
                    logging.error(f'"{wallpaper_data}" is a directory, aborting')

        elif wallpaper_type == "color":
            if wallpaper_data:
                wallpaper_data = color_utils.color2hex(wallpaper_data)
                materialYouColors = get_material_you_colors(
                    wallpaper_data,
                    ncolor=ncolor,
                    source_type=wallpaper_type,
                    custom_colors=custom_colors,
                    scheme_type=scheme_type,
                    light_chroma_multiplier=light_chroma_multiplier,
                    dark_chroma_multiplier=dark_chroma_multiplier,
                )

        if materialYouColors is not None:
            try:
                if len(materialYouColors["best"]) > 1:
                    best_colors = f"Best colors: {settings.TERM_STY_BOLD}"

                    for i, color in enumerate(materialYouColors["best"]):
                        rgb = color_utils.hex2rgb(color)
                        preview = (
                            f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]};1m{color} \033[0m"
                        )
                        best_colors += f"{settings.TERM_COLOR_DEF+settings.TERM_STY_BOLD}{i}:{preview}"
                    logging.info(best_colors[:-5])

                source = materialYouColors["source"]
                sedColor = source["color"]
                seedNo = source["index"]
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
