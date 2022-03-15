import os
from pathlib import Path
class ColorScheme:
    def __init__(self, colors):
        self.colors = colors
        
        
    def make_light_scheme(self):
        colors = self.colors
        #print(f'Colors light:\n{self.colors}')
        
        light_scheme = f"""[ColorEffects:Disabled]
Color=56,56,56
ColorAmount=0
ColorEffect=0
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
BackgroundNormal={colors['light']['primary']}
DecorationFocus={colors['light']['primary']}
DecorationHover=255,89,125
ForegroundActive=#ffff00
ForegroundInactive=75,79,85
ForegroundLink=41,128,185
ForegroundNegative=39,120,110
ForegroundNeutral=95,125,205
ForegroundNormal={colors['light']['onPrimary']}
ForegroundPositive=156,83,198
ForegroundVisited=127,140,141

[Colors:Selection]
BackgroundAlternate=255,89,125
BackgroundNormal={colors['light']['primary']}
DecorationFocus={colors['light']['primary']}
DecorationHover=255,89,125
ForegroundActive=252,252,252
ForegroundInactive=132,134,140
ForegroundLink=253,188,75
ForegroundNegative=67,205,189
ForegroundNeutral=95,125,205
ForegroundNormal=253,230,235
ForegroundPositive=156,83,198
ForegroundVisited=189,195,199

[Colors:Tooltip]
BackgroundAlternate=255,89,125
BackgroundNormal=241,104,111
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
BackgroundNormal={colors['light']['surface']}
DecorationFocus=255,99,118
DecorationHover=255,89,125
ForegroundActive=61,174,233
ForegroundInactive=75,79,85
ForegroundLink=31,140,236
ForegroundNegative=67,205,189
ForegroundNeutral=95,125,205
ForegroundNormal=60,66,70
ForegroundPositive=156,83,198
ForegroundVisited=127,140,141

[Colors:Window]
BackgroundAlternate=#ff0000
BackgroundNormal={colors['light']['primaryContainer']}
DecorationFocus=#ff0000
DecorationHover=#00ff00
ForegroundActive=61,174,233
ForegroundInactive=75,79,85
ForegroundLink=41,128,185
ForegroundNegative=67,205,189
ForegroundNeutral=95,125,205
ForegroundNormal=92,93,97
ForegroundPositive=156,83,198
ForegroundVisited=127,140,141

[General]
ColorScheme=MaterialYouLight
Name=Material You Light
shadeSortColumn=true

[KDE]
contrast=7

[WM]
activeBackground=247,249,249
activeBlend=183,186,195
activeForeground=65,66,67
inactiveBackground=247,249,249
inactiveBlend=247,249,249
inactiveForeground=113,115,120
"""
        print(colors['light']['primary'])
        
        home = str(Path.home())
        with open (home+'/.local/share/color-schemes/MaterialYouLight.colors', 'w', encoding='utf8') as light_scheme_file:
            light_scheme_file.write(light_scheme)
            
            
        with open (home+'/.local/share/color-schemes/MaterialYouLight.colors', 'r', encoding='utf8') as light_scheme_file:
            print(light_scheme_file.read())
            
        os.system('./plasma-theme  -c /home/luis/.local/share/color-schemes/Moe.colors')
        os.system('./plasma-theme  -c /home/luis/.local/share/color-schemes/MaterialYouLight.colors')