from array import array
import importlib
from pathlib import Path
import sys
from color_utils import blendColors
import subprocess
from themeconfigs import ThemeConfig

class ColorScheme:

    def __init__(self, colors):
        self._colors = colors

    def make_color_schemes(self, light):
        colors = self._colors

        # home folder
        home = str(Path.home())

        # Base text states taken from Breeze Color Scheme
        base_text_states = {
            "Link" : "#2980b9",
            "Visited": "#9b59b6",
            "Negative": "#da4453",
            "Neutral": "#f67400",
            "Positive": "#27ae60"
        }

        # Blend some extra colors by factor left(0.0) to right(1.0)
        extras = {
            "LightSurface1": blendColors(colors['light']['Surface'], colors['light']['Primary'], .08),
            "DarkSurface1": blendColors(colors['dark']['Surface'], colors['dark']['Primary'], .08),
            "LinkOnPrimaryLight": blendColors(colors['light']['OnPrimary'], base_text_states['Link'], .5),
            "LinkVisitedOnPrimaryLight": blendColors(colors['light']['OnPrimary'], base_text_states['Visited'], .8),
            "NegativeOnPrimaryLight": blendColors(colors['light']['OnPrimary'], base_text_states['Negative'], .8),
            "PositiveOnPrimaryLight": blendColors(colors['light']['OnPrimary'], base_text_states['Positive'], .8),
            "NeutralOnPrimaryLight": blendColors(colors['light']['OnPrimary'], base_text_states['Neutral'], .8),
            "LinkOnPrimaryDark": blendColors(colors['dark']['OnPrimary'], base_text_states['Link'], .5),
            "LinkVisitedOnPrimaryDark": blendColors(colors['dark']['OnPrimary'], base_text_states['Visited'], .8),
            "NegativeOnPrimaryDark": blendColors(colors['dark']['OnPrimary'], base_text_states['Negative'], .8),
            "PositiveOnPrimaryDark": blendColors(colors['dark']['OnPrimary'], base_text_states['Positive'], .8),
            "NeutralOnPrimaryDark": blendColors(colors['dark']['OnPrimary'], base_text_states['Neutral'], .8),
            "LightSelectionAlt": blendColors(colors['light']['Surface'], colors['light']['Secondary'], .3),
            "DarkSelectionAlt": blendColors(colors['dark']['Surface'], colors['dark']['Secondary'], .4),
        }

        # Load themes config on the go for now
        importlib.reload(sys.modules['themeconfigs'])
        from themeconfigs import ThemeConfig
        schemes = ThemeConfig(colors, extras, base_text_states)

        light_scheme=schemes.get_light_scheme()
        dark_scheme=schemes.get_dark_scheme()

        # plasma-apply-colorscheme doesnt allow to apply the same theme twice to reload
        # since I don't know how to reaload it with code lets make a copy and switch between them
        # sadly color settings will show copies too
        if light:
            with open (home+'/.local/share/color-schemes/MaterialYouLight.colors', 'w', encoding='utf8') as light_scheme_file:
                light_scheme_file.write(light_scheme)
            with open (home+'/.local/share/color-schemes/MaterialYouLight2.colors', 'w', encoding='utf8') as light_scheme_file:
                light_scheme_file.write(light_scheme)
            # os.system('plasma-apply-colorscheme /home/luis/.local/share/color-schemes/MaterialYouDark.colors')
            subprocess.Popen("plasma-apply-colorscheme "+home+"/.local/share/color-schemes/MaterialYouLight2.colors",
                                        shell=True, stderr=subprocess.PIPE,stdout=subprocess.DEVNULL)
            #time.sleep(1)
            subprocess.Popen("plasma-apply-colorscheme "+home+"/.local/share/color-schemes/MaterialYouLight.colors",
                                        shell=True, stderr=subprocess.PIPE,stdout=subprocess.DEVNULL)
            #os.system('plasma-apply-colorscheme /home/luis/.local/share/color-schemes/MaterialYouLight.colors')
        else:
            with open (home+'/.local/share/color-schemes/MaterialYouDark.colors', 'w', encoding='utf8') as dark_scheme_file:
                dark_scheme_file.write(dark_scheme)
            with open (home+'/.local/share/color-schemes/MaterialYouDark2.colors', 'w', encoding='utf8') as dark_scheme_file:
                dark_scheme_file.write(dark_scheme)
            # os.system('plasma-apply-colorscheme /home/luis/.local/share/color-schemes/MaterialYouDark.colors')
            subprocess.Popen("plasma-apply-colorscheme "+home+"/.local/share/color-schemes/MaterialYouDark2.colors",
                                        shell=True, stderr=subprocess.PIPE,stdout=subprocess.DEVNULL)
            #time.sleep(1)
            subprocess.Popen("plasma-apply-colorscheme "+home+"/.local/share/color-schemes/MaterialYouDark.colors",
                                        shell=True, stderr=subprocess.PIPE,stdout=subprocess.DEVNULL)
            #os.system('plasma-apply-colorscheme /home/luis/.local/share/color-schemes/MaterialYouLight.colors')
