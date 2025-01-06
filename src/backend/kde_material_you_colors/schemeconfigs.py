import logging
from kde_material_you_colors.utils.color_utils import (
    blendColors,
    lighteen_color,
    scale_saturation,
    blend2contrast,
    sort_colors_luminance,
    hex2alpha,
    hex2rgb,
)
from kde_material_you_colors.utils import string_utils


class ThemeConfig:
    def __init__(
        self,
        colors,
        wallpaper_data,
        light_blend_multiplier=None,
        dark_blend_multiplier=None,
        toolbar_opacity=None,
        toolbar_opacity_dark=None,
        custom_colors_list=None,
    ):
        if custom_colors_list is not None:
            colors_best = custom_colors_list
            colors_str = ""
            for color in custom_colors_list:
                rgb = hex2rgb(color)
                colors_str += f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]};1m{color} \033[0m"
            logging.info(f"Using custom colors: {colors_str[:-5]}")
        else:
            colors_best = colors["best"]
        tones_primary = colors["palettes"]["primary"]
        tones_secondary = colors["palettes"]["secondary"]
        tones_neutral = colors["palettes"]["neutral"]
        tones_neutral_variant = colors["palettes"]["neutralVariant"]
        tones_tertiary = colors["palettes"]["tertiary"]
        tones_error = colors["palettes"]["error"]

        colors_light = colors["schemes"]["light"]
        colors_dark = colors["schemes"]["dark"]

        self._material_you_schemes = colors

        self._extras = colors["custom"]

        extras = self._extras

        best_colors_count = len(colors_best)
        # bg , ansi 30
        pywal_colors_dark = (colors_dark["surface"],)
        # gray? bold, ansi 30
        pywal_colors_dark_intense = (
            blendColors(pywal_colors_dark[0], tones_secondary[90], 0.8),
        )
        # dark gray? faint ansi 30
        pywal_colors_dark_faint = (
            blendColors(pywal_colors_dark[0], tones_secondary[90], 0.7),
        )
        tone = 50

        for x in range(7):
            if len(pywal_colors_dark) <= 7:
                if x < best_colors_count:
                    c = lighteen_color(colors_best[x], 0.2, tones_neutral[99])
                    pywal_colors_dark += (
                        blend2contrast(
                            c, pywal_colors_dark[0], tones_neutral[99], 2.5, 0.01, True
                        ),
                    )
                else:
                    if len(pywal_colors_dark) <= 7:
                        c = lighteen_color(tones_primary[tone], 0.2, tones_neutral[99])
                        pywal_colors_dark += (
                            blend2contrast(
                                c,
                                pywal_colors_dark[0],
                                tones_neutral[99],
                                2.5,
                                0.01,
                                True,
                            ),
                        )
                    if len(pywal_colors_dark) <= 7:
                        c = lighteen_color(tones_tertiary[tone], 0.2, tones_neutral[99])
                        pywal_colors_dark += (
                            blend2contrast(
                                c,
                                pywal_colors_dark[0],
                                tones_neutral[99],
                                2.5,
                                0.01,
                                True,
                            ),
                        )
                    if tone < 91:
                        tone += 8
            else:
                break

        all_colors = pywal_colors_dark
        pywal_colors_dark = (pywal_colors_dark[0],)
        # sort colors if they don't come from custom colors
        if custom_colors_list is None:
            all_colors = sort_colors_luminance(all_colors[-7:])
        else:
            all_colors = all_colors[-7:]

        for n in range(7):
            pywal_colors_dark += (blendColors(tones_neutral[99], all_colors[n], 0.95),)

            pywal_colors_dark_intense += (
                blendColors(tones_neutral[99], all_colors[n], 0.82),
            )

            pywal_colors_dark_faint += (
                blendColors(pywal_colors_dark[0], all_colors[n], 0.7),
            )

        tone = 50
        # ansi 30
        pywal_colors_light = (colors_light["surface"],)
        pywal_colors_light_intense = (
            blendColors(pywal_colors_light[0], tones_secondary[25], 0.8),
        )
        pywal_colors_light_faint = (
            blendColors(pywal_colors_light[0], tones_secondary[25], 0.7),
        )

        for x in range(7):
            if len(pywal_colors_light) <= 7:
                if x < best_colors_count:
                    c = scale_saturation(colors_best[x], 1)
                    c = lighteen_color(c, 0.2, tones_neutral[99])
                    pywal_colors_light += (
                        blend2contrast(
                            c,
                            pywal_colors_light[0],
                            tones_neutral[10],
                            2,
                            0.01,
                            False,
                        ),
                    )
                else:
                    if len(pywal_colors_light) <= 7:
                        c = scale_saturation(tones_primary[tone], 1)
                        pywal_colors_light += (
                            blend2contrast(
                                c,
                                pywal_colors_light[0],
                                tones_neutral[10],
                                2,
                                0.01,
                                False,
                            ),
                        )
                    if len(pywal_colors_light) <= 7:
                        c = scale_saturation(tones_tertiary[tone], 1)
                        pywal_colors_light += (
                            blend2contrast(
                                c,
                                pywal_colors_light[0],
                                tones_neutral[10],
                                2,
                                0.01,
                                False,
                            ),
                        )
                    if tone < 91:
                        tone += 8
            else:
                break

        all_colors = pywal_colors_light
        pywal_colors_light = (pywal_colors_light[0],)
        # sort colors if they don't come from custom colors
        if custom_colors_list is None:
            all_colors = sort_colors_luminance(all_colors[-7:])
        else:
            all_colors = all_colors[-7:]
        for n in range(7):
            pywal_colors_light += (blendColors(tones_neutral[1], all_colors[n], 0.95),)

            pywal_colors_light_intense += (
                blendColors(tones_neutral[1], all_colors[n], 0.82),
            )

            pywal_colors_light_faint += (
                blendColors(pywal_colors_light[0], all_colors[n], 0.7),
            )

        # print("CONTRAST CHECK DARK - NORMAL")
        # for color in pywal_colors_dark:
        #     c = contrast_ratio(color, pywal_colors_dark[0])
        #     print(f"{color}  {'{0:.2g}'.format(c)} |", end=" ")
        # print()

        # print("CONTRAST CHECK DARK - INTENSE")
        # for color in pywal_colors_dark_intense:
        #     c = contrast_ratio(color, pywal_colors_dark[0])
        #     print(f"{color}  {'{0:.2g}'.format(c)} |", end=" ")
        # print()

        # print("CONTRAST CHECK DARK - FAINT")
        # for color in pywal_colors_dark_faint:
        #     c = contrast_ratio(color, pywal_colors_dark[0])
        #     print(f"{color}  {'{0:.2g}'.format(c)} |", end=" ")
        # print("\n")

        # print("CONTRAST CHECK LIGHT - NORMAL")
        # for color in pywal_colors_light:
        #     c = contrast_ratio(pywal_colors_light[0], color)
        #     print(f"{color}   {'{0:.2g}'.format(c)} |", end=" ")
        # print()

        # print("CONTRAST CHECK LIGHT - INTENSE")
        # for color in pywal_colors_light_intense:
        #     c = contrast_ratio(pywal_colors_light[0], color)
        #     print(f"{color}  {'{0:.2g}'.format(c)} |", end=" ")
        # print()

        # print("CONTRAST CHECK LIGHT - FAINT")
        # for color in pywal_colors_light_faint:
        #     c = contrast_ratio(pywal_colors_light[0], color)
        #     print(f"{color}  {'{0:.2g}'.format(c)} |", end=" ")
        # print()

        self._light_scheme = f"""[ColorEffects:Disabled]
Color={colors_light["surfaceContainer"]}
ColorAmount=0.5
ColorEffect=3
ContrastAmount=0
ContrastEffect=0
IntensityAmount=0
IntensityEffect=0

[ColorEffects:Inactive]
ChangeSelectionColor=true
Color={colors_light['surfaceContainerLowest']}
ColorAmount=0.025
ColorEffect=0
ContrastAmount=0.1
ContrastEffect=0
Enable=false
IntensityAmount=0
IntensityEffect=0

[Colors:Button]
BackgroundAlternate={colors_light['surfaceVariant']}
BackgroundNormal={colors_light['surfaceContainerHigh']}
DecorationFocus={colors_light['primary']}
DecorationHover={colors_light['primary']}
ForegroundActive={colors_light['onSurface']}
ForegroundInactive={colors_light['outline']}
ForegroundLink={extras['link']['light']['primary']}
ForegroundNegative={extras['negative']['light']['primary']}
ForegroundNeutral={extras['neutral']['light']['primary']}
ForegroundNormal={colors_light['onSurface']}
ForegroundPositive={extras['positive']['light']['primary']}
ForegroundVisited={extras['visited']['light']['primary']}

[Colors:Complementary]
BackgroundAlternate={colors_light['surface']}
BackgroundNormal={colors_light['surfaceContainer']}
DecorationFocus={colors_light['primary']}
DecorationHover={colors_light['primary']}
ForegroundActive={colors_light['inverseSurface']}
ForegroundInactive={colors_light['outline']}
ForegroundLink={extras['link']['light']['primary']}
ForegroundNegative={extras['negative']['light']['primary']}
ForegroundNeutral={extras['neutral']['light']['primary']}
ForegroundNormal={colors_light['onSurfaceVariant']}
ForegroundPositive={extras['positive']['light']['primary']}
ForegroundVisited={extras['visited']['light']['primary']}

[Colors:Header]
BackgroundAlternate={colors_light['surfaceContainer']}
BackgroundNormal={colors_light['surfaceContainer']}
DecorationFocus={colors_light['primary']}
DecorationHover={colors_light['primary']}
ForegroundActive={colors_light['inverseSurface']}
ForegroundInactive={colors_light['outline']}
ForegroundLink={extras['link']['light']['primary']}
ForegroundNegative={extras['negative']['light']['primary']}
ForegroundNeutral={extras['neutral']['light']['primary']}
ForegroundNormal={colors_light['onSurfaceVariant']}
ForegroundPositive={extras['positive']['light']['primary']}
ForegroundVisited={extras['visited']['light']['primary']}

[Colors:Header][Inactive]
BackgroundAlternate={colors_light['surfaceContainer']}
BackgroundNormal={colors_light['surfaceContainer']}
DecorationFocus={colors_light['primary']}
DecorationHover={colors_light['primary']}
ForegroundActive={colors_light['inverseSurface']}
ForegroundInactive={colors_light['outline']}
ForegroundLink={extras['link']['light']['primary']}
ForegroundNegative={extras['negative']['light']['primary']}
ForegroundNeutral={extras['neutral']['light']['primary']}
ForegroundNormal={colors_light['onSurfaceVariant']}
ForegroundPositive={extras['positive']['light']['primary']}
ForegroundVisited={extras['visited']['light']['primary']}

[Colors:Selection]
BackgroundAlternate={colors_light['primary']}
BackgroundNormal={colors_light['primary']}
DecorationFocus={colors_light['primary']}
DecorationHover={colors_light['secondary']}
ForegroundActive={colors_light['onPrimary']}
ForegroundInactive={colors_light['onPrimary']}
ForegroundLink={extras['link']['light']['onPrimaryFixedVariant']}
ForegroundNegative={extras['negative']['light']['onPrimaryFixedVariant']}
ForegroundNeutral={extras['neutral']['light']['onPrimaryFixedVariant']}
ForegroundNormal={colors_light['onPrimary']}
ForegroundPositive={extras['positive']['light']['onPrimaryFixedVariant']}
ForegroundVisited={extras['visited']['light']['onPrimaryFixedVariant']}

[Colors:Tooltip]
BackgroundAlternate={colors_light['surfaceVariant']}
BackgroundNormal={colors_light['surfaceContainer']}
DecorationFocus={colors_light['primary']}
DecorationHover={colors_light['primary']}
ForegroundActive={colors_light['onSurface']}
ForegroundInactive={colors_light['outline']}
ForegroundLink={extras['link']['light']['primary']}
ForegroundNegative={extras['negative']['light']['primary']}
ForegroundNeutral={extras['neutral']['light']['primary']}
ForegroundNormal={colors_light['onSurface']}
ForegroundPositive={extras['positive']['light']['primary']}
ForegroundVisited={extras['visited']['light']['primary']}

[Colors:View]
BackgroundAlternate={colors_light['surfaceContainer']}
BackgroundNormal={colors_light['surfaceBright']}
DecorationFocus={colors_light['primary']}
#-----------------------------------------------
DecorationHover={colors_light['secondaryFixed']}
ForegroundActive={colors_light['inverseSurface']}
ForegroundInactive={colors_light['outline']}
ForegroundLink={extras['link']['light']['primary']}
ForegroundNegative={extras['negative']['light']['primary']}
ForegroundNeutral={extras['neutral']['light']['primary']}
ForegroundNormal={colors_light['onSurface']}
ForegroundPositive={extras['positive']['light']['primary']}
ForegroundVisited={extras['visited']['light']['primary']}

[Colors:Window]
BackgroundAlternate={colors_light['surfaceVariant']}
BackgroundNormal={colors_light['surfaceContainer']}
DecorationFocus={colors_light['primary']}
DecorationHover={colors_light['primary']}
ForegroundActive={extras['link']['light']['primary']}
ForegroundInactive={colors_light['outline']}
ForegroundLink={extras['link']['light']['primary']}
ForegroundNegative={extras['negative']['light']['primary']}
ForegroundNeutral={extras['neutral']['light']['primary']}
#--- Window titles, context icons
ForegroundNormal={colors_light['onSurfaceVariant']}
ForegroundPositive={extras['positive']['light']['primary']}
ForegroundVisited={extras['visited']['light']['primary']}

[General]
ColorScheme=MaterialYouLight
Name=Material You Light
shadeSortColumn=true

[KDE]
contrast=4

[WM]
activeBackground={hex2alpha(colors_light["surfaceContainerHighest"],toolbar_opacity)}
activeBlend=227,229,231
activeForeground={colors_light['onSurface']}
inactiveBackground={hex2alpha(colors_light['secondaryContainer'],toolbar_opacity)}
inactiveBlend=239,240,241
inactiveForeground={colors_light['onSurfaceVariant']}
        """

        self._dark_scheme = f"""[ColorEffects:Disabled]
Color={colors_dark["surfaceContainer"]}
ColorAmount=0.5
ColorEffect=3
ContrastAmount=0
ContrastEffect=0
IntensityAmount=0
IntensityEffect=0

[ColorEffects:Inactive]
ChangeSelectionColor=true
Color={colors_dark['surfaceContainerLowest']}
ColorAmount=0.025
ColorEffect=0
ContrastAmount=0.1
ContrastEffect=0
Enable=true
IntensityAmount=0
IntensityEffect=0

[Colors:Button]
BackgroundAlternate={colors_dark['surfaceVariant']}
BackgroundNormal={colors_dark['surfaceContainerHigh']}
DecorationFocus={colors_dark['primary']}
DecorationHover={colors_dark['primary']}
ForegroundActive={colors_dark['onSurface']}
ForegroundInactive={colors_dark['outline']}
ForegroundLink={extras['link']['dark']['primary']}
ForegroundNegative={extras['negative']['dark']['primary']}
ForegroundNeutral={extras['neutral']['dark']['primary']}
ForegroundNormal={colors_dark['onSurface']}
ForegroundPositive={extras['positive']['dark']['primary']}
ForegroundVisited={extras['visited']['dark']['primary']}

[Colors:Complementary]
BackgroundAlternate={colors_dark['surface']}
BackgroundNormal={colors_dark['surfaceContainer']}
DecorationFocus={colors_dark['primary']}
DecorationHover={colors_dark['primary']}
ForegroundActive={colors_dark['inverseSurface']}
ForegroundInactive={colors_dark['outline']}
ForegroundLink={extras['link']['dark']['primary']}
ForegroundNegative={extras['negative']['dark']['primary']}
ForegroundNeutral={extras['neutral']['dark']['primary']}
ForegroundNormal={colors_dark['onSurfaceVariant']}
ForegroundPositive={extras['positive']['dark']['primary']}
ForegroundVisited={extras['visited']['dark']['primary']}

[Colors:Header]
BackgroundAlternate={colors_dark['surfaceContainer']}
BackgroundNormal={colors_dark['surfaceContainer']}
DecorationFocus={colors_dark['primary']}
DecorationHover={colors_dark['primary']}
ForegroundActive={colors_dark['inverseSurface']}
ForegroundInactive={colors_dark['outline']}
ForegroundLink={extras['link']['dark']['primary']}
ForegroundNegative={extras['negative']['dark']['primary']}
ForegroundNeutral={extras['neutral']['dark']['primary']}
ForegroundNormal={colors_dark['onSurfaceVariant']}
ForegroundPositive={extras['positive']['dark']['primary']}
ForegroundVisited={extras['visited']['dark']['primary']}

[Colors:Header][Inactive]
BackgroundAlternate={colors_dark['surfaceContainer']}
BackgroundNormal={colors_dark['surfaceContainer']}
DecorationFocus={colors_dark['primary']}
DecorationHover={colors_dark['primary']}
ForegroundActive={colors_dark['inverseSurface']}
ForegroundInactive={colors_dark['outline']}
ForegroundLink={extras['link']['dark']['primary']}
ForegroundNegative={extras['negative']['dark']['primary']}
ForegroundNeutral={extras['neutral']['dark']['primary']}
ForegroundNormal={colors_dark['onSurfaceVariant']}
ForegroundPositive={extras['positive']['dark']['primary']}
ForegroundVisited={extras['visited']['dark']['primary']}

[Colors:Selection]
BackgroundAlternate={colors_dark['primary']}
BackgroundNormal={colors_dark['primary']}
DecorationFocus={colors_dark['primary']}
DecorationHover={colors_dark['secondary']}
ForegroundActive={colors_dark['onPrimary']}
ForegroundInactive={colors_dark['onPrimary']}
ForegroundLink={extras['link']['dark']['onPrimaryFixedVariant']}
ForegroundNegative={extras['negative']['dark']['onPrimaryFixedVariant']}
ForegroundNeutral={extras['neutral']['dark']['onPrimaryFixedVariant']}
ForegroundNormal={colors_dark['onPrimary']}
ForegroundPositive={extras['positive']['dark']['onPrimaryFixedVariant']}
ForegroundVisited={extras['visited']['dark']['onPrimaryFixedVariant']}

[Colors:Tooltip]
BackgroundAlternate={colors_dark['surfaceVariant']}
BackgroundNormal={colors_dark['surfaceContainer']}
DecorationFocus={colors_dark['primary']}
DecorationHover={colors_dark['primary']}
ForegroundActive={colors_dark['onSurface']}
ForegroundInactive={colors_dark['outline']}
ForegroundLink={extras['link']['dark']['primary']}
ForegroundNegative={extras['negative']['dark']['primary']}
ForegroundNeutral={extras['neutral']['dark']['primary']}
ForegroundNormal={colors_dark['onSurface']}
ForegroundPositive={extras['positive']['dark']['primary']}
ForegroundVisited={extras['visited']['dark']['primary']}

[Colors:View]
BackgroundAlternate={colors_dark['surfaceContainer']}
BackgroundNormal={colors_dark['surfaceDim']}
DecorationFocus={colors_dark['primary']}
#-----------------------------------------------
DecorationHover={colors_dark['inversePrimary']}
ForegroundActive={colors_dark['inverseSurface']}
ForegroundInactive={colors_dark['outline']}
ForegroundLink={extras['link']['dark']['primary']}
ForegroundNegative={extras['negative']['dark']['primary']}
ForegroundNeutral={extras['neutral']['dark']['primary']}
ForegroundNormal={colors_dark['onSurface']}
ForegroundPositive={extras['positive']['dark']['primary']}
ForegroundVisited={extras['visited']['dark']['primary']}

[Colors:Window]
BackgroundAlternate={colors_dark['surfaceVariant']}
BackgroundNormal={colors_dark['surfaceContainer']}
DecorationFocus={colors_dark['primary']}
DecorationHover={colors_dark['primary']}
ForegroundActive={extras['link']['dark']['primary']}
ForegroundInactive={colors_dark['outline']}
ForegroundLink={extras['link']['dark']['primary']}
ForegroundNegative={extras['negative']['dark']['primary']}
ForegroundNeutral={extras['neutral']['dark']['primary']}
#--- Window titles, context icons
ForegroundNormal={colors_dark['onSurfaceVariant']}
ForegroundPositive={extras['positive']['dark']['primary']}
ForegroundVisited={extras['visited']['dark']['primary']}

[General]
ColorScheme=MaterialYouDark
Name=Material You dark
shadeSortColumn=true

[KDE]
contrast=4

[WM]
activeBackground={hex2alpha(colors_dark['surfaceContainerHighest'],toolbar_opacity_dark)}
activeBlend=252,252,252
activeForeground={colors_dark['onSurface']}
inactiveBackground={hex2alpha(colors_dark['secondaryContainer'],toolbar_opacity_dark)}
inactiveBlend=161,169,177
inactiveForeground={colors_dark['onSecondaryContainer']}
        """

        self._wal_light_scheme = {
            "wallpaper": wallpaper_data,
            "checksum": "",
            "alpha": "100",
            "special": {
                "background": pywal_colors_light[0],
                "backgroundIntense": blendColors(
                    tones_neutral[8], colors_light["primary"], 0.0
                ),
                "backgroundFaint": blendColors(
                    tones_neutral[8], colors_light["primary"], 0.35
                ),
                "foreground": blendColors(
                    pywal_colors_light[0], tones_secondary[25], 0.98
                ),
                "foregroundIntense": tones_secondary[25],
                "foregroundFaint": blendColors(
                    pywal_colors_light[0], tones_secondary[25], 0.88
                ),
                "cursor": colors_dark["onSurface"],
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
                "color23": pywal_colors_light_faint[7],
            },
        }

        self._wal_dark_scheme = {
            "wallpaper": wallpaper_data,
            "checksum": "",
            "alpha": "100",
            "special": {
                "background": pywal_colors_dark[0],
                "backgroundIntense": blendColors(
                    tones_neutral[8], colors_dark["primary"], 0.0
                ),
                "backgroundFaint": blendColors(
                    tones_neutral[8], colors_dark["primary"], 0.35
                ),
                # Normal, ansi 39
                "foreground": blendColors(
                    pywal_colors_dark[0], tones_secondary[90], 0.98
                ),
                # bold, ansi 39
                "foregroundIntense": tones_secondary[90],
                # faint, ansi 39
                "foregroundFaint": blendColors(
                    pywal_colors_dark[0], tones_secondary[90], 0.88
                ),
                "cursor": colors_dark["onSurface"],
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
                "color23": pywal_colors_dark_faint[7],
            },
        }
        dark_active = colors_dark["onBackground"]
        dark_inactive = colors_dark["surfaceContainerHighest"]

        light_active = colors_light["onBackground"]
        light_inactive = colors_light["surfaceContainerHighest"]

        self._sierra_breeze_dark_colors = {
            "btn_close_active_color": string_utils.tup2str(
                hex2rgb(blendColors(dark_active, tones_primary[80], 0.7))
            ),
            "btn_minimize_active_color": string_utils.tup2str(
                hex2rgb(blendColors(dark_active, tones_primary[70], 0.7))
            ),
            "btn_maximize_active_color": string_utils.tup2str(
                hex2rgb(blendColors(dark_active, tones_primary[70], 0.7))
            ),
            "btn_keep_above_active_color": string_utils.tup2str(
                hex2rgb(blendColors(dark_active, "#118cff", 0.7))
            ),
            "btn_keep_below_active_color": string_utils.tup2str(
                hex2rgb(blendColors(dark_active, "#5d00b9", 0.7))
            ),
            "btn_on_all_desktops_active_color": string_utils.tup2str(
                hex2rgb(blendColors(dark_active, "#00b9b9", 0.7))
            ),
            "btn_shade_active_color": string_utils.tup2str(
                hex2rgb(blendColors(dark_active, "#b900b6", 0.7))
            ),
            "btn_inactive_color": string_utils.tup2str(
                hex2rgb(blendColors(dark_inactive, colors_dark["secondary"], 0.32))
            ),
        }

        self._sierra_breeze_light_colors = {
            "btn_close_active_color": string_utils.tup2str(
                hex2rgb(blendColors(tones_primary[50], light_active, 0.05))
            ),
            "btn_minimize_active_color": string_utils.tup2str(
                hex2rgb(blendColors(tones_primary[60], light_active, 0.05))
            ),
            "btn_maximize_active_color": string_utils.tup2str(
                hex2rgb(blendColors(tones_primary[70], light_active, 0.05))
            ),
            "btn_keep_above_active_color": string_utils.tup2str(
                hex2rgb(blendColors("#118cff", light_active, 0.05))
            ),
            "btn_keep_below_active_color": string_utils.tup2str(
                hex2rgb(blendColors("#5d00b9", light_active, 0.05))
            ),
            "btn_on_all_desktops_active_color": string_utils.tup2str(
                hex2rgb(blendColors("#00b9b9", light_active, 0.05))
            ),
            "btn_shade_active_color": string_utils.tup2str(
                hex2rgb(blendColors("#b900b6", light_active, 0.05))
            ),
            "btn_inactive_color": string_utils.tup2str(
                hex2rgb(blendColors(light_inactive, colors_light["secondary"], 0.32))
            ),
        }

        self._ksyntax_highlighting_dark = {
            "metadata": {
                "copyright": [
                    "SPDX-FileCopyrightText: 2016 Volker Krause <vkrause@kde.org>",
                    "SPDX-FileCopyrightText: 2016 Dominik Haumann <dhaumann@kde.org>",
                ],
                "license": "SPDX-License-Identifier: MIT",
                "name": "Material You Dark",
                "revision": 7,
            },
            "editor-colors": {
                "BackgroundColor": pywal_colors_dark[0],
                "BracketMatching": tones_secondary[35],
                "CodeFolding": "#224e65",
                "CurrentLine": tones_secondary[20],
                "CurrentLineNumber": colors_dark["onSurface"],
                "IconBorder": pywal_colors_dark[0],
                "IndentationLine": tones_secondary[20],
                "LineNumbers": tones_neutral[45],
                "MarkBookmark": "#0404bf",
                "MarkBreakpointActive": "#8b0607",
                "MarkBreakpointDisabled": "#820683",
                "MarkBreakpointReached": "#6d6e07",
                "MarkError": extras["negative"]["dark"]["onPrimaryFixedVariant"],
                "MarkExecution": "#4d4e50",
                "MarkWarning": extras["neutral"]["dark"]["onPrimaryFixedVariant"],
                "ModifiedLines": "#c04900",
                "ReplaceHighlight": "#808021",
                "SavedLines": "#1c8042",
                "SearchHighlight": "#218058",
                "Separator": "#3f4347",
                "SpellChecking": "#c0392b",
                "TabMarker": "#4d4d4d",
                "TemplateBackground": tones_secondary[20],
                "TemplateFocusedPlaceholder": "#123723",
                "TemplatePlaceholder": "#123723",
                "TemplateReadOnlyPlaceholder": "#4d1f24",
                "TextSelection": tones_secondary[30],
                "WordWrapMarker": "#3a3f44",
            },
            "text-styles": {
                "Alert": {
                    "background-color": "#4d1f24",
                    "bold": "true",
                    "selected-text-color": "#95da4c",
                    "text-color": "#95da4c",
                },
                "Annotation": {
                    "selected-text-color": "#54aa75",
                    "text-color": "#3f8058",
                },
                "Attribute": {
                    "selected-text-color": "#fdbc4b",
                    "text-color": "#2980b9",
                },
                "BaseN": {"selected-text-color": "#f67400", "text-color": "#f67400"},
                "BuiltIn": {"selected-text-color": "#bdc3c7", "text-color": "#7f8c8d"},
                "Char": {"selected-text-color": "#3daee9", "text-color": "#3daee9"},
                "Comment": {"selected-text-color": "#808080", "text-color": "#7a7c7d"},
                "CommentVar": {
                    "selected-text-color": "#94a3a4",
                    "text-color": "#7f8c8d",
                },
                "Constant": {
                    "bold": "true",
                    "selected-text-color": "#27aeae",
                    "text-color": "#27aeae",
                },
                "ControlFlow": {
                    "bold": "true",
                    "selected-text-color": "#fdbc4b",
                    "text-color": "#fdbc4b",
                },
                "DataType": {"selected-text-color": "#fdbc4b", "text-color": "#2980b9"},
                "DecVal": {"selected-text-color": "#f67400", "text-color": "#f67400"},
                "Documentation": {
                    "selected-text-color": "#da4453",
                    "text-color": "#a43340",
                },
                "Error": {
                    "selected-text-color": "#da4453",
                    "text-color": "#da4453",
                    "underline": "true",
                },
                "Extension": {
                    "bold": "true",
                    "selected-text-color": "#bdc3c7",
                    "text-color": "#0099ff",
                },
                "Float": {"selected-text-color": "#f67400", "text-color": "#f67400"},
                "Function": {"selected-text-color": "#af81ff", "text-color": "#8e44ad"},
                "Import": {"selected-text-color": "#27ae60", "text-color": "#27ae60"},
                "Information": {
                    "selected-text-color": "#e46700",
                    "text-color": "#c45b00",
                },
                "Keyword": {
                    "bold": "true",
                    "selected-text-color": colors_dark["onSurface"],
                    "text-color": colors_dark["onSurface"],
                },
                "Normal": {
                    "selected-text-color": colors_dark["onSurface"],
                    "text-color": colors_dark["onSurface"],
                },
                "Operator": {"selected-text-color": "#54aa75", "text-color": "#3f8058"},
                "Others": {"selected-text-color": "#27ae60", "text-color": "#27ae60"},
                "Preprocessor": {
                    "selected-text-color": "#27ae60",
                    "text-color": "#27ae60",
                },
                "RegionMarker": {
                    "background-color": "#153042",
                    "selected-text-color": "#3daee9",
                    "text-color": "#2980b9",
                },
                "SpecialChar": {
                    "selected-text-color": "#3daee9",
                    "text-color": "#3daee9",
                },
                "SpecialString": {
                    "selected-text-color": "#da4453",
                    "text-color": "#da4453",
                },
                "String": {"selected-text-color": "#f44f4f", "text-color": "#f44f4f"},
                "Variable": {"selected-text-color": "#27aeae", "text-color": "#27aeae"},
                "VerbatimString": {
                    "selected-text-color": "#da4453",
                    "text-color": "#da4453",
                },
                "Warning": {"selected-text-color": "#da4453", "text-color": "#da4453"},
            },
            "custom-styles": {},
        }

        self._ksyntax_highlighting_light = {
            "metadata": {
                "copyright": [
                    "SPDX-FileCopyrightText: 2016 Volker Krause <vkrause@kde.org>",
                    "SPDX-FileCopyrightText: 2016 Dominik Haumann <dhaumann@kde.org>",
                ],
                "license": "SPDX-License-Identifier: MIT",
                "revision": 9,
                "name": "Material You Light",
            },
            "editor-colors": {
                "BackgroundColor": pywal_colors_light[0],
                "CodeFolding": "#94caef",
                "BracketMatching": tones_secondary[65],
                "CurrentLine": tones_secondary[80],
                "IconBorder": pywal_colors_light[0],
                "IndentationLine": tones_secondary[80],
                "LineNumbers": tones_neutral[55],
                "CurrentLineNumber": colors_light["onSurface"],
                "MarkBookmark": "#0000ff",
                "MarkBreakpointActive": "#ff0000",
                "MarkBreakpointReached": "#ffff00",
                "MarkBreakpointDisabled": "#ff00ff",
                "MarkExecution": "#a0a0a4",
                "MarkWarning": extras["neutral"]["dark"]["onPrimaryFixedVariant"],
                "MarkError": extras["negative"]["dark"]["onPrimaryFixedVariant"],
                "ModifiedLines": "#fdbc4b",
                "ReplaceHighlight": "#00ff00",
                "SavedLines": "#2ecc71",
                "SearchHighlight": "#ffff00",
                "TextSelection": tones_secondary[80],
                "Separator": "#d5d5d5",
                "SpellChecking": "#bf0303",
                "TabMarker": "#d2d2d2",
                "TemplateBackground": tones_secondary[80],
                "TemplatePlaceholder": "#baf8ce",
                "TemplateFocusedPlaceholder": "#76da98",
                "TemplateReadOnlyPlaceholder": "#f6e6e6",
                "WordWrapMarker": "#ededed",
            },
            "text-styles": {
                "Normal": {
                    "text-color": colors_light["onSurface"],
                    "selected-text-color": colors_light["onSurface"],
                    "bold": "false",
                    "italic": "false",
                    "underline": "false",
                    "strike-through": "false",
                },
                "Keyword": {
                    "text-color": colors_light["onSurface"],
                    "selected-text-color": "#ffffff",
                    "bold": "true",
                },
                "Function": {"text-color": "#644a9b", "selected-text-color": "#452886"},
                "Variable": {"text-color": "#0057ae", "selected-text-color": "#00316e"},
                "ControlFlow": {
                    "text-color": colors_light["onSurface"],
                    "selected-text-color": "#ffffff",
                    "bold": "true",
                },
                "Operator": {"text-color": "#ca60ca", "selected-text-color": "#a44ea4"},
                "BuiltIn": {
                    "text-color": "#644a9b",
                    "selected-text-color": "#452886",
                    "bold": "true",
                },
                "Extension": {
                    "text-color": "#0095ff",
                    "selected-text-color": "#ffffff",
                    "bold": "true",
                },
                "Preprocessor": {
                    "text-color": "#006e28",
                    "selected-text-color": "#006e28",
                },
                "Attribute": {
                    "text-color": "#0057ae",
                    "selected-text-color": "#00316e",
                },
                "Char": {"text-color": "#924c9d", "selected-text-color": "#6c2477"},
                "SpecialChar": {
                    "text-color": "#3daee9",
                    "selected-text-color": "#fcfcfc",
                },
                "String": {"text-color": "#bf0303", "selected-text-color": "#9c0e0e"},
                "VerbatimString": {
                    "text-color": "#e31616",
                    "selected-text-color": "#9c0e0e",
                },
                "SpecialString": {
                    "text-color": "#ff5500",
                    "selected-text-color": "#ff5500",
                },
                "Import": {"text-color": "#ff5500", "selected-text-color": "#ff5500"},
                "DataType": {"text-color": "#0057ae", "selected-text-color": "#00316e"},
                "DecVal": {"text-color": "#b08000", "selected-text-color": "#805c00"},
                "BaseN": {"text-color": "#b08000", "selected-text-color": "#805c00"},
                "Float": {"text-color": "#b08000", "selected-text-color": "#805c00"},
                "Constant": {"text-color": "#aa5500", "selected-text-color": "#5e2f00"},
                "Comment": {"text-color": "#898887", "selected-text-color": "#5e5d5d"},
                "Documentation": {
                    "text-color": "#607880",
                    "selected-text-color": "#46585e",
                },
                "Annotation": {
                    "text-color": "#ca60ca",
                    "selected-text-color": "#a44ea4",
                },
                "CommentVar": {
                    "text-color": "#0095ff",
                    "selected-text-color": "#ffffff",
                },
                "RegionMarker": {
                    "text-color": "#0057ae",
                    "selected-text-color": "#00316e",
                    "background-color": "#e0e9f8",
                },
                "Information": {
                    "text-color": "#b08000",
                    "selected-text-color": "#805c00",
                },
                "Warning": {"text-color": "#bf0303", "selected-text-color": "#9c0e0e"},
                "Alert": {
                    "text-color": "#bf0303",
                    "selected-text-color": "#9c0e0e",
                    "background-color": "#f7e6e6",
                    "bold": "true",
                },
                "Error": {
                    "text-color": "#bf0303",
                    "selected-text-color": "#9c0e0e",
                    "underline": "true",
                },
                "Others": {"text-color": "#006e28", "selected-text-color": "#006e28"},
            },
            "custom-styles": {},
        }

    def get_material_schemes(self):
        return self._material_you_schemes

    def get_extras(self):
        return self._extras

    def get_light_scheme(self):
        return self._light_scheme

    def get_dark_scheme(self):
        return self._dark_scheme

    def get_wal_light_scheme(self):
        return self._wal_light_scheme

    def get_wal_dark_scheme(self):
        return self._wal_dark_scheme

    def get_sierra_breeze_dark_colors(self):
        return self._sierra_breeze_dark_colors

    def get_sierra_breeze_light_colors(self):
        return self._sierra_breeze_light_colors

    def get_ksyntax_highlighting_dark(self):
        return self._ksyntax_highlighting_dark

    def get_ksyntax_highlighting_light(self):
        return self._ksyntax_highlighting_light
