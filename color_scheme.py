import os
from pathlib import Path
import time
import numpy
from colorutils import Color

class RGB(numpy.ndarray): # taken from https://programming-idioms.org/idiom/154/halfway-between-two-hex-color-codes/2155/python
        @classmethod
        def from_str(cls, rgbstr):
            return numpy.array([
            int(rgbstr[i:i+2], 16)
            for i in range(1, len(rgbstr), 2)
            ]).view(cls)

        def __str__(self):
            self = self.astype(numpy.uint8)
            return '#' + ''.join(format(n, 'x') for n in self)

class ColorScheme:
    
    def __init__(self, colors):
        self.colors = colors
        
        
    def make_light_scheme(self):
        colors = self.colors
        #print(f'Colors light:\n{self.colors}')
        c1 = RGB.from_str(colors['light']['Surface'])
        c2 = RGB.from_str(colors['light']['SecondaryContainer'])
        c3 = ((((c1 + c2 ) /2) + c1)  / 2)
        
        c1 = RGB.from_str(colors['dark']['Surface'])
        c2 = RGB.from_str(colors['dark']['SecondaryContainer'])
        c3_dark = ((((c1 + c2 ) /2)))
        #blend1 = Color(c1.rgb + c2.rgb)
        print(f'{c1} + {c2} = {c3}')
        light_scheme = f"""[ColorEffects:Disabled]
Color={c3}
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
BackgroundAlternate=255,89,125
BackgroundNormal={colors['light']['Primary']}
DecorationFocus={colors['light']['Primary']}
DecorationHover=255,89,125
ForegroundActive=252,252,252
ForegroundInactive=132,134,140
ForegroundLink=253,188,75
ForegroundNegative=67,205,189
ForegroundNeutral=95,125,205
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
BackgroundNormal={c3}
DecorationFocus={colors['light']['Primary']}
#-----------------------------------------------
DecorationHover={colors['light']['Primary']}
ForegroundActive={colors['light']['OnSurface']}
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
ForegroundNeutral={colors['light']['InversePrimary']}
#---------------------------------------------------- Window header text all
ForegroundNormal={colors['light']['OnSurfaceVariant']}
ForegroundPositive=156,83,198
ForegroundVisited=127,140,141

[General]
ColorScheme=MaterialYouLight
Name=Material You Light
shadeSortColumn=true

[KDE]
contrast=5

[WM]
activeBackground={colors['light']['SecondaryContainer']}
activeBlend=183,186,195
activeForeground={colors['light']['OnSecondaryContainer']}
inactiveBackground={colors['light']['SecondaryContainer']}
inactiveBlend=247,249,249
inactiveForeground={colors['light']['OnSecondaryContainer']}
"""
        dark_scheme = f"""[ColorEffects:Disabled]
Color={c3_dark}
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
BackgroundNormal={c3_dark}
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
            
        os.system('./plasma-theme  -c /home/luis/.local/share/color-schemes/MaterialYouDark.colors')
        time.sleep(1)
        os.system('./plasma-theme  -c /home/luis/.local/share/color-schemes/MaterialYouLight.colors')