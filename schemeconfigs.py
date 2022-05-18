from color_utils import blendColors, hex2rgb
from utils import range_check, tup2str
class ThemeConfig:
    def __init__(self, colors, wallpaper_data, light_blend_multiplier=1, dark_blend_multiplier=1):
        colors_best = colors['bestColors']
        tones_primary = colors['primaryTones']
        tones_neutral = colors['neutralTones']
        
        lbm = range_check(light_blend_multiplier,0,4)
        dbm = range_check(dark_blend_multiplier,0,4)
            
        tone = 30
        pywal_colors_dark = ()
        pywal_colors_dark = (blendColors(
            tones_neutral['8'], colors['dark']['Primary'], .01),)
        for x in range(7):
            str_x = str(x)
            if str_x in colors_best.keys():
                pywal_colors_dark += (blendColors(
                    colors['dark']['OnSurface'], colors_best[str_x], .55),)
            else:
                pywal_colors_dark += (blendColors(
                    colors['dark']['OnSurface'], tones_primary[str(tone)], .58),)
                tone += 10

        tone = 30
        pywal_colors_light = ()
        pywal_colors_light = (blendColors(
            tones_neutral['98'], colors['light']['Primary'], .01),)
        for x in range(7):
            str_x = str(x)
            if str_x in colors_best.keys():
                pywal_colors_light += (blendColors(
                    colors['light']['OnSurface'], colors_best[str_x], .70),)
            else:
                pywal_colors_light += (blendColors(
                    colors['light']['OnSurface'], tones_primary[str(tone)], .8),)
                tone += 10

        # Base text states taken from Breeze Color Scheme
        base_text_states = {
            "Link": "#2980b9",
            "Visited": "#9b59b6",
            "Negative": "#da4453",
            "Neutral": "#f67400",
            "Positive": "#27ae60"
        }

        # Blend some extra colors by factor left(0.0) to right(1.0)
        self._extras = {
            "LightSurface1": blendColors(colors['light']['Background'], colors['light']['Primary'], .08*lbm),
            "DarkSurface1": blendColors(colors['dark']['Background'], colors['dark']['Primary'], .05*dbm),

            "LightSurface2": blendColors(colors['light']['Background'], colors['light']['Primary'], .11*lbm),
            "DarkSurface2": blendColors(colors['dark']['Background'], colors['dark']['Primary'], .08*dbm),

            "LightSurface3": blendColors(colors['light']['Background'], colors['light']['Primary'], .14*lbm),
            "DarkSurface3": blendColors(colors['dark']['Background'], colors['dark']['Primary'], .11*dbm),

            "LightSurface": blendColors(colors['light']['Surface'], colors['light']['Primary'], 0.05*lbm),
            "DarkSurface": blendColors(colors['dark']['Surface'], colors['dark']['Primary'], 0.02*dbm),

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

            "LightSelectionAlt": blendColors(colors['light']['Surface'], colors['light']['Secondary'], .02*lbm),
            "DarkSelectionAlt": blendColors(colors['dark']['Background'], colors['dark']['Secondary'], .3*dbm),

            "LightSelectionAltActive": blendColors(colors['light']['Background'], colors['light']['Secondary'], .5),
            "DarkSelectionAltActive": blendColors(colors['dark']['Background'], colors['dark']['Secondary'], .5),
        }
        extras = self._extras

        self._light_scheme = f"""[ColorEffects:Disabled]
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
BackgroundNormal={extras['LightSelectionAlt']}
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
BackgroundNormal={extras['LightSurface']}
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
BackgroundNormal={extras['LightSurface']}
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
BackgroundAlternate={extras['LightSurface']}
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

        self._dark_scheme = f"""[ColorEffects:Disabled]
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
BackgroundNormal={extras['DarkSurface']}
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
BackgroundNormal={extras['DarkSurface']}
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
BackgroundAlternate={extras['DarkSurface']}
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

        self._wal_light_scheme = {
            "wallpaper": wallpaper_data,
            "alpha": "100",

            "special": {
                "background": pywal_colors_light[0],
                "foreground": colors['light']['OnSurface'],
                "cursor": colors['light']['OnSurface'],
            },
            "colors": {
                "color0": pywal_colors_light[0],
                "color1": pywal_colors_light[1],
                "color2": pywal_colors_light[2],
                "color3": pywal_colors_light[3],
                "color4": pywal_colors_light[4],
                "color5": pywal_colors_light[5],
                "color6": pywal_colors_light[6],
                "color7": pywal_colors_light[7],
                "color8": colors['light']['Secondary'],
                "color9": pywal_colors_light[1],
                "color10": pywal_colors_light[2],
                "color11": pywal_colors_light[3],
                "color12": pywal_colors_light[4],
                "color13": pywal_colors_light[5],
                "color14": pywal_colors_light[6],
                "color15": pywal_colors_light[7]
            }
        }

        self._wal_dark_scheme = {
            "wallpaper": wallpaper_data,
            "alpha": "100",

            "special": {
                "background": pywal_colors_dark[0],
                "foreground": colors['dark']['OnSurface'],
                "cursor": colors['dark']['OnSurface'],
            },
            "colors": {
                "color0": pywal_colors_dark[0],
                "color1": pywal_colors_dark[1],
                "color2": pywal_colors_dark[2],
                "color3": pywal_colors_dark[3],
                "color4": pywal_colors_dark[4],
                "color5": pywal_colors_dark[5],
                "color6": pywal_colors_dark[6],
                "color7": pywal_colors_dark[7],
                "color8": colors['dark']['Secondary'],
                "color9": pywal_colors_dark[1],
                "color10": pywal_colors_dark[2],
                "color11": pywal_colors_dark[3],
                "color12": pywal_colors_dark[4],
                "color13": pywal_colors_dark[5],
                "color14": pywal_colors_dark[6],
                "color15": pywal_colors_dark[7]
            }
        }
        dark_active=colors['dark']['OnBackground']
        dark_inactive=extras['DarkSurface3']
        
        light_active=colors['light']['OnBackground']
        light_inactive=extras['LightSurface3']
    
        self._sierra_breeze_dark_colors = {
            "btn_close_active_color" : tup2str(hex2rgb(blendColors(dark_active, tones_primary['80'], .7))),
            "btn_minimize_active_color" : tup2str(hex2rgb(blendColors(dark_active, tones_primary['70'], .7))),
            "btn_maximize_active_color" : tup2str(hex2rgb(blendColors(dark_active, tones_primary['55'], .7))),
            "btn_keep_above_active_color" : tup2str(hex2rgb(blendColors(dark_active, "#118cff", .7))),
            "btn_keep_below_active_color" : tup2str(hex2rgb(blendColors(dark_active, "#5d00b9", .7))),
            "btn_on_all_desktops_active_color" : tup2str(hex2rgb(blendColors(dark_active, "#00b9b9", .7))),
            "btn_shade_active_color" : tup2str(hex2rgb(blendColors(dark_active, "#b900b6", .7))),
            "btn_inactive_color" : tup2str(hex2rgb(blendColors(dark_inactive, colors['dark']['Secondary'], .32)))
        }
        
        self._sierra_breeze_light_colors = {
            "btn_close_active_color" : tup2str(hex2rgb(blendColors(tones_primary['50'],light_active, .05*lbm))),
            "btn_minimize_active_color" : tup2str(hex2rgb(blendColors(tones_primary['60'],light_active, .05*lbm))),
            "btn_maximize_active_color" : tup2str(hex2rgb(blendColors(tones_primary['70'],light_active, .05*lbm))),
            "btn_keep_above_active_color" : tup2str(hex2rgb(blendColors("#118cff", light_active, .05*lbm))),
            "btn_keep_below_active_color" : tup2str(hex2rgb(blendColors("#5d00b9", light_active, .05*lbm))),
            "btn_on_all_desktops_active_color" : tup2str(hex2rgb(blendColors("#00b9b9", light_active, .05*lbm))),
            "btn_shade_active_color" : tup2str(hex2rgb(blendColors("#b900b6", light_active, .05*lbm))),
            "btn_inactive_color" : tup2str(hex2rgb(blendColors(light_inactive, colors['light']['Secondary'], .32)))
        }

    def get_extras(self):
        return self._extras
    
    def get_light_scheme(self):
        return(self._light_scheme)

    def get_dark_scheme(self):
        return(self._dark_scheme)

    def get_wal_light_scheme(self):
        return (self._wal_light_scheme)

    def get_wal_dark_scheme(self):
        return (self._wal_dark_scheme)
    
    def get_sierra_breeze_dark_colors(self):
        return (self._sierra_breeze_dark_colors)
    
    def get_sierra_breeze_light_colors(self):
        return (self._sierra_breeze_light_colors)
