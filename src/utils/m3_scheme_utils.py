import logging
import os
import globals
if globals.USER_HAS_COLR:
    import colr
from . import color_utils
from . import math_utils
from .extra_image_utils import sourceColorsFromImage
from .m3_theme_utils import *
from .palettes.palettes import *
from material_color_utilities_python.palettes.core_palette import *


def dict_to_rgb(dark_scheme):
    out = {}
    for key, color in dark_scheme.items():
        out.update({key: hexFromArgb(color)})
    return out


def tones_from_palette(palette):
    tones = {}
    for x in range(100):
        tones.update({x: palette.tone(x)})
    return tones


def get_custom_colors(custom_colors):
    colors = {}
    for custom_color in custom_colors:
        value = hexFromArgb(custom_color['color']['value'])
        colors.update(
            {
                value: {
                    'color': dict_to_rgb(custom_color['color']),
                    'value': hexFromArgb(custom_color['value']),
                    'light': dict_to_rgb(custom_color['light']),
                    'dark': dict_to_rgb(custom_color['dark']),
                }
            },
        )
    return colors


def get_material_you_colors(wallpaper_data, ncolor, source_type,palette_type:int=0):
    """ Get material you colors from wallpaper or hex color using material-color-utility

    Args:
        wallpaper_data (tuple): wallpaper (type and data)
        ncolor (int): Alternative color number flag passed to material-color-utility
        source_type (str): image or color string passed to material-color-utility

    Returns:
        str: string data from python-material-color-utilities
    """

    palette_types = {
        0:{
            "name":"Core (default)",
            "palette":CorePalette
        },
        1:{
            "name":"Fidelity",
            "palette":FidelityPalette
        },
        2:{
            "name":"Monochrome",
            "palette":MonochromePalette
        },
        3:{
            "name":"Neutral",
            "palette":NeutralPalette
        },
        4:{
            "name":"Tonal Spot",
            "palette":TonalSpotPalette
        }
        }

    if palette_type > len(palette_types) - 1:
        palette_type = 0
    #print(palette_types)
    logging.info(f"Using {palette_type}:{palette_types[palette_type]['name']} palette")
    palette_type=palette_types[palette_type]['palette']

    try:
        seedColor = 0
        if source_type == "image":
            # open image file
            img = Image.open(wallpaper_data)
            # resize image proportionally
            basewidth = 64
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)
            # get best colors
            source_colors = sourceColorsFromImage(img, top=False)
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
        theme = themeFromSourceColor(source=seed_color,palette_type=palette_type)

        # Given a image, the alt color and hex color
        # return a selected color or a single color for hex code
        totalColors = len(best_colors)
        if ncolor and ncolor != None:
            ncolor = math_utils.clip(ncolor, 0, totalColors, 0)
        else:
            ncolor = 0

        if totalColors > ncolor:
            seedColor = hexFromArgb(source_colors[ncolor])
            seedNo = ncolor
        else:
            seedColor = hexFromArgb(source_colors[-1])
            seedNo = totalColors-1
        if seedColor != 0:
            theme = themeFromSourceColor(argbFromHex(seedColor),palette_type=palette_type)

        dark_scheme = json.loads(theme['schemes']['dark'].toJSON())
        light_scheme = json.loads(theme['schemes']['light'].toJSON())
        primary_palete = theme['palettes']['primary']
        secondary_palete = theme['palettes']['secondary']
        tertiary_palete = theme['palettes']['tertiary']
        neutral_palete = theme['palettes']['neutral']
        neutral_variant_palete = theme['palettes']['neutralVariant']
        error_palette = theme['palettes']['error']
        custom_colors = theme['customColors']

        materialYouColors = {
            'best': best_colors,
            'seed': {
                seedNo: hexFromArgb(theme['source']),
            },
            'schemes': {
                'light': dict_to_rgb(light_scheme),
                'dark': dict_to_rgb(dark_scheme),
            },
            'palettes': {
                'primary': dict_to_rgb(tones_from_palette(primary_palete)),
                'secondary': dict_to_rgb(tones_from_palette(secondary_palete)),
                'tertiary': dict_to_rgb(tones_from_palette(tertiary_palete)),
                'neutral': dict_to_rgb(tones_from_palette(neutral_palete)),
                'neutralVariant': dict_to_rgb(tones_from_palette(neutral_variant_palete)),
                'error': dict_to_rgb(tones_from_palette(error_palette)),
            },
            'custom': [
                get_custom_colors(custom_colors)
            ]
        }
        return materialYouColors

    except Exception as e:
        logging.error(
            f'Error trying to get colors from {wallpaper_data}:\n{e}')
        return None


