#! python3
"""
Really quick and dirty script to extract availability for one date from the HTML for the
Pitchero availability page.
"""

from collections import namedtuple
import re
import sys

_Player = namedtuple("_Player", "surname firstname availability comment")

_NAME_RE = re.compile(r"<strong>(?P<surname>[^<]*)</strong>,  (?P<firstname>.*)$", re.M)
_AVAIL_RE = re.compile(
    r'/availability/(?P<date>[0-9-]*)".* data-original-title="(?P<availability>[^"]*)"', re.M
)
_COMMENT_RE = re.compile(r"- (?P<comment>.*) By", re.M)
_COMMENT_RE_2 = re.compile(r"- (?P<comment>.*)$", re.M)

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
            commentMatch = _COMMENT_RE.search(AVAIL)
            if commentMatch:
                comment = commentMatch.group("comment")
            else:
                commentMatch = _COMMENT_RE_2.search(AVAIL)
                if commentMatch:
                    comment = commentMatch.group("comment")
                else:
                    comment = None
            if comment is not None:
                comment = comment.rstrip(".")
            AVAIL = kind
            break
    else:
        raise Exception("Unknown: " + AVAIL)
    player = _Player(match.group("surname"), match.group("firstname"), AVAIL, comment)
    players.append(player)

players.sort()

for kind in _AVAIL_TYPES:
    print("\n" + kind + ":")
    for player in players:
        if player.availability == kind:
            comment = player.comment
            if comment is None:
                comment = ""
            else:
                comment = f" ({comment})"
            print("   ", player.firstname, player.surname, comment)
