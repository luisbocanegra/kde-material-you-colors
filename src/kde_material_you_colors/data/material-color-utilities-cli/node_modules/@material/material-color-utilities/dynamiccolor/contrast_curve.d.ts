/**
 * @license
 * Copyright 2023 Google LLC
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
/**
 * A class containing the contrast curve for a dynamic color on its background.
 *
 * The four values correspond to contrast requirements for contrast levels
 * -1.0, 0.0, 0.5, and 1.0, respectively.
 */
export declare class ContrastCurve {
    readonly low: number;
    readonly normal: number;
    readonly medium: number;
    readonly high: number;
    /**
     * Creates a `ContrastCurve` object.
     *
     * @param low Contrast requirement for contrast level -1.0
     * @param normal Contrast requirement for contrast level 0.0
     * @param medium Contrast requirement for contrast level 0.5
     * @param high Contrast requirement for contrast level 1.0
     */
    constructor(low: number, normal: number, medium: number, high: number);
    /**
     * Returns the contrast ratio at a given contrast level.
     *
     * @param contrastLevel The contrast level. 0.0 is the default (normal);
     * -1.0 is the lowest; 1.0 is the highest.
     * @return The contrast ratio, a number between 1.0 and 21.0.
     */
    getContrast(contrastLevel: number): number;
}
