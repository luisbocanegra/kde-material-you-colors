from array import array
from pathlib import Path
import time
from colr import hex2rgb
from matplotlib.colors import rgb2hex
import numpy
from colorutils import Color
import subprocess

class ColorScheme:
    
    def __init__(self, colors):
        self.colors = colors
        
    def blendColors(colorA, colorB, amount):
        [rA, gA, bA] = hex2rgb(colorA)
        [rB, gB, bB] = hex2rgb(colorB)
        r = numpy.int(rA + (rB - rA) * amount)
        g = numpy.int(gA + (gB - gA) * amount)
        b = numpy.int(bA + (bB - bA) * amount)
        color = Color((r, g, b))
        return color.hex
        
        
    def make_light_scheme(self):
        colors = self.colors
        #print(f'Colors light:\n{self.colors}')
        LightSurface1 = ColorScheme.blendColors(colors['light']['Surface'],colors['light']['Primary'],.08)
        
        DarkSurface1 = ColorScheme.blendColors(colors['dark']['Surface'],colors['dark']['Primary'],.08)
        
        #surface1 = ColorsHelper(colors['light']['Surface'],colors['light']['Primary'],1,0.05)
        surface1 = ColorScheme.blendColors(colors['light']['Surface'],colors['light']['Primary'],.08)

                
        light_scheme = f"""[ColorEffects:Disabled]
Color={LightSurface1}
ColorAmount=0.55
ColorEffect=3
ContrastAmount=0.65
ContrastEffect=0
IntensityAmount=0.1
IntensityEffect=0

[ColorEffects:Inactive]
ChangeSelectionColor=true
Color=#000fff
ColorAmount=1
ColorEffect=0
ContrastAmount=1
ContrastEffect=0
Enable=false
IntensityAmount=10
IntensityEffect=10

[Colors:Button]
BackgroundAlternate=255,89,125
BackgroundNormal={colors['light']['Surface']}
DecorationFocus={colors['light']['Primary']}
DecorationHover={colors['light']['Primary']}
ForegroundActive=#ffff00
ForegroundInactive=0,0,255
ForegroundLink=41,128,185
ForegroundNegative=39,120,110
ForegroundNeutral=95,125,205
ForegroundNormal={colors['light']['OnSurface']}
ForegroundPositive=156,83,198
ForegroundVisited=127,140,141

[Colors:Header]
BackgroundNormal={colors['light']['SecondaryContainer']}

[Colors:Selection]
BackgroundAlternate={colors['light']['Primary']}
BackgroundNormal={colors['light']['Primary']}
DecorationFocus={colors['light']['Primary']}
DecorationHover={colors['light']['Primary']}
ForegroundActive={colors['light']['OnPrimary']}
ForegroundInactive={colors['light']['OnPrimary']}
ForegroundLink=253,188,75
ForegroundNegative=67,205,189
ForegroundNeutral={colors['light']['OnPrimary']}
ForegroundNormal={colors['light']['OnPrimary']}
ForegroundPositive=156,83,198
ForegroundVisited=189,195,199

[Colors:Tooltip]
BackgroundAlternate=255,89,125
BackgroundNormal={colors['light']['Primary']}
DecorationFocus=255,99,118
DecorationHover=255,89,125
ForegroundActive=61,174,233
ForegroundInactive={colors['light']['OnPrimary']}
ForegroundLink=41,128,185
ForegroundNegative=67,205,189
ForegroundNeutral=95,125,205
ForegroundNormal=237,240,242
ForegroundPositive=156,83,198
ForegroundVisited=127,140,141

[Colors:View]
BackgroundAlternate={colors['light']['InverseOnSurface']}
BackgroundNormal={LightSurface1}
DecorationFocus={colors['light']['Primary']}
#-----------------------------------------------
DecorationHover={colors['light']['Primary']}
ForegroundActive={colors['light']['OnPrimary']}
ForegroundInactive={colors['light']['OnSurfaceVariant']}
ForegroundLink=31,140,236
ForegroundNegative={colors['light']['Error']}
ForegroundNeutral={colors['light']['InversePrimary']}
ForegroundNormal={colors['light']['OnSurfaceVariant']}
ForegroundPositive=156,83,198
ForegroundVisited=196,54,189

[Colors:Window]
BackgroundAlternate=#ff0000
BackgroundNormal={colors['light']['SecondaryContainer']}
DecorationFocus=#ff0000
DecorationHover=#00ff00
ForegroundActive=61,174,233
ForegroundInactive=75,79,85
ForegroundLink=41,128,185
ForegroundNegative=67,205,189
ForegroundNeutral={colors['light']['Primary']}
#---------------------------------------------------- Window header text all
ForegroundNormal={colors['light']['OnSurfaceVariant']}
ForegroundPositive=156,83,198
ForegroundVisited=127,140,141

[General]
ColorScheme=MaterialYouLight
Name=Material You Light
shadeSortColumn=false

[KDE]
contrast=5

[WM]
activeBackground={colors['light']['SecondaryContainer']}
activeBlend=#ff0000
activeForeground={colors['light']['OnSecondaryContainer']}
inactiveBackground={colors['light']['SecondaryContainer']}
inactiveBlend=#ff0000
inactiveForeground={colors['light']['OnSecondaryContainer']}
"""
        dark_scheme = f"""[ColorEffects:Disabled]
Color={DarkSurface1}
ColorAmount=0.55
ColorEffect=3
ContrastAmount=0.65
ContrastEffect=0
IntensityAmount=0.1
IntensityEffect=0

[ColorEffects:Inactive]
ChangeSelectionColor=false
Color=112,111,110
ColorAmount=-0.9
ColorEffect=0
ContrastAmount=0.1
ContrastEffect=0
Enable=true
IntensityAmount=0
IntensityEffect=0

[Colors:Button]
BackgroundAlternate=255,89,125
BackgroundNormal={colors['dark']['Secondary']}
DecorationFocus={colors['dark']['Primary']}
DecorationHover=255,89,125
ForegroundActive=#ffff00
ForegroundInactive=#ff0000
ForegroundLink=41,128,185
ForegroundNegative=39,120,110
ForegroundNeutral=95,125,205
ForegroundNormal={colors['dark']['OnSecondary']}
ForegroundPositive=156,83,198
ForegroundVisited=127,140,141

[Colors:Selection]
BackgroundAlternate={colors['dark']['Primary']}
BackgroundNormal={colors['dark']['Primary']}
DecorationFocus={colors['dark']['Primary']}
DecorationHover=255,89,125
ForegroundActive=252,252,252
ForegroundInactive=132,134,140
ForegroundLink=253,188,75
ForegroundNegative=67,205,189
ForegroundNeutral=95,125,205
ForegroundNormal={colors['dark']['OnPrimary']}
ForegroundPositive=156,83,198
ForegroundVisited=189,195,199

[Colors:Tooltip]
BackgroundAlternate=255,89,125
BackgroundNormal={colors['dark']['Primary']}
DecorationFocus=255,99,118
DecorationHover=255,89,125
ForegroundActive=61,174,233
ForegroundInactive=75,79,85
ForegroundLink=41,128,185
ForegroundNegative=67,205,189
ForegroundNeutral=95,125,205
ForegroundNormal=237,240,242
ForegroundPositive=156,83,198
ForegroundVisited=127,140,141

[Colors:View]
BackgroundAlternate=250,251,252
BackgroundNormal={DarkSurface1}
DecorationFocus={colors['dark']['Primary']}
DecorationHover={colors['dark']['Primary']}
ForegroundActive=61,174,233
ForegroundInactive=75,79,85
ForegroundLink=31,140,236
ForegroundNegative=67,205,189
ForegroundNeutral={colors['dark']['InversePrimary']}
ForegroundNormal={colors['dark']['OnSurface']}
ForegroundPositive=156,83,198
ForegroundVisited=127,140,141

[Colors:Window]
BackgroundAlternate=#ff0000
BackgroundNormal={colors['dark']['SecondaryContainer']}
DecorationFocus=#ff0000
DecorationHover=#00ff00
ForegroundActive=61,174,233
ForegroundInactive=75,79,85
ForegroundLink=41,128,185
ForegroundNegative=67,205,189
ForegroundNeutral={colors['dark']['InversePrimary']}
ForegroundNormal={colors['dark']['OnSurface']}
ForegroundPositive=156,83,198
ForegroundVisited=127,140,141

[General]
ColorScheme=MaterialYouDark
Name=Material You dark
shadeSortColumn=true

[KDE]
contrast=10

[WM]
activeBackground={colors['dark']['SecondaryContainer']}
activeBlend=183,186,195
activeForeground={colors['dark']['OnSecondaryContainer']}
inactiveBackground={colors['dark']['SecondaryContainer']}
inactiveBlend=247,249,249
inactiveForeground={colors['dark']['OnSecondaryContainer']}
"""
        #print(colors['light']['Primary'])
        
        home = str(Path.home())
        with open (home+'/.local/share/color-schemes/MaterialYouLight.colors', 'w', encoding='utf8') as light_scheme_file:
            light_scheme_file.write(light_scheme)
            
        home = str(Path.home())
        with open (home+'/.local/share/color-schemes/MaterialYouDark.colors', 'w', encoding='utf8') as dark_scheme_file:
            dark_scheme_file.write(dark_scheme)
        
        # home = str(Path.home())
        # with open (home+'/.kde4/share/apps/color-schemes/MaterialYouLight.colors', 'w', encoding='utf8') as light_scheme_file:
        #     light_scheme_file.write(light_scheme)
            
            
        # with open (home+'/.local/share/color-schemes/MaterialYouLight.colors', 'r', encoding='utf8') as light_scheme_file:
        #     print(light_scheme_file.read())
            
        #os.system('plasma-apply-colorscheme /home/luis/.local/share/color-schemes/MaterialYouDark.colors')
        subprocess.Popen("plasma-apply-colorscheme /home/luis/.local/share/color-schemes/MaterialYouDark.colors",
                                    shell=True, stdout=subprocess.PIPE,stderr=subprocess.DEVNULL).communicate()[0].decode('utf-8').strip()
        time.sleep(2)
        subprocess.Popen("plasma-apply-colorscheme /home/luis/.local/share/color-schemes/MaterialYouLight.colors",
                                    shell=True, stdout=subprocess.PIPE,stderr=subprocess.DEVNULL).communicate()[0].decode('utf-8').strip()
        #os.system('plasma-apply-colorscheme /home/luis/.local/share/color-schemes/MaterialYouLight.colors')