import os
import json
import time
import logging
import calendar
import datetime
import urllib.parse
import urllib.error
import urllib.request


LOGGER = logging.getLogger("ostracker")
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
    expires = datetime.datetime.utcfromtimestamp(handle["expires_at"])

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
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        if err.code != 409:
            raise
        # Conflicts with a pending update -> use that as a handle
        return json.load(err)


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
