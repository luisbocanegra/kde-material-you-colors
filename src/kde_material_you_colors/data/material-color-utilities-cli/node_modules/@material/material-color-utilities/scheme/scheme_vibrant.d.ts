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
import { DynamicScheme } from './dynamic_scheme.js';
/**
 * A Dynamic Color theme that maxes out colorfulness at each position in the
 * Primary Tonal Palette.
 */
export declare class SchemeVibrant extends DynamicScheme {
    /**
     * Hues (in degrees) used at breakpoints such that designers can specify a
     * hue rotation that occurs at a given break point.
     */
    private static readonly hues;
    /**
     * Hue rotations (in degrees) of the Secondary [TonalPalette],
     * corresponding to the breakpoints in [hues].
     */
    private static readonly secondaryRotations;
    /**
     * Hue rotations (in degrees) of the Tertiary [TonalPalette],
     * corresponding to the breakpoints in [hues].
     */
    private static readonly tertiaryRotations;
    constructor(sourceColorHct: Hct, isDark: boolean, contrastLevel: number);
}
