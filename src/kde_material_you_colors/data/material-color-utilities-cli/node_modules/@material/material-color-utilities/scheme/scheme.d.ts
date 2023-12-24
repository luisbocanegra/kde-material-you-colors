/**
 * @license
 * Copyright 2021 Google LLC
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
import { CorePalette } from '../palettes/core_palette.js';
/**
 * Represents a Material color scheme, a mapping of color roles to colors.
 */
export declare class Scheme {
    private readonly props;
    get primary(): number;
    get onPrimary(): number;
    get primaryContainer(): number;
    get onPrimaryContainer(): number;
    get secondary(): number;
    get onSecondary(): number;
    get secondaryContainer(): number;
    get onSecondaryContainer(): number;
    get tertiary(): number;
    get onTertiary(): number;
    get tertiaryContainer(): number;
    get onTertiaryContainer(): number;
    get error(): number;
    get onError(): number;
    get errorContainer(): number;
    get onErrorContainer(): number;
    get background(): number;
    get onBackground(): number;
    get surface(): number;
    get onSurface(): number;
    get surfaceVariant(): number;
    get onSurfaceVariant(): number;
    get outline(): number;
    get outlineVariant(): number;
    get shadow(): number;
    get scrim(): number;
    get inverseSurface(): number;
    get inverseOnSurface(): number;
    get inversePrimary(): number;
    /**
     * @param argb ARGB representation of a color.
     * @return Light Material color scheme, based on the color's hue.
     */
    static light(argb: number): Scheme;
    /**
     * @param argb ARGB representation of a color.
     * @return Dark Material color scheme, based on the color's hue.
     */
    static dark(argb: number): Scheme;
    /**
     * @param argb ARGB representation of a color.
     * @return Light Material content color scheme, based on the color's hue.
     */
    static lightContent(argb: number): Scheme;
    /**
     * @param argb ARGB representation of a color.
     * @return Dark Material content color scheme, based on the color's hue.
     */
    static darkContent(argb: number): Scheme;
    /**
     * Light scheme from core palette
     */
    static lightFromCorePalette(core: CorePalette): Scheme;
    /**
     * Dark scheme from core palette
     */
    static darkFromCorePalette(core: CorePalette): Scheme;
    private constructor();
    toJSON(): {
        primary: number;
        onPrimary: number;
        primaryContainer: number;
        onPrimaryContainer: number;
        secondary: number;
        onSecondary: number;
        secondaryContainer: number;
        onSecondaryContainer: number;
        tertiary: number;
        onTertiary: number;
        tertiaryContainer: number;
        onTertiaryContainer: number;
        error: number;
        onError: number;
        errorContainer: number;
        onErrorContainer: number;
        background: number;
        onBackground: number;
        surface: number;
        onSurface: number;
        surfaceVariant: number;
        onSurfaceVariant: number;
        outline: number;
        outlineVariant: number;
        shadow: number;
        scrim: number;
        inverseSurface: number;
        inverseOnSurface: number;
        inversePrimary: number;
    };
}
