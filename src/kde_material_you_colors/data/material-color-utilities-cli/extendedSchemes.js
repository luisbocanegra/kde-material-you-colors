import {
  TonalPalette,
  DynamicScheme,
  DislikeAnalyzer,
  TemperatureCache,
} from "@material/material-color-utilities";

import { Variant } from './node_modules/@material/material-color-utilities/scheme/variant.js'
import * as math from './node_modules/@material/material-color-utilities/utils/math_utils.js';
import { clamp } from "./utils.js";

/** A Dynamic Color theme that is grayscale. */
export class ExtendedSchemeMonochrome extends DynamicScheme {
  constructor(sourceColorHct, isDark, contrastLevel, chromaMultiplier) {
    super({
      sourceColorArgb: sourceColorHct.toInt(),
      variant: Variant.MONOCHROME,
      contrastLevel,
      isDark,
      primaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(0.0 * chromaMultiplier)),
      secondaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(0.0 * chromaMultiplier)),
      tertiaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(0.0 * chromaMultiplier)),
      neutralPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(0.0 * chromaMultiplier)),
      neutralVariantPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(0.0 * chromaMultiplier)),
    });
  }
}

/** A Dynamic Color theme that is near grayscale. */
export class ExtendedSchemeNeutral extends DynamicScheme {
  constructor(sourceColorHct, isDark, contrastLevel, chromaMultiplier) {
    super({
      sourceColorArgb: sourceColorHct.toInt(),
      variant: Variant.NEUTRAL,
      contrastLevel,
      isDark,
      primaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(12.0 * chromaMultiplier)),
      secondaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(8.0 * chromaMultiplier)),
      tertiaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(16.0 * chromaMultiplier)),
      neutralPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(2.0 * chromaMultiplier)),
      neutralVariantPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(2.0 * chromaMultiplier)),
    });
  }
}

/**
 * A Dynamic Color theme with low to medium colorfulness and a Tertiary
 * TonalPalette with a hue related to the source color.
 *
 * The default Material You theme on Android 12 and 13.
 */
export class ExtendedSchemeTonalSpot extends DynamicScheme {
  constructor(sourceColorHct, isDark, contrastLevel, chromaMultiplier) {
    super({
      sourceColorArgb: sourceColorHct.toInt(),
      variant: Variant.TONAL_SPOT,
      contrastLevel,
      isDark,
      primaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(36.0 * chromaMultiplier)),
      secondaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(16.0 * chromaMultiplier)),
      tertiaryPalette: TonalPalette.fromHueAndChroma(math.sanitizeDegreesDouble(sourceColorHct.hue + 60.0), clamp(24.0 * chromaMultiplier)),
      neutralPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(6.0 * chromaMultiplier)),
      neutralVariantPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(8.0 * chromaMultiplier)),
    });
  }
}

/**
 * A Dynamic Color theme that maxes out colorfulness at each position in the
 * Primary Tonal Palette.
 */
export class ExtendedSchemeVibrant extends DynamicScheme {
  constructor(sourceColorHct, isDark, contrastLevel, chromaMultiplier) {
    super({
      sourceColorArgb: sourceColorHct.toInt(),
      variant: Variant.VIBRANT,
      contrastLevel,
      isDark,
      primaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(200.0 * chromaMultiplier)),
      secondaryPalette: TonalPalette.fromHueAndChroma(DynamicScheme.getRotatedHue(sourceColorHct, ExtendedSchemeVibrant.hues, ExtendedSchemeVibrant.secondaryRotations), clamp(24.0 * chromaMultiplier)),
      tertiaryPalette: TonalPalette.fromHueAndChroma(DynamicScheme.getRotatedHue(sourceColorHct, ExtendedSchemeVibrant.hues, ExtendedSchemeVibrant.tertiaryRotations), clamp(32.0 * chromaMultiplier)),
      neutralPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(10.0 * chromaMultiplier)),
      neutralVariantPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(12.0 * chromaMultiplier)),
    });
  }
}
/**
* Hues (in degrees) used at breakpoints such that designers can specify a
* hue rotation that occurs at a given break point.
*/
ExtendedSchemeVibrant.hues = [
  0.0,
  41.0,
  61.0,
  101.0,
  131.0,
  181.0,
  251.0,
  301.0,
  360.0,
];
/**
* Hue rotations (in degrees) of the Secondary [TonalPalette],
* corresponding to the breakpoints in [hues].
*/
ExtendedSchemeVibrant.secondaryRotations = [
  18.0,
  15.0,
  10.0,
  12.0,
  15.0,
  18.0,
  15.0,
  12.0,
  12.0,
];
/**
* Hue rotations (in degrees) of the Tertiary [TonalPalette],
* corresponding to the breakpoints in [hues].
*/
ExtendedSchemeVibrant.tertiaryRotations = [
  35.0,
  30.0,
  20.0,
  25.0,
  30.0,
  35.0,
  30.0,
  25.0,
  25.0,
];

