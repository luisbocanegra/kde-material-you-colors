from color_utils import blendColors, hex2rgb, hex2alpha, scale_saturation, sort_colors_luminance, blend2contrast, lighteen_color
import utils


class ThemeConfig:
    def __init__(self, colors, wallpaper_data, light_blend_multiplier=1, dark_blend_multiplier=1, toolbar_opacity=100):
        if toolbar_opacity == None:
            toolbar_opacity = 100
        colors_best = colors['best']
        tones_primary = colors['palettes']['primary']
        tones_secondary = colors['palettes']['secondary']
        tones_neutral = colors['palettes']['neutral']
        tones_tertiary = colors['palettes']['tertiary']
        tones_error = colors['palettes']['error']
        colors_light = colors['schemes']['light']
        colors_dark = colors['schemes']['dark']

        lbm = utils.clip(light_blend_multiplier, 0, 4, 1.0)
        dbm = utils.clip(dark_blend_multiplier, 0, 4, 1.0)
        toolbar_opacity = utils.clip(toolbar_opacity, 0, 100, 100)

        # Base text states taken from Breeze Color Scheme
        base_text_states = {
            "Link": "#2980b9",
            "Visited": "#9b59b6",
            "Negative": "#da4453",
            "Neutral": "#f67400",
            "Positive": "#27ae60"
        }

        self._material_you_schemes = colors

        # Blend some extra colors by factor left(0.0) to right(1.0)
        self._extras = {
            "dark": {
                "surface": blendColors(tones_neutral[5], tones_primary[40], 0.08*dbm),
                "surface1": blendColors(colors_dark['background'], tones_primary[40], .05*dbm),
                "surface2": blendColors(colors_dark['background'], tones_primary[40], .08*dbm),
                "surface3": blendColors(colors_dark['background'], tones_primary[40], .11*dbm),

                "linkOnPrimary": blendColors(colors_dark['onPrimary'], base_text_states['Link'], .5),
                "linkVisitedOnPrimary": blendColors(colors_dark['onPrimary'], base_text_states['Visited'], .8),
                "negativeOnPrimary": blendColors(colors_dark['onPrimary'], base_text_states['Negative'], .8),
                "positiveOnPrimary": blendColors(colors_dark['onPrimary'], base_text_states['Positive'], .8),
                "neutralOnPrimary": blendColors(colors_dark['onPrimary'], base_text_states['Neutral'], .8),

                # view
                "linkOnSurface": blendColors(colors_dark['onSurface'], base_text_states['Link'], .8),
                "linkVisitedOnSurface": blendColors(colors_dark['onSurface'], base_text_states['Visited'], .8),
                "negativeOnSurface": blendColors(colors_dark['onSurface'], base_text_states['Negative'], .8),
                "positiveOnSurface": blendColors(colors_dark['onSurface'], base_text_states['Positive'], .8),
                "neutralOnSurface": blendColors(colors_dark['onSurface'], base_text_states['Neutral'], .8),

                "selectionAltActive": blendColors(colors_dark['background'], colors_dark['secondary'], .5),
            },
            "light": {
                "surface": blendColors(colors_light['background'], tones_primary[70], 0.13*lbm),
                "surface1": blendColors(colors_light['background'], tones_primary[70], .18*lbm),
                "surface2": blendColors(colors_light['background'], tones_primary[70], .23*lbm),
                "surface3": blendColors(colors_light['background'], tones_primary[70], .20*lbm),

                "linkOnPrimary": blendColors(colors_light['onPrimary'], base_text_states['Link'], .5),
                "linkVisitedOnPrimary": blendColors(colors_light['onPrimary'], base_text_states['Visited'], .8),
                "negativeOnPrimary": blendColors(colors_light['onPrimary'], base_text_states['Negative'], .8),
                "positiveOnPrimary": blendColors(colors_light['onPrimary'], base_text_states['Positive'], .8),
                "neutralOnPrimary": blendColors(colors_light['onPrimary'], base_text_states['Neutral'], .8),

                # view
                "linkOnSurface": blendColors(colors_light['onSurface'], base_text_states['Link'], .5),
                "linkVisitedOnSurface": blendColors(colors_light['onSurface'], base_text_states['Visited'], .8),
                "negativeOnSurface": blendColors(colors_light['onSurface'], base_text_states['Negative'], .8),
                "positiveOnSurface": blendColors(colors_light['onSurface'], base_text_states['Positive'], .8),
                "neutralOnSurface": blendColors(colors_light['onSurface'], base_text_states['Neutral'], .8),

                "selectionAltActive": blendColors(colors_light['background'], colors_light['secondary'], .5),
            },
        }
        self._extras['dark'].update(
            {
                "selectionAlt": blendColors(tones_secondary[30], self._extras['dark']['surface3'], .05*dbm),
                "selectionHover": blendColors(tones_secondary[50], self._extras['dark']['surface3'], .1*dbm),
            }
        )

        self._extras['light'].update(
            {
                "selectionAlt": blendColors(self._extras['light']['surface3'], tones_primary[30], .05*lbm),
                "selectionHover": blendColors(self._extras['light']['surface3'], tones_primary[50], .1*lbm),
            }
        )

        extras = self._extras

        best_colors_count = len(colors_best)
        best_colors_count = best_colors_count if best_colors_count > 7 else 8

        pywal_colors_dark = (extras['dark']['surface'],)
        pywal_colors_dark_intense = (blendColors(
            extras['dark']['surface'], colors_dark['secondary'], .8),)
        pywal_colors_dark_faint = (blendColors(
            extras['dark']['surface'], colors_dark['secondary'], .9),)
        tone = 50

        for x in range(7):
            str_x = str(x)
            if (len(pywal_colors_dark) <= 7):
                if str_x in colors_best.keys():
                    c = lighteen_color(
                        colors_best[str_x], .2, tones_neutral[99])
                    pywal_colors_dark += (blend2contrast(
                        c, pywal_colors_dark[0], tones_neutral[99], 4.5, .01, True),)
                else:
                    if (len(pywal_colors_dark) <= 7):
                        c = lighteen_color(
                            tones_primary[tone], .2, tones_neutral[99])
                        pywal_colors_dark += (blend2contrast(
                            c, pywal_colors_dark[0], tones_neutral[99], 4.5, .01, True),)
                    if (len(pywal_colors_dark) <= 7):
                        c = lighteen_color(
                            tones_tertiary[tone], .2, tones_neutral[99])
                        pywal_colors_dark += (blend2contrast(
                            c, pywal_colors_dark[0], tones_neutral[99], 4.5, .01, True),)
                    if tone < 91:
                        tone += 8
            else:
                break

        all = pywal_colors_dark
        pywal_colors_dark = (pywal_colors_dark[0],)
        sorted_colors = sort_colors_luminance(all)[-7:]
        for n in range(len(sorted_colors)):
            pywal_colors_dark += (sorted_colors[n],)
            pywal_colors_dark_intense += (blendColors(
                tones_neutral[1], sorted_colors[n], .96),)
            pywal_colors_dark_faint += (blendColors(
                tones_neutral[99], sorted_colors[n], .85),)

        tone = 50
        pywal_colors_light = (extras['light']['surface'],)
        pywal_colors_light_intense = (blendColors(
            tones_neutral[75], colors_light['secondary'], .8*lbm),)
        pywal_colors_light_faint = (blendColors(
            tones_neutral[50], colors_light['secondary'], .8*lbm),)

        for x in range(7):
            str_x = str(x)
            if (len(pywal_colors_light) <= 7):
                if str_x in colors_best.keys():
                    c = scale_saturation(colors_best[str_x], 1)
                    c = lighteen_color(c, .2, tones_neutral[99])
                    pywal_colors_light += (blend2contrast(
                        c, pywal_colors_light[0], tones_neutral[10], 4.5, .01, False),)
                else:
                    if (len(pywal_colors_light) <= 7):
                        c = scale_saturation(tones_primary[tone], 1)
                        pywal_colors_light += (blend2contrast(
                            c, pywal_colors_light[0], tones_neutral[10], 4.5, .01, False),)
                    if (len(pywal_colors_light) <= 7):
                        c = scale_saturation(tones_tertiary[tone], 1)
                        pywal_colors_light += (blend2contrast(
                            c, pywal_colors_light[0], tones_neutral[10], 4.5, .01, False),)
                    if tone < 91:
                        tone += 8
            else:
                break

        all = pywal_colors_light
        pywal_colors_light = (pywal_colors_light[0],)
        sorted_colors = sort_colors_luminance(all, True)[-7:]

        for n in range(len(sorted_colors)):
            pywal_colors_light += (blendColors(
                tones_neutral[38], sorted_colors[n], .8*lbm),)

            pywal_colors_light_intense += (blendColors(
                tones_neutral[33], sorted_colors[n], .8*lbm),)

            pywal_colors_light_faint += (blendColors(
                tones_neutral[23], sorted_colors[n], .8*lbm),)

        # print("CONTRAST CHECK DARK")
        # for color in pywal_colors_dark:
        #     c = contrast_ratio(color, pywal_colors_dark[0])
        #     print(f"{color} - {c}")
        # print("CONTRAST CHECK LIGHT")
        # for color in pywal_colors_light:
        #     c = contrast_ratio(pywal_colors_light[0],color)
        #     print(f"{color} - {c}")

        self._light_scheme = f"""[ColorEffects:Disabled]
Color={extras['light']['surface1']}
ColorAmount=0.55
ColorAmount=0
ColorEffect=0
ContrastAmount=0.65
ContrastEffect=1
IntensityAmount=0.1
IntensityEffect=2

[ColorEffects:Inactive]
ChangeSelectionColor=true
Color={colors_light['surfaceVariant']}
ColorAmount=0.025
ColorEffect=2
ContrastAmount=0.1
ContrastEffect=2
Enable=false
IntensityAmount=0
IntensityEffect=0

[Colors:Button]
BackgroundAlternate={colors_light['surfaceVariant']}
BackgroundNormal={extras['light']['selectionAlt']}
DecorationFocus={colors_light['primary']}
DecorationHover={colors_light['primary']}
ForegroundActive={colors_light['onSurface']}
ForegroundInactive={colors_light['outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={base_text_states['Negative']}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors_light['onSurface']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:Complementary]
BackgroundAlternate={extras['light']['surface']}
BackgroundNormal={extras['light']['surface3']}
DecorationFocus={colors_light['primary']}
DecorationHover={colors_light['primary']}
ForegroundActive={colors_light['inverseSurface']}
ForegroundInactive={colors_light['outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={colors_light['error']}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors_light['onSurfaceVariant']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:Header]
BackgroundAlternate={extras['light']['surface']}
BackgroundNormal={extras['light']['surface3']}
DecorationFocus={colors_light['primary']}
DecorationHover={colors_light['primary']}
ForegroundActive={colors_light['inverseSurface']}
ForegroundInactive={colors_light['outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={colors_light['error']}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors_light['onSurfaceVariant']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:Header][Inactive]
BackgroundAlternate={extras['light']['surface']}
BackgroundNormal={extras['light']['surface3']}
DecorationFocus={colors_light['primary']}
DecorationHover={colors_light['primary']}
ForegroundActive={colors_light['inverseSurface']}
ForegroundInactive={colors_light['outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={colors_light['error']}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors_light['onSurfaceVariant']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:Selection]
BackgroundAlternate={colors_light['primary']}
BackgroundNormal={colors_light['primary']}
DecorationFocus={colors_light['primary']}
DecorationHover={colors_light['primary']}
ForegroundActive={colors_light['onPrimary']}
ForegroundInactive={colors_light['onPrimary']}
ForegroundLink={extras['light']['linkOnPrimary']}
ForegroundNegative={extras['light']['negativeOnPrimary']}
ForegroundNeutral={extras['light']['neutralOnPrimary']}
ForegroundNormal={colors_light['onPrimary']}
ForegroundPositive={extras['light']['positiveOnPrimary']}
ForegroundVisited={extras['light']['linkVisitedOnPrimary']}

[Colors:Tooltip]
BackgroundAlternate={colors_light['surfaceVariant']}
BackgroundNormal={extras['light']['surface']}
DecorationFocus={colors_light['primary']}
DecorationHover={colors_light['primary']}
ForegroundActive={colors_light['onSurface']}
ForegroundInactive={colors_light['outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={colors_light['error']}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors_light['onSurface']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:View]
BackgroundAlternate={extras['light']['surface2']}
BackgroundNormal={extras['light']['surface']}
DecorationFocus={colors_light['primary']}
#-----------------------------------------------
DecorationHover={extras['light']['selectionHover']}
ForegroundActive={colors_light['inverseSurface']}
ForegroundInactive={colors_light['outline']}
ForegroundLink={extras['light']['linkOnSurface']}
ForegroundNegative={colors_light['error']}
ForegroundNeutral={extras['light']['neutralOnSurface']}
ForegroundNormal={colors_light['onSurfaceVariant']}
ForegroundPositive={extras['light']['positiveOnSurface']}
ForegroundVisited={extras['light']['linkVisitedOnSurface']}

[Colors:Window]
BackgroundAlternate={extras['light']['surface']}
BackgroundNormal={extras['light']['surface3']}
DecorationFocus={colors_light['primary']}
DecorationHover={colors_light['primary']}
ForegroundActive={colors_light['inverseSurface']}
ForegroundInactive={colors_light['outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={colors_light['error']}
ForegroundNeutral={base_text_states['Neutral']}
#--- Window titles, context icons
ForegroundNormal={colors_light['onSurfaceVariant']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[General]
ColorScheme=MaterialYouLight
Name=Material You Light
shadeSortColumn=true

[KDE]
contrast=4

[WM]
activeBackground={hex2alpha(extras['light']['surface3'],toolbar_opacity)}
activeBlend=227,229,231
activeForeground={colors_light['onSurface']}
inactiveBackground={hex2alpha(colors_light['secondaryContainer'],toolbar_opacity)}
inactiveBlend=239,240,241
inactiveForeground={colors_light['onSurfaceVariant']}
        """

        self._dark_scheme = f"""[ColorEffects:Disabled]
Color={extras['dark']['surface1']}
ColorAmount=0
ColorEffect=0
ContrastAmount=0.65
ContrastEffect=1
IntensityAmount=0.1
IntensityEffect=2

[ColorEffects:Inactive]
ChangeSelectionColor=true
Color=Color={colors_dark['surfaceVariant']}
ColorAmount=0.025
ColorEffect=2
ContrastAmount=0.1
ContrastEffect=2
Enable=false
IntensityAmount=0
IntensityEffect=0

[Colors:Button]
BackgroundAlternate={colors_dark['surfaceVariant']}
BackgroundNormal={extras['dark']['selectionAlt']}
DecorationFocus={colors_dark['primary']}
DecorationHover={colors_dark['primary']}
ForegroundActive={colors_dark['onSurface']}
ForegroundInactive={colors_dark['outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={tones_error[50]}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors_dark['onSurface']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:Complementary]
BackgroundAlternate={extras['dark']['surface']}
BackgroundNormal={extras['dark']['surface3']}
DecorationFocus={colors_dark['primary']}
DecorationHover={colors_dark['primary']}
ForegroundActive={colors_dark['inverseSurface']}
ForegroundInactive={colors_dark['outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={tones_error[50]}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors_dark['onSurfaceVariant']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:Header]
BackgroundAlternate={extras['dark']['surface']}
BackgroundNormal={extras['dark']['surface3']}
DecorationFocus={colors_dark['primary']}
DecorationHover={colors_dark['primary']}
ForegroundActive={colors_dark['inverseSurface']}
ForegroundInactive={colors_dark['outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={tones_error[50]}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors_dark['onSurfaceVariant']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:Header][Inactive]
BackgroundAlternate={extras['dark']['surface']}
BackgroundNormal={extras['dark']['surface3']}
DecorationFocus={colors_dark['primary']}
DecorationHover={colors_dark['primary']}
ForegroundActive={colors_dark['inverseSurface']}
ForegroundInactive={colors_dark['outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={tones_error[50]}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors_dark['onSurfaceVariant']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:Selection]
BackgroundAlternate={colors_dark['primary']}
BackgroundNormal={colors_dark['primary']}
DecorationFocus={colors_dark['primary']}
DecorationHover={colors_dark['primary']}
ForegroundActive={colors_dark['onPrimary']}
ForegroundInactive={colors_dark['onPrimary']}
ForegroundLink={extras['dark']['linkOnPrimary']}
ForegroundNegative={extras['dark']['negativeOnPrimary']}
ForegroundNeutral={extras['dark']['neutralOnPrimary']}
ForegroundNormal={colors_dark['onPrimary']}
ForegroundPositive={extras['dark']['positiveOnPrimary']}
ForegroundVisited={extras['dark']['linkVisitedOnPrimary']}



[Colors:Tooltip]
BackgroundAlternate={colors_dark['surfaceVariant']}
BackgroundNormal={extras['dark']['surface']}
DecorationFocus={colors_dark['primary']}
DecorationHover={colors_dark['primary']}
ForegroundActive={colors_dark['onSurface']}
ForegroundInactive={colors_dark['outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={tones_error[50]}
ForegroundNeutral={base_text_states['Neutral']}
ForegroundNormal={colors_dark['onSurface']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[Colors:View]
BackgroundAlternate={extras['dark']['surface2']}
BackgroundNormal={extras['dark']['surface']}
DecorationFocus={colors_dark['primary']}
#-----------------------------------------------
DecorationHover={colors_dark['inversePrimary']}
ForegroundActive={colors_dark['inverseSurface']}
ForegroundInactive={colors_dark['outline']}
ForegroundLink={extras['dark']['linkOnSurface']}
ForegroundNegative={extras['dark']['negativeOnSurface']}
ForegroundNeutral={extras['dark']['neutralOnSurface']}
ForegroundNormal={colors_dark['onSurfaceVariant']}
ForegroundPositive={extras['dark']['positiveOnSurface']}
ForegroundVisited={extras['dark']['linkVisitedOnSurface']}

[Colors:Window]
BackgroundAlternate={extras['dark']['surface']}
BackgroundNormal={extras['dark']['surface3']}
DecorationFocus={colors_dark['primary']}
DecorationHover={colors_dark['primary']}
ForegroundActive={colors_dark['inverseSurface']}
ForegroundInactive={colors_dark['outline']}
ForegroundLink={base_text_states['Link']}
ForegroundNegative={tones_error[50]}
ForegroundNeutral={base_text_states['Neutral']}
#--- Window titles, context icons
ForegroundNormal={colors_dark['onSurfaceVariant']}
ForegroundPositive={base_text_states['Positive']}
ForegroundVisited={base_text_states['Visited']}

[General]
ColorScheme=MaterialYouDark
Name=Material You dark
shadeSortColumn=true

[KDE]
contrast=4

[WM]
activeBackground={hex2alpha(extras['dark']['surface3'],toolbar_opacity)}
activeBlend=252,252,252
activeForeground={colors_dark['onSurface']}
inactiveBackground={hex2alpha(colors_dark['secondaryContainer'],toolbar_opacity)}
inactiveBlend=161,169,177
inactiveForeground={colors_dark['onSecondaryContainer']}
        """

        self._wal_light_scheme = {
            "wallpaper": wallpaper_data,
            "alpha": "100",

            "special": {
                "background": pywal_colors_light[0],
                "backgroundIntense": blendColors(
                    tones_neutral[8], colors_light['primary'], .0),
                "backgroundFaint": blendColors(
                    tones_neutral[8], colors_light['primary'], .35),
                "foreground": colors_light['onSurface'],
                "foregroundIntense": blendColors(
                    colors_light['onSurface'], colors_light['secondary'], .7),
                "foregroundFaint": blendColors(
                    colors_light['onSurface'], colors_light['secondary'], .35),

                "cursor": colors_dark['onSurface'],
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
                "color8": pywal_colors_light_intense[0],
                "color9": pywal_colors_light_intense[1],
                "color10": pywal_colors_light_intense[2],
                "color11": pywal_colors_light_intense[3],
                "color12": pywal_colors_light_intense[4],
                "color13": pywal_colors_light_intense[5],
                "color14": pywal_colors_light_intense[6],
                "color15": pywal_colors_light_intense[7],
                "color16": pywal_colors_light_faint[0],
                "color17": pywal_colors_light_faint[1],
                "color18": pywal_colors_light_faint[2],
                "color19": pywal_colors_light_faint[3],
                "color20": pywal_colors_light_faint[4],
                "color21": pywal_colors_light_faint[5],
                "color22": pywal_colors_light_faint[6],
                "color23": pywal_colors_light_faint[7]
            }
        }

        self._wal_dark_scheme = {
            "wallpaper": wallpaper_data,
            "alpha": "100",

            "special": {
                "background": pywal_colors_dark[0],
                "backgroundIntense": blendColors(
                    tones_neutral[8], colors_dark['primary'], .0),
                "backgroundFaint": blendColors(
                    tones_neutral[8], colors_dark['primary'], .35),
                "foreground": colors_dark['onSurface'],
                "foregroundIntense": blendColors(
                    colors_dark['onSurface'], colors_dark['secondary'], .7),
                "foregroundFaint": blendColors(
                    colors_dark['onSurface'], colors_dark['secondary'], .35),
                "cursor": colors_dark['onSurface'],
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
                "color8": pywal_colors_dark_intense[0],
                "color9": pywal_colors_dark_intense[1],
                "color10": pywal_colors_dark_intense[2],
                "color11": pywal_colors_dark_intense[3],
                "color12": pywal_colors_dark_intense[4],
                "color13": pywal_colors_dark_intense[5],
                "color14": pywal_colors_dark_intense[6],
                "color15": pywal_colors_dark_intense[7],
                "color16": pywal_colors_dark_faint[0],
                "color17": pywal_colors_dark_faint[1],
                "color18": pywal_colors_dark_faint[2],
                "color19": pywal_colors_dark_faint[3],
                "color20": pywal_colors_dark_faint[4],
                "color21": pywal_colors_dark_faint[5],
                "color22": pywal_colors_dark_faint[6],
                "color23": pywal_colors_dark_faint[7]
            }
        }
        dark_active = colors_dark['onBackground']
        dark_inactive = extras['dark']['surface3']

        light_active = colors_light['onBackground']
        light_inactive = extras['light']['surface3']

        self._sierra_breeze_dark_colors = {
            "btn_close_active_color": utils.tup2str(hex2rgb(blendColors(dark_active, tones_primary[80], .7))),
            "btn_minimize_active_color": utils.tup2str(hex2rgb(blendColors(dark_active, tones_primary[70], .7))),
            "btn_maximize_active_color": utils.tup2str(hex2rgb(blendColors(dark_active, tones_primary[70], .7))),
            "btn_keep_above_active_color": utils.tup2str(hex2rgb(blendColors(dark_active, "#118cff", .7))),
            "btn_keep_below_active_color": utils.tup2str(hex2rgb(blendColors(dark_active, "#5d00b9", .7))),
            "btn_on_all_desktops_active_color": utils.tup2str(hex2rgb(blendColors(dark_active, "#00b9b9", .7))),
            "btn_shade_active_color": utils.tup2str(hex2rgb(blendColors(dark_active, "#b900b6", .7))),
            "btn_inactive_color": utils.tup2str(hex2rgb(blendColors(dark_inactive, colors_dark['secondary'], .32)))
        }

        self._sierra_breeze_light_colors = {
            "btn_close_active_color": utils.tup2str(hex2rgb(blendColors(tones_primary[50], light_active, .05*lbm))),
            "btn_minimize_active_color": utils.tup2str(hex2rgb(blendColors(tones_primary[60], light_active, .05*lbm))),
            "btn_maximize_active_color": utils.tup2str(hex2rgb(blendColors(tones_primary[70], light_active, .05*lbm))),
            "btn_keep_above_active_color": utils.tup2str(hex2rgb(blendColors("#118cff", light_active, .05*lbm))),
            "btn_keep_below_active_color": utils.tup2str(hex2rgb(blendColors("#5d00b9", light_active, .05*lbm))),
            "btn_on_all_desktops_active_color": utils.tup2str(hex2rgb(blendColors("#00b9b9", light_active, .05*lbm))),
            "btn_shade_active_color": utils.tup2str(hex2rgb(blendColors("#b900b6", light_active, .05*lbm))),
            "btn_inactive_color": utils.tup2str(hex2rgb(blendColors(light_inactive, colors_light['secondary'], .32)))
        }

    def get_material_schemes(self):
        return self._material_you_schemes

    def get_extras(self):
        return self._extras

    def get_light_scheme(self):
        return (self._light_scheme)

    def get_dark_scheme(self):
        return (self._dark_scheme)

    def get_wal_light_scheme(self):
        return (self._wal_light_scheme)

    def get_wal_dark_scheme(self):
        return (self._wal_dark_scheme)

    def get_sierra_breeze_dark_colors(self):
        return (self._sierra_breeze_dark_colors)

    def get_sierra_breeze_light_colors(self):
        return (self._sierra_breeze_light_colors)
