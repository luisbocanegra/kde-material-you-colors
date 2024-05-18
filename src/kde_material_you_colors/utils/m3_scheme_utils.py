import logging
import os
import json
from PIL import Image

from materialyoucolor.hct import Hct
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
from materialyoucolor.palettes.tonal_palette import TonalPalette
from materialyoucolor.dislike.dislike_analyzer import DislikeAnalyzer
from materialyoucolor.blend import Blend
from materialyoucolor.dynamiccolor.dynamic_color import DynamicColor
from materialyoucolor.utils.color_utils import argb_from_rgba
from kde_material_you_colors.utils.color_utils import rgb2hex
from kde_material_you_colors.utils.color_utils import argbFromHex
from kde_material_you_colors.utils.color_utils import hexFromArgb
from kde_material_you_colors import settings
from kde_material_you_colors.utils import color_utils
from kde_material_you_colors.utils import notify
from kde_material_you_colors.utils.wallpaper_utils import WallpaperReader
from kde_material_you_colors.utils.extra_image_utils import sourceColorsFromImage
from kde_material_you_colors.schemeconfigs import ThemeConfig
from kde_material_you_colors.utils.math_utils import clip


def dict_to_hex(dark_scheme):
    out = {}
    # print(dark_scheme)
    for key, [r, g, b, a] in dark_scheme.items():
        out.update({key: rgb2hex(r, g, b)})
    return out


def palette_to_hex(palette: TonalPalette):
    tones = []
    for x in range(100):
        tones.append(hexFromArgb(argb_from_rgba(palette.tone(x))))
    return tones


def custom_dynamic_color(
    custom_color,
    source_color=0,
    blend=True,
    scheme_variant=5,
    chroma_mult=1.0,
    tone_mult=1.0,
):
    value = custom_color["value"]
    value = DislikeAnalyzer.fix_if_disliked(Hct.from_int(value)).to_int()
    if custom_color["blend"]:
        value = Blend.harmonize(value, source_color)

    hct = Hct.from_int(value)
    scheme = getScheme(scheme_variant, hct, False, 0)
    schemeDark = getScheme(scheme_variant, hct, True, 0)
    colorsLight = getColors(scheme, chroma_mult, tone_mult)
    colorsDark = getColors(schemeDark, chroma_mult, tone_mult)

    return {
        "source": hexFromArgb(custom_color["value"]),
        "value": hexFromArgb(value),
        "blended": blend,
        "light": colorsLight,
        "dark": colorsDark,
        "palette": palette_to_hex(scheme.primary_palette),
    }


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


def getScheme(scheme_variant, source, isDark, contrastLevel):
    scheme_class = schemes[scheme_variant]
    return scheme_class(source, isDark, contrastLevel)


def getColors(scheme, chroma_mult, tone_mult):
    colors = {}
    for color in vars(MaterialDynamicColors).keys():
        color_name: DynamicColor = getattr(MaterialDynamicColors, color)
        if hasattr(color_name, "get_hct"):  # is a color
            argb = color_name.get_argb(scheme)
            hct = Hct(argb)
            hct.chroma = hct.chroma * clip(chroma_mult, 0, 10, 1)
            hct.tone = int(hct.tone * clip(tone_mult, 0.5, 1.5, 1))
            final = hct.to_int()
            colors[color] = hexFromArgb(final)
    return colors


def themeFromSourceColor(seed_color, scheme_variant=5, chroma_mult=1, tone_mult=1):
    source = Hct.from_int(seed_color)
    scheme = getScheme(scheme_variant, source, False, 0)
    schemeDark = getScheme(scheme_variant, source, True, 0)
    colorsLight = getColors(scheme, chroma_mult, tone_mult)
    colorsDark = getColors(schemeDark, chroma_mult, tone_mult)
    # Base text states taken from Breeze Color Scheme
    base_text_states = [
        {"name": "link", "value": argbFromHex("#2980b9"), "blend": False},
        {"name": "visited", "value": argbFromHex("#9b59b6"), "blend": False},
        {"name": "negative", "value": argbFromHex("#da4453"), "blend": False},
        {"name": "neutral", "value": argbFromHex("#f67400"), "blend": False},
        {"name": "positive", "value": argbFromHex("#27ae60"), "blend": False},
    ]

    cc = {}

    for color in base_text_states:
        cc[color["name"]] = custom_dynamic_color(
            color,
            argbFromHex(colorsDark["primary"]),
            True,
            6,
            chroma_mult,
            tone_mult,
        )

    out = {
        "source": seed_color,
        "schemes": {"light": colorsLight, "dark": colorsDark},
        "palettes": {
            "primary": palette_to_hex(scheme.primary_palette),
            "secondary": palette_to_hex(scheme.secondary_palette),
            "tertiary": palette_to_hex(scheme.tertiary_palette),
            "neutral": palette_to_hex(scheme.neutral_palette),
            "neutralVariant": palette_to_hex(scheme.neutral_variant_palette),
            "error": palette_to_hex(scheme.error_palette),
        },
        "customColors": cc,
    }
    return out


