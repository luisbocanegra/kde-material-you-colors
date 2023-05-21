from material_color_utilities_python.blend.blend import *
from material_color_utilities_python.palettes.core_palette import *
from material_color_utilities_python.utils.image_utils import *
from material_color_utilities_python.utils.string_utils import *
from .palettes.palettes import *
from .schemes.m3_schemes import *

# /**
#  * Generate custom color group from source and target color
#  *
#  * @param source Source color
#  * @param color Custom color
#  * @return Custom color group
#  *
#  * @link https://m3.material.io/styles/color/the-color-system/color-roles
#  */
# NOTE: Changes made to output format to be Dictionary
def customColor(source, color, palette_type):
    value = color["value"]
    from_v = value
    to = source
    if (color["blend"]):
        value = Blend.harmonize(from_v, to)
    palette = palette_type.of(value)
    tones = palette.a1
    return {
        "color": color,
        "value": value,
        "light": {
            "color": tones.tone(40),
            "onColor": tones.tone(100),
            "colorContainer": tones.tone(90),
            "onColorContainer": tones.tone(10),
        },
        "dark": {
            "color": tones.tone(80),
            "onColor": tones.tone(20),
            "colorContainer": tones.tone(30),
            "onColorContainer": tones.tone(90),
        },
    }

# /**
#  * Generate a theme from a source color
#  *
#  * @param source Source color
#  * @param customColors Array of custom colors
#  * @return Theme object
#  */
# NOTE: Changes made to output format to be Dictionary
def themeFromSourceColor(source, palette_type, customColors:list=[]):
    palette = palette_type.of(source)
    return {
        "source": source,
        "schemes": {
            "light": Scheme.light(source,palette_type),
            "dark": Scheme.dark(source,palette_type),
        },
        "palettes": {
            "primary": palette.a1,
            "secondary": palette.a2,
            "tertiary": palette.a3,
            "neutral": palette.n1,
            "neutralVariant": palette.n2,
            "error": palette.error,
        },
        "customColors": [customColor(source, c, palette_type) for c in customColors]
    }

# /**
#  * Generate a theme from an image source
#  *
#  * @param image Image element
#  * @param customColors Array of custom colors
#  * @return Theme object
#  */
def themeFromImage(image, palette_type, customColors = []):
    source = sourceColorFromImage(image)
    return themeFromSourceColor(source, palette_type, customColors)
