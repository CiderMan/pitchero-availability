#! python3
"""
Really quick and dirty script to extract availability for one date from the HTML for the
Pitchero availability page.
"""

from collections import namedtuple
import re
import sys

_Player = namedtuple("_Player", "surname firstname availability")

_NAME_RE = re.compile(r"<strong>(?P<surname>[^<]*)</strong>,  (?P<firstname>.*)$", re.M)
_AVAIL_RE = re.compile(
    r'/availability/(?P<date>[0-9-]*)".* data-original-title="(?P<availability>[^"]*)"', re.M
)

_AVAIL_TYPES = ("Available", "Not sure", "Unavailable", "Not set")

with open(sys.argv[1], encoding="utf8") as players:
    html = players.read()

DATE = None
players = []

for match in _NAME_RE.finditer(html):
    availMatch = _AVAIL_RE.search(html, match.end())
    assert availMatch
    if DATE is None:
        DATE = availMatch.group("date")
        print("Showing availability for", DATE + ":")
    assert availMatch.group("date") == DATE
    AVAIL = availMatch.group("availability")
    for kind in _AVAIL_TYPES:
        if AVAIL.startswith(kind):
            AVAIL = kind
            break
    else:
        raise Exception("Unknown: " + AVAIL)
    player = _Player(match.group("surname"), match.group("firstname"), AVAIL)
    players.append(player)

players.sort()

for kind in _AVAIL_TYPES:
    print("\n" + kind + ":")
    for player in players:
        if player.availability == kind:
            print("   ", player.firstname, player.surname)
