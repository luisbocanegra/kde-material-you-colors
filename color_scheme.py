import importlib
from pathlib import Path
import sys
import glob
import os
USER_HAS_PYWAL = importlib.util.find_spec("pywal") is not None
if USER_HAS_PYWAL:
    import pywal
import subprocess
from schemeconfigs import ThemeConfig
HOME_DIR = str(Path.home())
THEME_LIGHT_PATH = HOME_DIR+"/.local/share/color-schemes/MaterialYouLight"
THEME_DARK_PATH = HOME_DIR+"/.local/share/color-schemes/MaterialYouDark"
class ColorScheme:

    def __init__(self, colors, light_blend_multiplier, dark_blend_multiplier):
        self._colors = colors
        self._light_blend_multiplier = light_blend_multiplier
        self._dark_blend_multiplier =  dark_blend_multiplier
    def make_color_schemes(self, light=None, pywal_light=None, wallpaper=None, pywal_material=True, use_pywal=False):
        wallpaper_type = wallpaper[0]
        wallpaper_data = wallpaper[1]
        colors = self._colors
        light_blend_multiplier = self._light_blend_multiplier
        dark_blend_multiplier = self._dark_blend_multiplier
        # Load themes config on the go for now
        importlib.reload(sys.modules['schemeconfigs'])
        from schemeconfigs import ThemeConfig
        schemes = ThemeConfig(colors,wallpaper_data,light_blend_multiplier=light_blend_multiplier, dark_blend_multiplier=dark_blend_multiplier)

        light_scheme=schemes.get_light_scheme()
        dark_scheme=schemes.get_dark_scheme()

        # plasma-apply-colorscheme doesnt allow to apply the same theme twice to reload
        # since I don't know how to reaload it with code lets make a copy and switch between them
        # sadly color settings will show copies too
        
        with open (THEME_LIGHT_PATH+"2.colors", 'w', encoding='utf8') as light_scheme_file:
                light_scheme_file.write(light_scheme)
        with open (THEME_LIGHT_PATH+".colors", 'w', encoding='utf8') as light_scheme_file:
            light_scheme_file.write(light_scheme)
        with open (THEME_DARK_PATH+"2.colors", 'w', encoding='utf8') as dark_scheme_file:
                dark_scheme_file.write(dark_scheme)
        with open (THEME_DARK_PATH+".colors", 'w', encoding='utf8') as dark_scheme_file:
            dark_scheme_file.write(dark_scheme)
                
        if light == True:
            subprocess.run("plasma-apply-colorscheme "+THEME_LIGHT_PATH+"2.colors",
                                        shell=True, stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
            subprocess.run("plasma-apply-colorscheme "+THEME_LIGHT_PATH+".colors",
                                        shell=True, stderr=subprocess.PIPE)
        else:
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
