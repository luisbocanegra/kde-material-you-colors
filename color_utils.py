import numpy

def hex2rgb(hex):
        hex = hex.lstrip('#')
        rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
        return rgb
    
def rgb2hex(r,g,b):
    hex = "#{:02x}{:02x}{:02x}".format(r,g,b)
    return hex

# Blend two colors by an amount
def blendColors(colorA, colorB, amount):
    [rA, gA, bA] = hex2rgb(colorA)
    [rB, gB, bB] = hex2rgb(colorB)
    r = numpy.int(rA + (rB - rA) * amount)
    g = numpy.int(gA + (gB - gA) * amount)
    b = numpy.int(bA + (bB - bA) * amount)
    color = rgb2hex(r, g, b)
    return color