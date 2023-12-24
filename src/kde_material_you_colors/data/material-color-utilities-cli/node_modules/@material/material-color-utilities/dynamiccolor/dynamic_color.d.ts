/**
 * @license
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import { Hct } from '../hct/hct.js';
import { TonalPalette } from '../palettes/tonal_palette.js';
import { DynamicScheme } from '../scheme/dynamic_scheme.js';
import { ContrastCurve } from './contrast_curve.js';
import { ToneDeltaPair } from './tone_delta_pair.js';
/**
 * @param name The name of the dynamic color. Defaults to empty.
 * @param palette Function that provides a TonalPalette given
 * DynamicScheme. A TonalPalette is defined by a hue and chroma, so this
 * replaces the need to specify hue/chroma. By providing a tonal palette, when
 * contrast adjustments are made, intended chroma can be preserved.
 * @param tone Function that provides a tone given DynamicScheme.
 * @param isBackground Whether this dynamic color is a background, with
 * some other color as the foreground. Defaults to false.
 * @param background The background of the dynamic color (as a function of a
 *     `DynamicScheme`), if it exists.
 * @param secondBackground A second background of the dynamic color (as a
 *     function of a `DynamicScheme`), if it
 * exists.
 * @param contrastCurve A `ContrastCurve` object specifying how its contrast
 * against its background should behave in various contrast levels options.
 * @param toneDeltaPair A `ToneDeltaPair` object specifying a tone delta
 * constraint between two colors. One of them must be the color being
 * constructed.
 */
interface FromPaletteOptions {
    name?: string;
    palette: (scheme: DynamicScheme) => TonalPalette;
    tone: (scheme: DynamicScheme) => number;
    isBackground?: boolean;
    background?: (scheme: DynamicScheme) => DynamicColor;
    secondBackground?: (scheme: DynamicScheme) => DynamicColor;
    contrastCurve?: ContrastCurve;
    toneDeltaPair?: (scheme: DynamicScheme) => ToneDeltaPair;
}
/**
 * A color that adjusts itself based on UI state provided by DynamicScheme.
 *
 * Colors without backgrounds do not change tone when contrast changes. Colors
 * with backgrounds become closer to their background as contrast lowers, and
 * further when contrast increases.
 *
 * Prefer static constructors. They require either a hexcode, a palette and
 * tone, or a hue and chroma. Optionally, they can provide a background
 * DynamicColor.
 */
export declare class DynamicColor {
    readonly name: string;
    readonly palette: (scheme: DynamicScheme) => TonalPalette;
    readonly tone: (scheme: DynamicScheme) => number;
    readonly isBackground: boolean;
    readonly background?: (scheme: DynamicScheme) => DynamicColor;
    readonly secondBackground?: (scheme: DynamicScheme) => DynamicColor;
    readonly contrastCurve?: ContrastCurve;
    readonly toneDeltaPair?: (scheme: DynamicScheme) => ToneDeltaPair;
    private readonly hctCache;
    /**
     * Create a DynamicColor defined by a TonalPalette and HCT tone.
     *
     * @param args Functions with DynamicScheme as input. Must provide a palette
     * and tone. May provide a background DynamicColor and ToneDeltaConstraint.
     */
    static fromPalette(args: FromPaletteOptions): DynamicColor;
    /**
     * The base constructor for DynamicColor.
     *
     * _Strongly_ prefer using one of the convenience constructors. This class is
     * arguably too flexible to ensure it can support any scenario. Functional
     * arguments allow  overriding without risks that come with subclasses.
     *
     * For example, the default behavior of adjust tone at max contrast
     * to be at a 7.0 ratio with its background is principled and
     * matches accessibility guidance. That does not mean it's the desired
     * approach for _every_ design system, and every color pairing,
     * always, in every case.
     *
     * @param name The name of the dynamic color. Defaults to empty.
     * @param palette Function that provides a TonalPalette given
     * DynamicScheme. A TonalPalette is defined by a hue and chroma, so this
     * replaces the need to specify hue/chroma. By providing a tonal palette, when
     * contrast adjustments are made, intended chroma can be preserved.
     * @param tone Function that provides a tone, given a DynamicScheme.
     * @param isBackground Whether this dynamic color is a background, with
     * some other color as the foreground. Defaults to false.
     * @param background The background of the dynamic color (as a function of a
     *     `DynamicScheme`), if it exists.
     * @param secondBackground A second background of the dynamic color (as a
     *     function of a `DynamicScheme`), if it
     * exists.
     * @param contrastCurve A `ContrastCurve` object specifying how its contrast
     * against its background should behave in various contrast levels options.
     * @param toneDeltaPair A `ToneDeltaPair` object specifying a tone delta
     * constraint between two colors. One of them must be the color being
     * constructed.
     */
    constructor(name: string, palette: (scheme: DynamicScheme) => TonalPalette, tone: (scheme: DynamicScheme) => number, isBackground: boolean, background?: (scheme: DynamicScheme) => DynamicColor, secondBackground?: (scheme: DynamicScheme) => DynamicColor, contrastCurve?: ContrastCurve, toneDeltaPair?: (scheme: DynamicScheme) => ToneDeltaPair);
    /**
     * Return a ARGB integer (i.e. a hex code).
     *
     * @param scheme Defines the conditions of the user interface, for example,
     * whether or not it is dark mode or light mode, and what the desired
     * contrast level is.
     */
    getArgb(scheme: DynamicScheme): number;
    /**
     * Return a color, expressed in the HCT color space, that this
     * DynamicColor is under the conditions in scheme.
     *
     * @param scheme Defines the conditions of the user interface, for example,
     * whether or not it is dark mode or light mode, and what the desired
     * contrast level is.
     */
    getHct(scheme: DynamicScheme): Hct;
    /**
     * Return a tone, T in the HCT color space, that this DynamicColor is under
     * the conditions in scheme.
     *
     * @param scheme Defines the conditions of the user interface, for example,
     * whether or not it is dark mode or light mode, and what the desired
     * contrast level is.
     */
    getTone(scheme: DynamicScheme): number;
    /**
     * Given a background tone, find a foreground tone, while ensuring they reach
     * a contrast ratio that is as close to [ratio] as possible.
     *
     * @param bgTone Tone in HCT. Range is 0 to 100, undefined behavior when it
     *     falls outside that range.
     * @param ratio The contrast ratio desired between bgTone and the return
     *     value.
     */
    static foregroundTone(bgTone: number, ratio: number): number;
    /**
     * Returns whether [tone] prefers a light foreground.
     *
     * People prefer white foregrounds on ~T60-70. Observed over time, and also
     * by Andrew Somers during research for APCA.
     *
     * T60 used as to create the smallest discontinuity possible when skipping
     * down to T49 in order to ensure light foregrounds.
     * Since `tertiaryContainer` in dark monochrome scheme requires a tone of
     * 60, it should not be adjusted. Therefore, 60 is excluded here.
     */
    static tonePrefersLightForeground(tone: number): boolean;
    /**
     * Returns whether [tone] can reach a contrast ratio of 4.5 with a lighter
     * color.
     */
    static toneAllowsLightForeground(tone: number): boolean;
    /**
     * Adjust a tone such that white has 4.5 contrast, if the tone is
     * reasonably close to supporting it.
     */
    static enableLightForeground(tone: number): number;
}
export {};
