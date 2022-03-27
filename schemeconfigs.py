class ThemeConfig:
    def __init__(self, colors, extras, base_text_states):
        
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
Color={colors['light']['SurfaceVariant']}
ColorAmount=1
ColorEffect=0
ContrastAmount=1
ContrastEffect=0
Enable=false
IntensityAmount=10
IntensityEffect=10

[Colors:Button]
BackgroundAlternate={colors['light']['SurfaceVariant']}
BackgroundNormal={colors['light']['Surface']}
DecorationFocus={colors['light']['Primary']}
DecorationHover={colors['light']['Primary']}
ForegroundActive={colors['light']['OnSurface']}
ForegroundInactive={colors['light']['Outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={colors['light']['Error']}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors['light']['OnSurface']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:Header]
BackgroundNormal={extras['LightSurface3']}

[Colors:Selection]
BackgroundAlternate={colors['light']['Primary']}
BackgroundNormal={colors['light']['Primary']}
DecorationFocus={colors['light']['Primary']}
DecorationHover={colors['light']['Primary']}
ForegroundActive={colors['light']['OnPrimary']}
ForegroundInactive={colors['light']['OnPrimary']}
ForegroundLink={extras['LinkOnPrimaryLight']}
ForegroundNegative={extras['NegativeOnPrimaryLight']}
ForegroundNeutral={extras['NeutralOnPrimaryLight']}
ForegroundNormal={colors['light']['OnPrimary']}
ForegroundPositive={extras['PositiveOnPrimaryLight']}
ForegroundVisited={extras['LinkVisitedOnPrimaryLight']}

[Colors:Tooltip]
BackgroundAlternate={colors['light']['SurfaceVariant']}
BackgroundNormal={colors['light']['Surface']}
DecorationFocus={colors['light']['Primary']}
DecorationHover={colors['light']['Primary']}
ForegroundActive={colors['light']['OnSurface']}
ForegroundInactive={colors['light']['Outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={colors['light']['Error']}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors['light']['OnSurface']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:View]
BackgroundAlternate={extras['LightSurface2']}
BackgroundNormal={colors['light']['Surface']}
DecorationFocus={colors['light']['Primary']}
#-----------------------------------------------
DecorationHover={colors['light']['Primary']}
ForegroundActive={colors['light']['InverseSurface']}
ForegroundInactive={colors['light']['Outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={colors['light']['Error']}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors['light']['OnSurfaceVariant']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:Window]
BackgroundAlternate={colors['light']['Surface']}
BackgroundNormal={extras['LightSurface3']}
DecorationFocus={colors['light']['Primary']}
DecorationHover={colors['light']['Primary']}
ForegroundActive={colors['light']['InverseSurface']}
ForegroundInactive={colors['light']['Outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={colors['light']['Error']}
ForegroundNeutral={base_text_states['Neutral']}
#--- Window titles, context icons
ForegroundNormal={colors['light']['OnSurfaceVariant']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Negative']}

[General]
ColorScheme=MaterialYouLight
Name=Material You Light
shadeSortColumn=false

[KDE]
contrast=4

[WM]
activeBackground={extras['LightSurface3']}
activeBlend=#ff0000
activeForeground={colors['light']['OnSurface']}
inactiveBackground={colors['light']['SecondaryContainer']}
inactiveBlend=#ff0000
inactiveForeground={colors['light']['OnSurfaceVariant']}
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
Color=Color={colors['dark']['SurfaceVariant']}
ColorAmount=-0.9
ColorEffect=0
ContrastAmount=0.1
ContrastEffect=0
Enable=true
IntensityAmount=0
IntensityEffect=0

[Colors:Button]
BackgroundAlternate={colors['dark']['SurfaceVariant']}
BackgroundNormal={extras['DarkSelectionAlt']}
DecorationFocus={colors['dark']['Primary']}
DecorationHover={colors['dark']['Primary']}
ForegroundActive={colors['dark']['OnSurface']}
ForegroundInactive={colors['dark']['Outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={colors['dark']['Error']}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors['dark']['OnSurface']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:Header]
BackgroundNormal={extras['DarkSurface3']}

[Colors:Selection]
BackgroundAlternate={colors['dark']['Primary']}
BackgroundNormal={colors['dark']['Primary']}
DecorationFocus={colors['dark']['Primary']}
DecorationHover={colors['dark']['Primary']}
ForegroundActive={colors['dark']['OnPrimary']}
ForegroundInactive={colors['dark']['OnPrimary']}
ForegroundLink={extras['LinkOnPrimaryDark']}
ForegroundNegative={extras['NegativeOnPrimaryDark']}
ForegroundNeutral={extras['NeutralOnPrimaryDark']}
ForegroundNormal={colors['dark']['OnPrimary']}
ForegroundPositive={extras['PositiveOnPrimaryDark']}
ForegroundVisited={extras['LinkVisitedOnPrimaryDark']}



[Colors:Tooltip]
BackgroundAlternate={colors['dark']['SurfaceVariant']}
BackgroundNormal={colors['dark']['Surface']}
DecorationFocus={colors['dark']['Primary']}
DecorationHover={colors['dark']['Primary']}
ForegroundActive={colors['dark']['OnSurface']}
ForegroundInactive={colors['dark']['Outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={colors['dark']['Error']}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors['dark']['OnSurface']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:View]
BackgroundAlternate={extras['DarkSurface2']}
BackgroundNormal={colors['dark']['Surface']}
DecorationFocus={colors['dark']['Primary']}
#-----------------------------------------------
DecorationHover={colors['dark']['Primary']}
ForegroundActive={colors['dark']['InverseSurface']}
ForegroundInactive={colors['dark']['Outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={colors['dark']['Error']}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors['dark']['OnSurfaceVariant']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:Window]
BackgroundAlternate={colors['dark']['Surface']}
BackgroundNormal={extras['DarkSurface3']}
DecorationFocus={colors['dark']['Primary']}
DecorationHover={colors['dark']['Primary']}
ForegroundActive={colors['dark']['InverseSurface']}
ForegroundInactive={colors['dark']['Outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={colors['dark']['Error']}
ForegroundNeutral={base_text_states['Neutral']}
#--- Window titles, context icons
ForegroundNormal={colors['dark']['OnSurfaceVariant']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Negative']}

[General]
ColorScheme=MaterialYouDark
Name=Material You dark
shadeSortColumn=true

[KDE]
contrast=4

[WM]
activeBackground={extras['DarkSurface3']}
activeBlend=#ff0000
activeForeground={colors['dark']['OnSurface']}
inactiveBackground={colors['dark']['SecondaryContainer']}
inactiveBlend=#ff0000
inactiveForeground={colors['dark']['OnSecondaryContainer']}
        """
        
    def get_light_scheme(self):
        return(self._light_scheme)
    def get_dark_scheme(self):
        return(self._dark_scheme)