/**
 * A Dynamic Color theme that is intentionally detached from the source color.
 */
export class ExtendedSchemeExpressive extends DynamicScheme {
  constructor(sourceColorHct, isDark, contrastLevel, chromaMultiplier) {
    super({
      sourceColorArgb: sourceColorHct.toInt(),
      variant: Variant.EXPRESSIVE,
      contrastLevel,
      isDark,
      primaryPalette: TonalPalette.fromHueAndChroma(math.sanitizeDegreesDouble(sourceColorHct.hue + 240.0), clamp(40.0 * chromaMultiplier)),
      secondaryPalette: TonalPalette.fromHueAndChroma(DynamicScheme.getRotatedHue(sourceColorHct, ExtendedSchemeExpressive.hues, ExtendedSchemeExpressive.secondaryRotations), clamp(24.0 * chromaMultiplier)),
      tertiaryPalette: TonalPalette.fromHueAndChroma(DynamicScheme.getRotatedHue(sourceColorHct, ExtendedSchemeExpressive.hues, ExtendedSchemeExpressive.tertiaryRotations), clamp(32.0 * chromaMultiplier)),
      neutralPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue + 15, clamp(8.0 * chromaMultiplier)),
      neutralVariantPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue + 15, clamp(12.0 * chromaMultiplier)),
    });
  }
}
/**
* Hues (in degrees) used at breakpoints such that designers can specify a
* hue rotation that occurs at a given break point.
*/
ExtendedSchemeExpressive.hues = [
  0.0,
  21.0,
  51.0,
  121.0,
  151.0,
  191.0,
  271.0,
  321.0,
  360.0,
];
/**
* Hue rotations (in degrees) of the Secondary [TonalPalette],
* corresponding to the breakpoints in [hues].
*/
ExtendedSchemeExpressive.secondaryRotations = [
  45.0,
  95.0,
  45.0,
  20.0,
  45.0,
  90.0,
  45.0,
  45.0,
  45.0,
];
/**
* Hue rotations (in degrees) of the Tertiary [TonalPalette],
* corresponding to the breakpoints in [hues].
*/
ExtendedSchemeExpressive.tertiaryRotations = [
  120.0,
  120.0,
  20.0,
  45.0,
  20.0,
  15.0,
  20.0,
  120.0,
  120.0,
];

/**
 * A scheme that places the source color in `Scheme.primaryContainer`.
 *
 * Primary Container is the source color, adjusted for color relativity.
 * It maintains constant appearance in light mode and dark mode.
 * This adds ~5 tone in light mode, and subtracts ~5 tone in dark mode.
 * Tertiary Container is the complement to the source color, using
 * `TemperatureCache`. It also maintains constant appearance.
 */
