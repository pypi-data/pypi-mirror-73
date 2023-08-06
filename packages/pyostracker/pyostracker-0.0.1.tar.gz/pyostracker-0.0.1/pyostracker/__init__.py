import os
import json
import logging
import calendar
import datetime
import urllib.parse
import urllib.request


LOGGER = logging.getLogger("pyostracker")
TRACKER_URL = os.environ.get("TRACKER_URL", "https://ostracker.xyz")


def _poll_update(account, handle):
    params = urllib.parse.urlencode({
        "player": account,
        "start": handle["created_at"],
    })
    req = urllib.request.Request(
        f"{TRACKER_URL}/?{params}",
        headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
    )
    expires = datetime.datetime.fromisoformat(handle["expires_at_iso8601"])

    while datetime.datetime.utcnow() < expires:
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.load(resp)
            if data["hiscores"]:
                return data
            time.sleep(0.5)
        except Exception as err:
            LOGGER.debug("tracker error=%s", err)


def _update(account):
    params = urllib.parse.urlencode({
        "player": account,
    })
    req = urllib.request.Request(
        f"{TRACKER_URL}/update?{params}",
        headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.load(resp)


def update(account):
    return _poll_update(account, _update(account))


def scores(account, dt=None):
    params = {
        "player": account,
    }

    if dt is not None:
        start_at = datetime.datetime.utcnow() + dt
        params["start"] = calendar.timegm(start_at.utctimetuple())

    q_str = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        f"{TRACKER_URL}/?{q_str}",
        headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.load(resp)
