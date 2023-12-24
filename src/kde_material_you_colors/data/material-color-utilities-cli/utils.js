import {
  Blend,
  hexFromArgb,
  MaterialDynamicColors,
  CorePalette
} from "@material/material-color-utilities";
import {
  ExtendedSchemeMonochrome,
  ExtendedSchemeNeutral,
  ExtendedSchemeTonalSpot,
  ExtendedSchemeVibrant,
  ExtendedSchemeExpressive,
  ExtendedSchemeFidelity,
  ExtendedSchemeContent,
  ExtendedSchemeRainbow,
  ExtendedSchemeFruitSalad,
} from './extendedSchemes.js'

export function tones_from_palette(palette) {
  var tones = {}
  for (let i = 0; i < 100; i++) {
    tones[i] = palette.tone(i)
  }
  return tones
}

export function obj_to_rgb_array(scheme) {
  var out = []
  for (let key in scheme) {
    let color = scheme[key]
    out.push(hexFromArgb(color))
  }
  return out
}

export function clamp(value, min = 0, max = 100) {
  return Math.min(Math.max(value, min), max)
}

export function getScheme(scheme_type, source, isDark, contrastLevel, chromaMultiplier) {
  const Class = schemeMap[scheme_type]
  return new Class(source, isDark, contrastLevel, chromaMultiplier)
}

export function multiplyColor(hct, chromaMultiplier = 1, toneMultiplier = 1) {
  hct.chroma = hct.chroma * chromaMultiplier
  hct.tone = hct.tone * toneMultiplier
  return hct.toInt()
}

const schemeMap = {
  0: ExtendedSchemeMonochrome,
  1: ExtendedSchemeNeutral,
  2: ExtendedSchemeTonalSpot,
  3: ExtendedSchemeVibrant,
  4: ExtendedSchemeExpressive,
  5: ExtendedSchemeFidelity,
  6: ExtendedSchemeContent,
  7: ExtendedSchemeRainbow,
  8: ExtendedSchemeFruitSalad,
}

export function getMaterialColor(colorName) {
  return MaterialDynamicColors[colorName]
}


export function getColors(scheme) {
  const colorNames = [
    "background",
    "onBackground",
    "surface",
    "surfaceDim",
    "surfaceBright",
    "surfaceContainerLowest",
    "surfaceContainerLow",
    "surfaceContainer",
    "surfaceContainerHigh",
    "surfaceContainerHighest",
    "onSurface",
    "surfaceVariant",
    "onSurfaceVariant",
    "inverseSurface",
    "inverseOnSurface",
    "outline",
    "outlineVariant",
    "shadow",
    "scrim",
    "surfaceTint",
    "primary",
    "onPrimary",
    "primaryContainer",
    "onPrimaryContainer",
    "inversePrimary",
    "secondary",
    "onSecondary",
    "secondaryContainer",
    "onSecondaryContainer",
    "tertiary",
    "onTertiary",
    "tertiaryContainer",
    "onTertiaryContainer",
    "error",
    "onError",
    "errorContainer",
    "onErrorContainer"
  ]
  const result = {}
  for (const colorName of colorNames) {
    const materialColor = getMaterialColor(colorName)
    // const newColor = multiplyColor(materialColor.getHct(scheme), chromaMultiplier, toneMultiplier);
    result[colorName] = hexFromArgb(materialColor.getArgb(scheme))
  }
  return result
}



/**
 * Generate custom color group from source and target color
 * from utils/theme_utils.js
 *
 * @param source Source color
 * @param color Custom color
 * @return Custom color group
 *
 * @link https://m3.material.io/styles/color/the-color-system/color-roles
 */
export function customColor(source, color) {
  let value = color.value;
  const from = value;
  const to = source;
  if (color.blend) {
    value = Blend.harmonize(from, to);
  }
  const palette = CorePalette.of(value);
  const tones = palette.a1;
  return {
    // original
    "color": { value: color.value, name: hexFromArgb(color.value), blend: color.blend },
    // custom color
    "value": hexFromArgb(value),
    light: {
      color: hexFromArgb(tones.tone(40)),
      onColor: hexFromArgb(tones.tone(100)),
      colorContainer: hexFromArgb(tones.tone(90)),
      onColorContainer: hexFromArgb(tones.tone(10)),
    },
    dark: {
      color: hexFromArgb(tones.tone(80)),
      onColor: hexFromArgb(tones.tone(20)),
      colorContainer: hexFromArgb(tones.tone(30)),
      onColorContainer: hexFromArgb(tones.tone(90)),
    },
  };
}
