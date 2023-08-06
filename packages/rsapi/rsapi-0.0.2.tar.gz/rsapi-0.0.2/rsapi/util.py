import csv
import time
import math
import urllib.parse

import requests

from rsapi import API_URL, LOGGER, DEFAULT_RETRIES, DEFAULT_TIMEOUT


def request(path, _retries=DEFAULT_RETRIES, _timeout=DEFAULT_TIMEOUT, **query):
    q_str = urllib.parse.urlencode(query)
    url = f"{API_URL}/{path}?{q_str}"

    for i in range(1, _retries+1):
        started_at = time.monotonic()
        try:
            resp = requests.get(url, timeout=_timeout)
        except requests.exceptions.Timeout:
            resp = None
        ended_at = time.monotonic()
        delta = math.floor(ended_at - started_at)

        if delta > _timeout:
            LOGGER.debug("request took more than expected - %ds", delta)
            delta = _timeout

        # Rs site redirects to /unavailable with success codes on failure
        if (resp is not None and \
            resp.url == url and \
            resp.status_code == requests.codes["ok"]):
            return resp

        # Each iteration, backoff timer grows by 3**i, but at max req roof - time taken
        time.sleep(min(3**i, _timeout-delta))
    raise Exception("hiscore request timed out")


def parse_scores(text, skills):
    scores = {}

    for idx, row in enumerate(csv.reader(text.splitlines())):
        if not 2 <= len(row) <= 3:
            LOGGER.warning("bad row in hiscores row=%s", row)
            continue

        try:
            rank = int(row[0])
            level = int(row[1])
        except (TypeError, ValueError):
            LOGGER.warning("bad row in hiscores row=%s", row)
            continue

        # Acitivities don't have exp
        try:
            exp = int(row[2])
        except (TypeError, ValueError, IndexError):
            exp = None

        try:
            skill = skills[idx]
        except IndexError:
            LOGGER.debug("ignoring skill idx=%d", idx)
            continue

        if not isinstance(skill, str):
            skill = skill[0]

        scores[skill] = {
            "rank": rank,
            "level": level,
            "exp": exp,
        }

    return scores


