using MaterialColorUtilities.ColorAppearance;
using MaterialColorUtilities.Utils;

namespace Custom;

public static class Scorer
{
    /**
     * Given a large set of colors, remove colors that are unsuitable for a UI theme, and rank the rest
     * based on suitability.
     *
     * <p>Enables use of a high cluster count for image quantization, thus ensuring colors aren't
     * muddied, while curating the high cluster count to a much smaller number of appropriate choices.
     */
     // Try to get more exotic colors ;)
    private const float CUTOFF_CHROMA = 12f; // was 15f
    private const float CUTOFF_EXCITED_PROPORTION = 0.01f;
    private const float CUTOFF_TONE = 10f;
    private const float TARGET_CHROMA = 48f;
    private const float WEIGHT_PROPORTION = 0.7f;
    private const float WEIGHT_CHROMA_ABOVE = 0.3f;
    private const float WEIGHT_CHROMA_BELOW = 0.1f;

    public const int Default = unchecked((int)0xff4285F4);

    /**
     * Given a map with keys of colors and values of how often the color appears, rank the colors
     * based on suitability for being used for a UI theme.
     *
     * @param colorsToPopulation map with keys of colors and values of how often the color appears,
     *     usually from a source image.
     * @return Colors sorted by suitability for a UI theme. The most suitable color is the first item,
     *     the least suitable is the last. There will always be at least one color returned. If all
     *     the input colors were not suitable for a theme, a default fallback color will be provided,
     *     Google Blue.
     */
    public static List<int> Score(Dictionary<int, int> colorsToPopulation)
    {
        // Determine the total count of all colors.
        float populationSum = 0f;
        foreach (var entry in colorsToPopulation)
        {
            populationSum += entry.Value;
        }

        // Turn the count of each color into a proportion by dividing by the total
        // count. Also, fill a cache of CAM16 colors representing each color, and
        // record the proportion of colors for each CAM16 hue.
        Dictionary<int, Cam16> colorsToCam = new();
        float[] hueProportions = new float[361];
        foreach (var entry in colorsToPopulation)
        {
            int color = entry.Key;
            float population = entry.Value;
            float proportion = population / populationSum;

            Cam16 cam = Cam16.FromInt(color);
            colorsToCam[color] = cam;

            int hue = (int)Math.Round(cam.Hue);
            hueProportions[hue] += proportion;
        }

        // Determine the proportion of the colors around each color, by summing the
        // proportions around each color's hue.
        Dictionary<int, float> colorsToExcitedProportion = new();
        foreach (var entry in colorsToCam)
        {
            int color = entry.Key;
            Cam16 cam = entry.Value;
            int hue = (int)Math.Round(cam.Hue);

            float excitedProportion = 0f;
            for (int j = (hue - 15); j < (hue + 15); j++)
            {
                int neighborHue = MathUtils.SanitizeDegreesInt(j);
                excitedProportion += hueProportions[neighborHue];
            }

            colorsToExcitedProportion[color] = excitedProportion;
        }

        // Score the colors by their proportion, as well as how chromatic they are.
        Dictionary<int, float> colorsToScore = new();
        foreach (var entry in colorsToCam)
        {
            int color = entry.Key;
            Cam16 cam = entry.Value;

            float proportion = colorsToExcitedProportion[color];
            float proportionScore = proportion * 100.0f * WEIGHT_PROPORTION;

            float chromaWeight =
                cam.Chroma < TARGET_CHROMA ? WEIGHT_CHROMA_BELOW : WEIGHT_CHROMA_ABOVE;
            float chromaScore = (cam.Chroma - TARGET_CHROMA) * chromaWeight;

            float score = proportionScore + chromaScore;
            colorsToScore[color] = score;
        }

        // Remove colors that are unsuitable, ex. very dark or unchromatic colors.
        // Also, remove colors that are very similar in hue.
        List<int> filteredColors = Filter(colorsToExcitedProportion, colorsToCam);
        Dictionary<int, float> filteredColorsToScore = new();
        foreach (int color in filteredColors)
        {
            filteredColorsToScore[color] = colorsToScore[color];
        }

        // Ensure the list of colors returned is sorted such that the first in the
        // list is the most suitable, and the last is the least suitable.
        List<KeyValuePair<int, float>> entryList = new(filteredColorsToScore);
        entryList.Sort((a, b) => b.Value.CompareTo(a.Value));
        List<int> colorsByScoreDescending = new();
        foreach (var entry in entryList)
        {
            int color = entry.Key;
            Cam16 cam = colorsToCam[color];
            bool duplicateHue = false;

            foreach (int alreadyChosenColor in colorsByScoreDescending)
            {
                Cam16 alreadyChosenCam = colorsToCam[alreadyChosenColor];
                if (MathUtils.DifferenceDegrees(cam.Hue, alreadyChosenCam.Hue) < 15)
                {
                    duplicateHue = true;
                    break;
                }
            }

            if (duplicateHue)
            {
                continue;
            }
            colorsByScoreDescending.Add(entry.Key);
        }

        // Ensure that at least one color is returned.
        if (!colorsByScoreDescending.Any())
        {
            colorsByScoreDescending.Add(Default);
        }
        return colorsByScoreDescending;
    }

    private static List<int> Filter(
        Dictionary<int, float> colorsToExcitedProportion, Dictionary<int, Cam16> colorsToCam)
    {
        List<int> filtered = new();
        foreach (var entry in colorsToCam)
        {
            int color = entry.Key;
            Cam16 cam = entry.Value;
            float proportion = colorsToExcitedProportion[color];

            if (cam.Chroma >= CUTOFF_CHROMA
                && ColorUtils.LStarFromArgb(color) >= CUTOFF_TONE
                && proportion >= CUTOFF_EXCITED_PROPORTION)
            {
                filtered.Add(color);
            }
        }
        return filtered;
    }
}