def get_color_schemes(wallpaper, ncolor=None,palette_type:int=0):
    """ Display best colors, allow to select alternative color,
    and make and apply color schemes for dark and light mode

    Args:
        wallpaper (tuple): wallpaper (type and data)
        light (bool): wether use or not light scheme
        ncolor (int): Alternative color number flag passed to material-color-utility

    Returns:

    """
    if wallpaper != None:
        materialYouColors = None
        wallpaper_type = wallpaper[0]
        wallpaper_data = wallpaper[1]
        if wallpaper_type == "image":
            source_type = "image"
            if os.path.exists(wallpaper_data):
                if not os.path.isdir(wallpaper_data):
                    # get colors from material-color-utility
                    materialYouColors = get_material_you_colors(
                        wallpaper_data, ncolor=ncolor, source_type=source_type,palette_type=palette_type)
                else:
                    logging.error(
                        f'"{wallpaper_data}" is a directory, aborting')

        elif wallpaper_type == "color":
            source_type = "color"
            wallpaper_data = color_utils.color2hex(wallpaper_data)
            materialYouColors = get_material_you_colors(
                wallpaper_data, ncolor=ncolor, source_type=source_type,palette_type=palette_type)

        if materialYouColors != None:
            try:
                if len(materialYouColors['best']) > 1:
                    best_colors = f'Best colors: {globals.TERM_STY_BOLD}'

                    for index, col in materialYouColors['best'].items():
                        if globals.USER_HAS_COLR:
                            best_colors += f'{globals.TERM_COLOR_DEF+globals.TERM_STY_BOLD}{index}:{colr.color(col,fore=col)}'
                        else:
                            best_colors += f'{globals.TERM_COLOR_DEF+globals.TERM_STY_BOLD}{index}:{globals.TERM_COLOR_WHI}{col}'
                        if int(index) < len(materialYouColors['best'])-1:
                            best_colors = best_colors+","
                    logging.info(best_colors)

                seed = materialYouColors['seed']
                sedColor = list(seed.values())[0]
                seedNo = list(seed.keys())[0]
                if globals.USER_HAS_COLR:
                    logging.info(
                        f'Using seed: {globals.TERM_COLOR_DEF+globals.TERM_STY_BOLD}{seedNo}:{colr.color(sedColor, fore=sedColor)}')
                else:
                    logging.info(
                        f'Using seed: {globals.TERM_COLOR_DEF+globals.TERM_STY_BOLD}{seedNo}:{globals.TERM_COLOR_WHI}{sedColor}')

                return materialYouColors

            except Exception as e:
                logging.error(f'Error:\n{e}')
                return None

    else:
        logging.error(
            f'''Error: Couldn't set schemes with "{wallpaper_data}"''')
        return None


def export_schemes(schemes):
    """Export generated schemes to MATERIAL_YOU_COLORS_JSON

    Args:
        schemes (ThemeConfig): generated color schemes
    """
    colors = schemes.get_material_schemes()
    colors.update({
        "extras": schemes.get_extras(),
        "pywal": {
            "light": schemes.get_wal_light_scheme(),
            "dark": schemes.get_wal_dark_scheme()
        }
    })

    with open(globals.MATERIAL_YOU_COLORS_JSON, 'w', encoding='utf8') as material_you_colors:
        json.dump(colors, material_you_colors, indent=4, ensure_ascii=False)
