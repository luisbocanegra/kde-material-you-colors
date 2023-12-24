from material_color_utilities_python.quantize.quantizer_celebi import *
from material_color_utilities_python.score.score import *
from material_color_utilities_python.utils.color_utils import *
import logging


def pixelsFromImage(image) -> list:
    """Get pixels from image

    Args:
        image (Image): Wallpaper

    Returns:
        list: Pixels array in argb
    """
    # // Convert Image data to Pixel Array
    if image.mode == "RGB":
        image = image.convert("RGBA")
    if image.mode != "RGBA":
        logging.warning("Image not in RGB|RGBA format - Converting...")
        image = image.convert("RGBA")

    pixels = []
    for x in range(image.width):
        for y in range(image.height):
            # for the given pixel at w,h, lets check its value against the threshold
            pixel = image.getpixel((x, y))
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            a = pixel[3]
            if a < 255:
                continue
            argb = argbFromRgb(r, g, b)
            pixels.append(argb)

    return pixels
