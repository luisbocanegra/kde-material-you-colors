import numpy
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

    r = int(srgbTransferToInt(+4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s))
    g = int(srgbTransferToInt(-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s))
    b = int(srgbTransferToInt(-0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s))

    return rgb2hex(r, g, b)

# Tests
if __name__ == '__main__':
    # Test color blend
    print(blendColors('#ff0000', "#00ff00", .01))
    print(blendColors('#ff0000', "#00ff00", .25))
    print(blendColors('#ff0000', "#00ff00", .5))
    print(blendColors('#ff0000', "#00ff00", .75))
    print(blendColors('#ff0000', "#00ff00", .99))
