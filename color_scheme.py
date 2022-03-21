from array import array
import importlib
from pathlib import Path
import sys
import time
from colr import hex2rgb
from matplotlib.colors import rgb2hex
import numpy
from colorutils import Color
import subprocess
from themeconfigs import ThemeConfig
class ColorScheme:

    def __init__(self, colors):
        self._colors = colors

    # Blend two colors by an amount
    def blendColors(colorA, colorB, amount):
        [rA, gA, bA] = hex2rgb(colorA)
        [rB, gB, bB] = hex2rgb(colorB)
        r = numpy.int(rA + (rB - rA) * amount)
        g = numpy.int(gA + (gB - gA) * amount)
        b = numpy.int(bA + (bB - bA) * amount)
        color = Color((r, g, b))
        return color.hex

    def make_color_schemes(self):
        colors = self._colors

        # home folder
        home = str(Path.home())
        
        # Blend some extra colors
        extras = {
            "LightSurface1": ColorScheme.blendColors(colors['light']['Surface'], colors['light']['Primary'], .08),
            "DarkSurface1": ColorScheme.blendColors(colors['dark']['Surface'], colors['dark']['Primary'], .08)
        }
        # Load themes config on the go for now
        importlib.reload(sys.modules['themeconfigs'])
        from themeconfigs import ThemeConfig
        schemes = ThemeConfig(colors, extras)
        
        light_scheme=schemes.get_light_scheme()
        dark_scheme=schemes.get_dark_scheme()

        # plasma-apply-colorscheme doesnt allow to apply the same theme twice to reload
        # since I don't know how to reaload it with code lets make a copy and switch between them
        # sadly color settings will show copies too

        with open (home+'/.local/share/color-schemes/MaterialYouLight.colors', 'w', encoding='utf8') as light_scheme_file:
            light_scheme_file.write(light_scheme)
        with open (home+'/.local/share/color-schemes/MaterialYouLight2.colors', 'w', encoding='utf8') as light_scheme_file:
            light_scheme_file.write(light_scheme)

        with open (home+'/.local/share/color-schemes/MaterialYouDark.colors', 'w', encoding='utf8') as dark_scheme_file:
            dark_scheme_file.write(dark_scheme)
        with open (home+'/.local/share/color-schemes/MaterialYouDark2.colors', 'w', encoding='utf8') as dark_scheme_file:
            dark_scheme_file.write(dark_scheme)




        # os.system('plasma-apply-colorscheme /home/luis/.local/share/color-schemes/MaterialYouDark.colors')
        print(subprocess.Popen("plasma-apply-colorscheme "+home+"/.local/share/color-schemes/MaterialYouLight2.colors",
                                    shell=True, stdout=subprocess.PIPE,stderr=subprocess.DEVNULL).communicate()[0].decode('utf-8').strip())
        #time.sleep(1)
        print(subprocess.Popen("plasma-apply-colorscheme "+home+"/.local/share/color-schemes/MaterialYouLight.colors",
                                    shell=True, stdout=subprocess.PIPE,stderr=subprocess.DEVNULL).communicate()[0].decode('utf-8').strip())
        #os.system('plasma-apply-colorscheme /home/luis/.local/share/color-schemes/MaterialYouLight.colors')