def get_material_you_colors(
    wallpaper_data, ncolor, source_type, scheme_variant, chroma_mult, tone_mult
):
    """Get material you colors from wallpaper or hex color using material-color-utility

    Args:
        wallpaper_data (tuple): wallpaper (type and data)
        ncolor (int): Alternative color number flag passed to material-color-utility
        source_type (str): image or color string passed to material-color-utility

    Returns:
        str: string data from python-material-color-utilities
    """

    try:
        source_color = 0
        if source_type == "image":
            # open image file
            img = Image.open(wallpaper_data)
            # resize image proportionally
            basewidth = 128
            wpercent = basewidth / float(img.size[0])
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            source_colors = sourceColorsFromImage(img)
            img.close()
            seed_color = source_colors[0]
        else:
            seed_color = argbFromHex(wallpaper_data)
            source_colors = [seed_color]

        best_colors = [hexFromArgb(color) for color in source_colors]

        # Given the best colors and the alt color index
        # return a selected color or the first one if index is out of bounds
        totalColors = len(best_colors)
        if ncolor is None or ncolor > totalColors - 1:
            ncolor = 0
        source_color = hexFromArgb(source_colors[ncolor])
        theme = themeFromSourceColor(
            argbFromHex(source_color), scheme_variant, chroma_mult, tone_mult
        )

        materialYouColors = {
            "best": best_colors,
            "seed": {
                "index": ncolor,
                "color": hexFromArgb(theme["source"]),
            },
            "schemes": {
                "light": theme["schemes"]["light"],
                "dark": theme["schemes"]["dark"],
            },
            "palettes": {
                "primary": theme["palettes"]["primary"],
                "secondary": theme["palettes"]["secondary"],
                "tertiary": theme["palettes"]["tertiary"],
                "neutral": theme["palettes"]["neutral"],
                "neutralVariant": theme["palettes"]["neutralVariant"],
                "error": theme["palettes"]["error"],
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
    scheme_variant=5,
    chroma_mult=1.0,
    tone_mult=1.0,
):
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
        if wallpaper_type in ["image", "screenshot"] and (
            wallpaper_data and os.path.exists(wallpaper_data)
        ):
            if os.path.isdir(wallpaper_data):
                logging.error(f'"{wallpaper_data}" is a directory, aborting')
                return None
            materialYouColors = get_material_you_colors(
                wallpaper_data,
                ncolor,
                "image",
                scheme_variant,
                chroma_mult,
                tone_mult,
            )

        elif wallpaper_type == "color" and wallpaper_data:
            color = color_utils.color2hex(wallpaper_data)
            materialYouColors = get_material_you_colors(
                color,
                ncolor,
                wallpaper_type,
                scheme_variant,
                chroma_mult,
                tone_mult,
            )

        if materialYouColors is not None:
            if len(materialYouColors["best"]) > 1:
                best_colors = f"Best colors: {settings.TERM_STY_BOLD}"
                for i, color in enumerate(materialYouColors["best"]):
                    rgb = color_utils.hex2rgb(color)
                    preview = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]};1m{color} \033[0m"
                    best_colors += (
                        f"{settings.TERM_COLOR_DEF+settings.TERM_STY_BOLD}{i}:{preview}"
                    )
                logging.info(best_colors[:-5])

            seed = materialYouColors["seed"]
            sedColor = seed["color"]
            seedNo = seed["index"]
            rgb = color_utils.hex2rgb(sedColor)
            preview = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]};1m{sedColor}\033[0m"
            logging.info(
                f"Using seed: {settings.TERM_COLOR_DEF+settings.TERM_STY_BOLD}{seedNo}:{preview}"
            )
            return materialYouColors


def export_schemes(theme: ThemeConfig):
    """Export generated schemes to MATERIAL_YOU_COLORS_JSON

    Args:
        schemes (ThemeConfig): generated color schemes
    """
    colors = theme.get_material_schemes()
    colors.update(
        {
            "extras": theme.get_extras(),
            "pywal": {
                "light": theme.get_wal_light_scheme(),
                "dark": theme.get_wal_dark_scheme(),
            },
        }
    )

    with open(
        settings.MATERIAL_YOU_COLORS_JSON, "w", encoding="utf8"
    ) as material_you_colors:
        json.dump(colors, material_you_colors, indent=4, ensure_ascii=False)
