import operator
import numpy
import colorsys
from material_color_utilities_python.utils.theme_utils import *


def hex2rgb(hex):
    hex = hex.lstrip('#')
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    #print(f'{rgb} {type(rgb)}')
    return rgb


def rgb2hex(r, g, b):
    hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return hex

# Blend RGB colors using Oklab
# Adapted from https://github.com/ProtonAOSP/android_frameworks_base/commit/28cc1ae1b1436120f111f1e21ca62e1fc9e0a7df


def cube(x):
    x = float(x)
    return x * x * x

# Linear -> sRGB


def srgbTransfer(x):
    x = float(x)
    if x >= 0.0031308:
        return 1.055 * float(numpy.power(x, (1.0 / 2.4)) - 0.055)
    else:
        return 12.92 * x

# sRGB -> Linear


def srgbTransferInv(x):
    x = float(x)
    if x >= 0.04045:
        return float(numpy.power(((x + 0.055) / 1.055), 2.4))
    else:
        return x / 12.92


def srgbRed(redInt):
    return srgbTransferInv(redInt / 255.0)


def srgbGreen(greenInt):
    return srgbTransferInv(greenInt / 255.0)


def srgbBlue(blueInt):
    return srgbTransferInv(blueInt / 255.0)


def srgbTransferToInt(c):
    c = float(c)
    res = numpy.round(srgbTransfer(c) * 255.0)
    if res < 0:
        return 0
    elif res > 255:
        return 255
    else:
        return res


def rgbToOklabLp(r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    return float(numpy.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b))


def rgbToOklabMp(r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    return float(numpy.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b))


def rgbToOklabSp(r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    return float(numpy.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b))


def blendColors(colorA, colorB, ratio):
    inverseRatio = 1 - ratio

    [r1, g1, b1] = hex2rgb(colorA)
    [r2, g2, b2] = hex2rgb(colorB)

    r1 = srgbRed(r1)
    g1 = srgbRed(g1)
    b1 = srgbRed(b1)

    lp1 = rgbToOklabLp(r1, g1, b1)
    mp1 = rgbToOklabMp(r1, g1, b1)
    sp1 = rgbToOklabSp(r1, g1, b1)

    r2 = srgbRed(r2)
    g2 = srgbRed(g2)
    b2 = srgbRed(b2)

    lp2 = rgbToOklabLp(r2, g2, b2)
    mp2 = rgbToOklabMp(r2, g2, b2)
    sp2 = rgbToOklabSp(r2, g2, b2)

    l = cube(lp1 * inverseRatio + lp2 * ratio)
    m = cube(mp1 * inverseRatio + mp2 * ratio)
    s = cube(sp1 * inverseRatio + sp2 * ratio)

    r = int(srgbTransferToInt(+4.0767416621 * l -
            3.3077115913 * m + 0.2309699292 * s))
    g = int(srgbTransferToInt(-1.2684380046 * l +
            2.6097574011 * m - 0.3413193965 * s))
    b = int(srgbTransferToInt(-0.0041960863 * l -
            0.7034186147 * m + 1.7076147010 * s))

    return rgb2hex(r, g, b)


def hex2alpha(solid_color, opacity):
    opacity = int(numpy.ceil(opacity*2.55))
    aa = f'{opacity:x}'
    if len(aa) == 1:
        aa = f'0{aa}'
    argb = solid_color.replace('#', f'#{aa}')
    return argb


def rgb2alpha(rgb, opacity):
    opacity = int(numpy.ceil(opacity*2.55))
    rgba = (rgb[0], rgb[1], rgb[2], opacity)
    return rgba


def hex2rgba(hex, opacity):
    hex = hex.lstrip('#')
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    rgba = rgb2alpha(rgb, opacity)
    return rgba


def color_luminance(color):
    r, g, b = hex2rgb(color)
    lum = 0.2126 * srgbRed(r) + 0.7152 * srgbGreen(g) + 0.0722 * srgbBlue(b)
    #print("Luminance:", lum)
    return (color, lum)


def sort_colors_luminance(colors, reverse=False):
    first_color = colors[0]
    all_colors = colors
    # print(f"Sorting colors by luminance: {colors}")
    colors_with_luminance = []
    sorted_colors = ()
    for color in colors:
        colors_with_luminance.append(color_luminance(color))
    colors_with_luminance.sort(key=operator.itemgetter(1), reverse=reverse)

    for color in colors_with_luminance:
        #print(color[0], color[1])
        sorted_colors += color[0],
    # print(colors_with_luminance)
    # print(sorted_colors)
    # print(f"Sorted colors: {sorted_colors}")
    return sorted_colors


def contrast_ratio(lighter_color, darker_color):
    l1 = float(color_luminance(lighter_color)[1])
    l2 = float(color_luminance(darker_color)[1])
    contrast_ratio = (l1+0.05)/(l2+0.05)
    return contrast_ratio


