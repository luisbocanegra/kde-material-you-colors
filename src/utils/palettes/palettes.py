
from material_color_utilities_python.hct.hct import *
from material_color_utilities_python.palettes.tonal_palette import *

# /**
#  * A scheme that places the source color in `Scheme.primaryContainer`.
#  *
#  * Primary Container is the source color, adjusted for color relativity.
#  * It maintains constant appearance in light mode and dark mode.
#  * This adds ~5 tone in light mode, and subtracts ~5 tone in dark mode.
#  * Tertiary Container is the complement to the source color, using
#  * `TemperatureCache`. It also maintains constant appearance.
#  */
class FidelityPalette:
    def __init__(self, argb):
        hct = Hct.fromInt(argb)
        chroma = hct.chroma
        hue = hct.hue
        self.a1 = TonalPalette.fromHueAndChroma(hue, chroma)
        self.a2 = TonalPalette.fromHueAndChroma(hue, max(chroma - 32.0, chroma * 0.5))
        self.a3 = TonalPalette.fromHueAndChroma(hue, 16.0) # TODO add DislikeAnalyzer
        self.n1 = TonalPalette.fromHueAndChroma(hue, chroma / 8.0)
        self.n2 = TonalPalette.fromHueAndChroma(hue, chroma / 8.0 + 4.0)
        self.error = TonalPalette.fromHueAndChroma(25, 84)

    # /**
    #  * @param argb ARGB representation of a color
    #  */
    @staticmethod
    def of(argb):
        return FidelityPalette(argb)

# /** A Color Palette that is grayscale. */
class MonochromePalette:
    def __init__(self, argb):
        hct = Hct.fromInt(argb)
        hue = hct.hue
        self.a1 = TonalPalette.fromHueAndChroma(hue, 0.0)
        self.a2 = TonalPalette.fromHueAndChroma(hue, 0.0)
        self.a3 = TonalPalette.fromHueAndChroma(hue, 0.0)
        self.n1 = TonalPalette.fromHueAndChroma(hue, 0.0)
        self.n2 = TonalPalette.fromHueAndChroma(hue, 0.0)
        self.error = TonalPalette.fromHueAndChroma(25, 84)

    # /**
    #  * @param argb ARGB representation of a color
    #  */
    @staticmethod
    def of(argb):
        return MonochromePalette(argb);

# /** A Color Palette that is near grayscale. */
class NeutralPalette:
    def __init__(self, argb):
        hct = Hct.fromInt(argb)
        hue = hct.hue
        self.a1 = TonalPalette.fromHueAndChroma(hue, 12.0)
        self.a2 = TonalPalette.fromHueAndChroma(hue, 8.0)
        self.a3 = TonalPalette.fromHueAndChroma(hue, 16.0)
        self.n1 = TonalPalette.fromHueAndChroma(hue, 2.0)
        self.n2 = TonalPalette.fromHueAndChroma(hue, 2.0)
        self.error = TonalPalette.fromHueAndChroma(25, 84)

    # /**
    #  * @param argb ARGB representation of a color
    #  */
    @staticmethod
    def of(argb):
        return NeutralPalette(argb)


# /**
#  * A Dynamic Color theme with low to medium colorfulness and a Tertiary
#  * TonalPalette with a hue related to the source color.
#  *
#  * The default Material You theme on Android 12 and 13.
#  */
class TonalSpotPalette:
    def __init__(self, argb):
        hct = Hct.fromInt(argb)
        hue = hct.hue
        self.a1 = TonalPalette.fromHueAndChroma(hue, 40.0)
        self.a2 = TonalPalette.fromHueAndChroma(hue, 16.0)
        self.a3 = TonalPalette.fromHueAndChroma(sanitizeDegreesDouble(hue + 60.0), 24.0) # TODO add DislikeAnalyzer
        self.n1 = TonalPalette.fromHueAndChroma(hue, 6.0)
        self.n2 = TonalPalette.fromHueAndChroma(hue, 8.0)
        self.error = TonalPalette.fromHueAndChroma(25, 84)

    # /**
    #  * @param argb ARGB representation of a color
    #  */
    @staticmethod
    def of(argb):
        return TonalSpotPalette(argb)
