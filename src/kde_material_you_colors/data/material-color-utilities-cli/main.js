import {
  Hct,
  MaterialDynamicColors,
  QuantizerCelebi,
  Score,
  hexFromArgb
} from "@material/material-color-utilities";
import {
  getScheme,
  getColors,
  obj_to_rgb_array,
  tones_from_palette,
  customColor,
} from './utils.js'
import { readFileSync } from 'fs';

const filename = process.argv[2];
const jsonStr = readFileSync(filename, 'utf-8');


const source_info = JSON.parse(jsonStr)

const pixels = source_info["pixels"]
const custom_colors = source_info["custom_colors"]
var ncolor = source_info["ncolor"]
const multipliers = source_info["mult"]
const chroma_mult_light = source_info["mult"]["chroma"]["light"]
const chroma_mult_dark = source_info["mult"]["chroma"]["dark"]

// Convert Pixels to Material Colors
const result = QuantizerCelebi.quantize(pixels, 128);
const ranked = Score.score(result, { desired: 7, fallbackColorARGB: 0xff4285f4, filter: true });
var argb = ranked[0];

// get source color from ranked and ncolor
if (ranked.length > ncolor) {
  argb = ranked[ncolor]
} else {
  argb = ranked[ranked.length - 1]
  ncolor = ranked.length - 1
}

const contrastLevel = 0;
var source = Hct.fromInt(argb);
const scheme_type = source_info["scheme_type"];
const chromaMultiplier = chroma_mult_light;
const chromaMultiplierDark = chroma_mult_dark;
const schemeDark = new getScheme(scheme_type, source, true, contrastLevel, chromaMultiplierDark);
const scheme = new getScheme(scheme_type, source, false, contrastLevel, chromaMultiplier);
let colorsLight = getColors(scheme, 1, 1)
let colorsDark = getColors(schemeDark, 1, 1)

var source_colors = custom_colors.length === 7 ? custom_colors : ranked
let tone = 50
function get_custom_colors(source_colors, scheme_type, scheme, isDark, contrastLevel, chromaMultiplier) {
  var customColors = []
  for (let x = 0; x < 7; x++) {
    if (customColors.length < 7) {
      if (x < source_colors.length) {
        //const custom_scheme = getScheme(scheme_type, Hct.fromInt(source_colors[x]), isDark, contrastLevel, chromaMultiplier);
        //var ss = MaterialDynamicColors.primary.getArgb(custom_scheme)
        customColors.push(source_colors[x])
      } else {
        if (customColors.length < 7) {
          const custom_scheme = getScheme(scheme_type, Hct.fromInt(scheme.primaryPalette.tone(tone)), isDark, contrastLevel, chromaMultiplier);
          // var ss = MaterialDynamicColors.primary.getArgb(custom_scheme)
          customColors.push(custom_scheme.primaryPalette.tone(tone))
        }
        if (customColors.length < 7) {
          const custom_scheme = getScheme(scheme_type, Hct.fromInt(scheme.tertiaryPalette.tone(tone)), isDark, contrastLevel, chromaMultiplier);
          //var ss = MaterialDynamicColors.primary.getArgb(custom_scheme)
          customColors.push(custom_scheme.tertiaryPalette.tone(tone))
        }
        tone += 8
      }
    }
  }
  return customColors
}

var customColors = get_custom_colors(source_colors, scheme_type, scheme, false, contrastLevel, chromaMultiplier)
var customColorsDark = get_custom_colors(source_colors, scheme_type, schemeDark, true, contrastLevel, chromaMultiplierDark)

//customColors = customColors.map((c) => ({ 'value': c, 'name': c, 'blend': true }))
//customColorsDark = customColorsDark.map((c) => ({ 'value': c, 'name': c, 'blend': false }))

let out = {
  "best": ranked.map((c) => hexFromArgb(c)),
  "source": { "index": ncolor, "color": hexFromArgb(argb) },
  "schemes": {
    "light": colorsLight,
    "dark": colorsDark
  },
  "palettes": {
    "light": {
      "primary": obj_to_rgb_array(tones_from_palette(scheme.primaryPalette)),
      "secondary": obj_to_rgb_array(tones_from_palette(scheme.secondaryPalette)),
      "tertiary": obj_to_rgb_array(tones_from_palette(scheme.tertiaryPalette)),
      "neutral": obj_to_rgb_array(tones_from_palette(scheme.neutralPalette)),
      "neutralVariant": obj_to_rgb_array(tones_from_palette(scheme.neutralVariantPalette)),
      "error": obj_to_rgb_array(tones_from_palette(scheme.errorPalette)),
    },
    "dark": {
      "primary": obj_to_rgb_array(tones_from_palette(schemeDark.primaryPalette)),
      "secondary": obj_to_rgb_array(tones_from_palette(schemeDark.secondaryPalette)),
      "tertiary": obj_to_rgb_array(tones_from_palette(schemeDark.tertiaryPalette)),
      "neutral": obj_to_rgb_array(tones_from_palette(schemeDark.neutralPalette)),
      "neutralVariant": obj_to_rgb_array(tones_from_palette(schemeDark.neutralVariantPalette)),
      "error": obj_to_rgb_array(tones_from_palette(schemeDark.errorPalette)),
    }
  },
  "customColors": {
    light: customColors.map((c) => hexFromArgb(c)),
    dark: customColorsDark.map((c) => hexFromArgb(c))
  },
  // "source_info": source_info
}
console.log(JSON.stringify(out, null, 2))

/* TODO:
- Best colors {}
- ncolor
- 
*/
