import importlib
from pathlib import Path
import sys
import glob
import os
USER_HAS_PYWAL = importlib.util.find_spec("pywal") is not None
if USER_HAS_PYWAL:
    import pywal
from color_utils import blendColors
import subprocess
from schemeconfigs import ThemeConfig
HOME_DIR = str(Path.home())
THEME_LIGHT_PATH = HOME_DIR+"/.local/share/color-schemes/MaterialYouLight"
THEME_DARK_PATH = HOME_DIR+"/.local/share/color-schemes/MaterialYouDark"
class ColorScheme:

    def __init__(self, colors):
        self._colors = colors

    def make_color_schemes(self, light=None, pywal_light=None, wallpaper=None, pywal_material=True, use_pywal=False):
        wallpaper_type = wallpaper[0]
        wallpaper_data = wallpaper[1]
        colors = self._colors

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
            "LightSurface1": blendColors(colors['light']['Background'], colors['light']['Primary'], .08),
            "DarkSurface1": blendColors(colors['dark']['Background'], colors['dark']['Primary'], .05),
            
            "LightSurface2": blendColors(colors['light']['Background'], colors['light']['Primary'], .11),
            "DarkSurface2": blendColors(colors['dark']['Background'], colors['dark']['Primary'], .08),
            
            "LightSurface3": blendColors(colors['light']['Background'], colors['light']['Primary'], .14),
            "DarkSurface3": blendColors(colors['dark']['Background'], colors['dark']['Primary'], .11),
            
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
            
            "LightSelectionAlt": blendColors(colors['light']['Background'], colors['light']['Secondary'], .3),
            "DarkSelectionAlt": blendColors(colors['dark']['Background'], colors['dark']['Secondary'], .3),
            
            "LightSelectionAltActive": blendColors(colors['light']['Background'], colors['light']['Secondary'], .5),
            "DarkSelectionAltActive": blendColors(colors['dark']['Background'], colors['dark']['Secondary'], .5),
        }

        # Load themes config on the go for now
        importlib.reload(sys.modules['schemeconfigs'])
        from schemeconfigs import ThemeConfig
        schemes = ThemeConfig(colors, extras, base_text_states,wallpaper_data)

        light_scheme=schemes.get_light_scheme()
        dark_scheme=schemes.get_dark_scheme()

        # plasma-apply-colorscheme doesnt allow to apply the same theme twice to reload
        # since I don't know how to reaload it with code lets make a copy and switch between them
        # sadly color settings will show copies too
        if light == True:
            print("Setting light scheme")
            with open (THEME_LIGHT_PATH+"2.colors", 'w', encoding='utf8') as light_scheme_file:
                light_scheme_file.write(light_scheme)
            with open (THEME_LIGHT_PATH+".colors", 'w', encoding='utf8') as light_scheme_file:
                light_scheme_file.write(light_scheme)
            subprocess.run("plasma-apply-colorscheme "+THEME_LIGHT_PATH+"2.colors",
                                        shell=True, stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
            subprocess.run("plasma-apply-colorscheme "+THEME_LIGHT_PATH+".colors",
                                        shell=True, stderr=subprocess.PIPE)
        else:
            with open (THEME_DARK_PATH+"2.colors", 'w', encoding='utf8') as dark_scheme_file:
                dark_scheme_file.write(dark_scheme)
            with open (THEME_DARK_PATH+".colors", 'w', encoding='utf8') as dark_scheme_file:
                dark_scheme_file.write(dark_scheme)
            subprocess.run("plasma-apply-colorscheme "+THEME_DARK_PATH+"2.colors",
                                        shell=True, stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
            subprocess.run("plasma-apply-colorscheme "+THEME_DARK_PATH+".colors",
                                        shell=True, stderr=subprocess.PIPE)
        if use_pywal != None and use_pywal == True:
            if USER_HAS_PYWAL:
                if pywal_light != None:
                    if pywal_light  == True:
                        pywal_colors=schemes.get_wal_light_scheme()
                    else:
                        pywal_colors=schemes.get_wal_dark_scheme()
                elif light != None:
                    if light  == True:
                        pywal_colors=schemes.get_wal_light_scheme()
                    else:
                        pywal_colors=schemes.get_wal_dark_scheme()
                #use material you colors for pywal
                if pywal_material:
                    
                    # Apply the palette to all open terminals.
                    # Second argument is a boolean for VTE terminals.
                    # Set it to true if the terminal you're using is
                    # VTE based. (xfce4-terminal, termite, gnome-terminal.)
                    #print(pywal_colors)
                    pywal.sequences.send(pywal_colors, vte_fix=False)
                    
                    # Export all template files.
                    pywal.export.every(pywal_colors)

                    # Reload xrdb, i3 and polybar.
                    pywal.reload.env()
                    
                # TODO: remove this or make it optional
                elif wallpaper_data != None:
                    use_flag = ""
                    if pywal_light != None:
                        if pywal_light == True:
                            use_flag = "-l"
                    elif light != None:
                        if light == True:
                            use_flag = "-l"
                    subprocess.Popen("/usr/bin/wal -i "+wallpaper_data +" "+use_flag , shell=True, stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
                