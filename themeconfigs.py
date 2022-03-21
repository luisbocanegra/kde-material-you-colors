class ThemeConfig:
    def __init__(self, colors, extras):
        
        self._light_scheme=f"""[ColorEffects:Disabled]
Color={extras['LightSurface1']}
ColorAmount=0.55
ColorEffect=3
ContrastAmount=0.65
ContrastEffect=0
IntensityAmount=0.1
IntensityEffect=0

[ColorEffects:Inactive]
ChangeSelectionColor=false
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
BackgroundNormal={extras['LightSurface1']}
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
        self._dark_scheme=f"""[ColorEffects:Disabled]
Color={extras['DarkSurface1']}
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
BackgroundNormal={extras['DarkSurface1']}
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
        
    def get_light_scheme(self):
        return(self._light_scheme)
    def get_dark_scheme(self):
        return(self._dark_scheme)