export class ExtendedSchemeFidelity extends DynamicScheme {
  constructor(sourceColorHct, isDark, contrastLevel, chromaMultiplier) {
    const newSourceColorHct = sourceColorHct
    newSourceColorHct.chroma = sourceColorHct.chroma * chromaMultiplier
    super({
      sourceColorArgb: sourceColorHct.toInt(),
      variant: Variant.FIDELITY,
      contrastLevel,
      isDark,
      primaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(sourceColorHct.chroma * chromaMultiplier)),
      secondaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(Math.max(sourceColorHct.chroma - 32.0, sourceColorHct.chroma * 0.5) * chromaMultiplier)),
      tertiaryPalette: TonalPalette.fromInt(DislikeAnalyzer
        .fixIfDisliked(new TemperatureCache(newSourceColorHct).complement)
        .toInt()),
      neutralPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp((sourceColorHct.chroma / 8.0) * chromaMultiplier)),
      neutralVariantPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp((sourceColorHct.chroma / 8.0 + 4.0) * chromaMultiplier)),
    });
  }
}

/**
 * A scheme that places the source color in `Scheme.primaryContainer`.
 *
 * Primary Container is the source color, adjusted for color relativity.
 * It maintains constant appearance in light mode and dark mode.
 * This adds ~5 tone in light mode, and subtracts ~5 tone in dark mode.
 * Tertiary Container is the complement to the source color, using
 * `TemperatureCache`. It also maintains constant appearance.
 */
export class ExtendedSchemeContent extends DynamicScheme {
  constructor(sourceColorHct, isDark, contrastLevel, chromaMultiplier) {
    const newSourceColorHct = sourceColorHct
    newSourceColorHct.chroma = sourceColorHct.chroma * chromaMultiplier
    super({
      sourceColorArgb: sourceColorHct.toInt(),
      variant: Variant.CONTENT,
      contrastLevel,
      isDark,
      primaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(sourceColorHct.chroma * chromaMultiplier)),
      secondaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(Math.max(sourceColorHct.chroma - 32.0, sourceColorHct.chroma * 0.5) * chromaMultiplier)),
      tertiaryPalette: TonalPalette.fromInt(DislikeAnalyzer
        .fixIfDisliked(new TemperatureCache(newSourceColorHct).analogous(3, 6)[2])
        .toInt()),
      neutralPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp((sourceColorHct.chroma / 8.0) * chromaMultiplier)),
      neutralVariantPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp((sourceColorHct.chroma / 8.0 + 4.0) * chromaMultiplier)),
    });
  }
}

/**
 * A playful theme - the source color's hue does not appear in the theme.
 */
export class ExtendedSchemeRainbow extends DynamicScheme {
  constructor(sourceColorHct, isDark, contrastLevel, chromaMultiplier) {
    super({
      sourceColorArgb: sourceColorHct.toInt(),
      variant: Variant.RAINBOW,
      contrastLevel,
      isDark,
      primaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(48.0 * chromaMultiplier)),
      secondaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(16.0 * chromaMultiplier)),
      tertiaryPalette: TonalPalette.fromHueAndChroma(math.sanitizeDegreesDouble(sourceColorHct.hue + 60.0), clamp(24.0 * chromaMultiplier)),
      neutralPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(0.0 * chromaMultiplier)),
      neutralVariantPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(0.0 * chromaMultiplier)),
    });
  }
}

/**
 * A playful theme - the source color's hue does not appear in the theme.
 */
export class ExtendedSchemeFruitSalad extends DynamicScheme {
  constructor(sourceColorHct, isDark, contrastLevel, chromaMultiplier) {
    super({
      sourceColorArgb: sourceColorHct.toInt(),
      variant: Variant.FRUIT_SALAD,
      contrastLevel,
      isDark,
      primaryPalette: TonalPalette.fromHueAndChroma(math.sanitizeDegreesDouble(sourceColorHct.hue - 50.0), clamp(48.0 * chromaMultiplier)),
      secondaryPalette: TonalPalette.fromHueAndChroma(math.sanitizeDegreesDouble(sourceColorHct.hue - 50.0), clamp(36.0 * chromaMultiplier)),
      tertiaryPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(36.0 * chromaMultiplier)),
      neutralPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(10.0 * chromaMultiplier)),
      neutralVariantPalette: TonalPalette.fromHueAndChroma(sourceColorHct.hue, clamp(16.0 * chromaMultiplier)),
    });
  }
}
