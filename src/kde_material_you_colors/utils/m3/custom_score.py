from materialyoucolor.hct import Hct
from materialyoucolor.utils.math_utils import sanitize_degrees_int, difference_degrees
from materialyoucolor.dislike.dislike_analyzer import DislikeAnalyzer
from materialyoucolor.score.score import ScoreOptions
from materialyoucolor.score.score import SCORE_OPTION_DEFAULTS


class Score:
    TARGET_CHROMA = 48.0
    WEIGHT_PROPORTION = 0.7
    WEIGHT_CHROMA_ABOVE = 0.3
    WEIGHT_CHROMA_BELOW = 0.1
    CUTOFF_CHROMA = 5.0
    CUTOFF_EXCITED_PROPORTION = 0.01
    CUTOFF_TONE = 0.0

    def __init__(self):
        pass

    @staticmethod
    def score(colors_to_population: dict, options: ScoreOptions = None) -> list[int]:
        if options is None:
            options = SCORE_OPTION_DEFAULTS

        desired = options.desired
        fallback_color_argb = options.fallback_color_argb
        filter_enabled = options.filter
        dislike_filter = options.dislike_filter

        colors_hct = []
        hue_population = [0] * 360
        population_sum = 0

        for rgb, population in colors_to_population.items():
            hct = Hct.from_int(rgb)
            colors_hct.append(hct)
            hue = int(hct.hue)
            hue_population[hue] += population
            population_sum += population

        hue_excited_proportions = [0.0] * 360

        for hue in range(360):
            proportion = hue_population[hue] / population_sum
            for i in range(hue - 14, hue + 16):
                neighbor_hue = int(sanitize_degrees_int(i))
                hue_excited_proportions[neighbor_hue] += proportion

        scored_hct = []
        for hct in colors_hct:
            hue = int(sanitize_degrees_int(round(hct.hue)))
            proportion = hue_excited_proportions[hue]

            if filter_enabled and (
                hct.chroma < Score.CUTOFF_CHROMA
                or proportion <= Score.CUTOFF_EXCITED_PROPORTION
                or hct.tone < Score.CUTOFF_TONE
            ):
                continue

            proportion_score = proportion * 100.0 * Score.WEIGHT_PROPORTION
            chroma_weight = (
                Score.WEIGHT_CHROMA_BELOW
                if hct.chroma < Score.TARGET_CHROMA
                else Score.WEIGHT_CHROMA_ABOVE
            )
            chroma_score = (hct.chroma - Score.TARGET_CHROMA) * chroma_weight
            score = proportion_score + chroma_score
            scored_hct.append({"hct": hct, "score": score})

        scored_hct.sort(
            key=lambda x: -1 if x["score"] > 0 else (1 if x["score"] < 0 else 0)
        )

        chosen_colors = []
        for difference_degrees_ in range(90, 14, -1):
            chosen_colors.clear()
            for hct in [item["hct"] for item in scored_hct]:
                duplicate_hue = any(
                    difference_degrees(hct.hue, chosen_hct.hue) < difference_degrees_
                    for chosen_hct in chosen_colors
                )
                if not duplicate_hue:
                    chosen_colors.append(hct)
                if len(chosen_colors) >= desired:
                    break
            if len(chosen_colors) >= desired:
                break

        colors = []
        if not chosen_colors:
            colors.append(fallback_color_argb)

        if dislike_filter:
            for chosen_hct in chosen_colors:
                chosen_colors[chosen_colors.index(chosen_hct)] = (
                    DislikeAnalyzer.fix_if_disliked(chosen_hct)
                )
        for chosen_hct in chosen_colors:
            colors.append(chosen_hct.to_int())
        return colors
