import logging

# C++ QuantizeCelebi
from materialyoucolor.quantize import QuantizeCelebi

# Material You's default scoring of colors
from materialyoucolor.score.score import Score
from materialyoucolor.score.score import ScoreOptions

SCORE_OPTIONS = ScoreOptions(
    desired=7,  # ANSI colors target
    fallback_color_argb=0xFF4285F4,  # Google Blue.
    filter=True,  # Avoid unsuitable colors.
    dislike_filter=True,  # Fix globally disliked colors
)


def sourceColorsFromImage(image):
    if image.mode == "RGB":
        image = image.convert("RGBA")
    if image.mode != "RGBA":
        logging.warning("Image not in RGB|RGBA format - Converting...")
        image = image.convert("RGBA")

    pixel_len = image.width * image.height
    image_data = image.getdata()
    quality = 1
    pixel_array = [image_data[_] for _ in range(0, pixel_len, quality)]

    # // Convert Pixels to Material Colors
    result = QuantizeCelebi(pixel_array, 128)
    ranked = Score.score(result, SCORE_OPTIONS)
    return ranked
