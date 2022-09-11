from material_color_utilities_python.quantize.quantizer_celebi import *
from material_color_utilities_python.score.score import *
from material_color_utilities_python.utils.color_utils import *
from PIL import Image

# /**
#  * Get the source color from an image.
#  *
#  * @param image The image element
#  * @param top wether or not return only one color
#  * @return Source color - the color most suitable for creating a UI theme
#  */


def sourceColorsFromImage(image, top=False):
    # // Convert Image data to Pixel Array
    # const imageBytes = await new Promise((resolve, reject) => {
    #     const canvas = document.createElement('canvas');
    #     const context = canvas.getContext('2d');
    #     if (!context) {
    #         return reject(new Error('Could not get canvas context'));
    #     }
    #     image.onload = () => {
    #         canvas.width = image.width;
    #         canvas.height = image.height;
    #         context.drawImage(image, 0, 0);
    #         resolve(context.getImageData(0, 0, image.width, image.height).data);
    #     };
    # });
    # // Convert Image data to Pixel Array
    # const pixels = [];
    # for (let i = 0; i < imageBytes.length; i += 4) {
    #     const r = imageBytes[i];
    #     const g = imageBytes[i + 1];
    #     const b = imageBytes[i + 2];
    #     const a = imageBytes[i + 3];
    #     if (a < 255) {
    #         continue;
    #     }
    #     const argb = argbFromRgb(r, g, b);
    #     pixels.push(argb);
    # }
    if (image.mode == 'RGB'):
        image = image.convert('RGBA')
    if (image.mode != 'RGBA'):
        print("Warning: Image not in RGB|RGBA format - Converting...")
        image = image.convert('RGBA')

    pixels = []
    for x in range(image.width):
        for y in range(image.height):
            # for the given pixel at w,h, lets check its value against the threshold
            pixel = image.getpixel((x, y))
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            a = pixel[3]
            if (a < 255):
                continue
            argb = argbFromRgb(r, g, b)
            pixels.append(argb)

    # // Convert Pixels to Material Colors
    result = QuantizerCelebi.quantize(pixels, 128)
    ranked = Score.score(result)
    if top == True:
        return ranked[0]
    else:
        return ranked
