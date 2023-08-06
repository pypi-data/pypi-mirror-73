import logging


DEFAULT_TIMEOUT = 60  #  timeout for a single request
DEFAULT_RETRIES = 3

API_URL = "https://secure.runescape.com"
LOGGER = logging.getLogger("rsapi")


def diff_scores(baseline, scores):
    deltas = {}

    for skill_name, score in scores.items():
        delta = {}
        other = baseline.get(skill_name)
        if other:
            for attr in "exp", "rank", "level":
                a = other[attr]
                b = score[attr]

                # Should assert a is None too?
                if b is None:
                    continue

                # No change
                if a == b:
                    continue

                # Baseline is unranked?
                if a == -1:
                    delta[attr] = b
                else:
                    delta[attr] = b - a
        else:
            delta = {
                "rank": 0,
                "level": 0,
                "exp": 0,
            }

        if delta:
            deltas[skill_name] = delta

    return deltas