def blend2contrast(lighter_color, darker_color, blend_color, min_contrast, blend_step, dark=True):
    # print(f"Test blend2contrast {lighter_color} {darker_color} {blend_color} 4.5 0.1")

    if dark:
        contrast = contrast_ratio(lighter_color, darker_color)
    else:
        contrast = contrast_ratio(darker_color, lighter_color)

    if contrast < min_contrast:
        blend_ratio = 0.0

        while contrast < 4.5:
            blend_ratio += blend_step
            if dark:
                new = blendColors(lighter_color, blend_color, blend_ratio)
                contrast = contrast_ratio(new, darker_color)
            else:
                new = blendColors(lighter_color, blend_color, blend_ratio)
                contrast = contrast_ratio(darker_color, new)
            # print(f"new: {new} vs {darker_color} blend: {blend_ratio} contrast: {contrast}")
        return new
    else:
        return blendColors(lighter_color, blend_color, .12)


def scale_lightness(hex_color, amount):
    r, g, b = hex2rgb(hex_color)
    # convert rgb to hls
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    # manipulate value and convert back to rgb
    r, g, b = colorsys.hsv_to_rgb(h, s, amount)
    o_hex = rgb2hex(int(r), int(g), int(b))
    # print(f"scale_lightness color: {hex_color} * amount: {amount} = {o_hex}")
    return o_hex


def lighteen_color(hex_color, min, blend):
    current_luminance = color_luminance(hex_color)[1]
    # print(f"original luminance: {current_luminance}")
    if current_luminance < min:
        new_lightness = 255.0*(1.0-current_luminance)
        # print(f increase lightness to {new_lightness}")
        new_color = scale_lightness(hex_color, new_lightness)
    else:
        new_color = hex_color
    o = blendColors(new_color, blend, 0.2)
    # print(f"result after blend: {o}")
    return o


def scale_saturation(hex_color, amount):
    r, g, b = hex2rgb(hex_color)
    # convert rgb to hls
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    # manipulate value and convert back to rgb
    r, g, b = colorsys.hsv_to_rgb(h, amount, v)
    o_hex = rgb2hex(int(r), int(g), int(b))
    # print(f"scale_lightness color: {hex_color} * amount: {amount} = {o_hex}")
    return o_hex


# Tests
if __name__ == '__main__':
    # Test color blend
    print("> Test color blend #ff0000 , #00ff00")
    print(blendColors('#ff0000', "#00ff00", .01))
    print(blendColors('#ff0000', "#00ff00", .25))
    print(blendColors('#ff0000', "#00ff00", .5))
    print(blendColors('#ff0000', "#00ff00", .75))
    print(blendColors('#ff0000', "#00ff00", .99))

    print("> Test color hex2alpha '#ff0000',50")
    print(hex2alpha('#ff0000', 50))

    color1hex = '#082523'
    color1rgb = hex2rgb(color1hex)
    color1rgb_alpha = rgb2alpha(color1rgb, 200)

    print("> Test color rgb2alpha")
    print(color1rgb_alpha)
    print("> Test color hex2rgba")
    color1rgba = hex2rgba(color1hex, 200)
    print(color1rgba)
    print("> Test color_luminance")
    print(color_luminance(color1hex))

    colors_list = ('#f96767', '#222250', '#ff8400',
                   '#ffd500', '#00fffb', '#c1f7fb', '#00eeff')
    print("> Test sort_colors_luminance '#f96767','#222250','#ff8400','#ffd500','#00fffb','#c1f7fb','#00eeff'")
    print(sort_colors_luminance(colors_list))

    print("> Test contrast_ratio '#475AC6','#1A1A22'")
    print(contrast_ratio('#475AC6', '#1A1A22'))

    print("> Test blend2contrast '#475AC6','#1A1A22','#c1f7fb',4.5 ,0.1, True")
    print(blend2contrast('#475AC6', '#1A1A22', '#c1f7fb', 4.5, 0.1, True))
    print("> Test blend2contrast '#e1ffb4','#FEFCF5','#060605', 4.5, 0.01, False")
    print(blend2contrast('#e1ffb4', '#FEFCF5', '#060605', 4.5, 0.01, False))

    print("> Oklab vs cam16 blend '#ff0000', '#0000ff', .5")
    print(f"oklab: {blendColors('#ff0000', '#0000ff', .5)}")
    print(
        f"cam16: {hexFromArgb(Blend.cam16Ucs(argbFromHex('#ff0000'),argbFromHex('#0000ff'),0.5))}")

    print("> lighteen_color '#b70708',.15,'#ffffff'")
    print(lighteen_color('#b70708', .15, '#ffffff'))

    test_colors = ['#000000',
                   '#4141a6',
                   '#1dc136',
                   '#bbb13c',
                   '#ed19cd',
                   '#e40f0f',
                   '#fe6c0b',
                   '#fff000',
                   '#36e5d3',
                   '#131aed',
                   '#ff0000',
                   '#00ff00',
                   '#0000ff',
                   '#ffffff'
                   ]

    for color in test_colors:
        print(color_luminance(color))
