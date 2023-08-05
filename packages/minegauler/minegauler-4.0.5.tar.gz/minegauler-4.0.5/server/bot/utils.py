"""
utils.py - Bot utilities

February 2020, Lewis Gaul
"""

__all__ = (
    "BOT_NAME",
    "NO_TAG_USERS",
    "USER_NAMES",
    "USER_NAMES_FILE",
    "Matchup",
    "PlayerInfo",
    "get_matchups",
    "get_message",
    "get_highscore_times",
    "get_player_info",
    "send_group_message",
    "send_message",
    "send_new_best_message",
    "send_myself_message",
    "set_bot_access_token",
    "set_user_nickname",
    "user_from_email",
)

import collections
import json
import logging
import pathlib
from typing import Iterable, List, Optional, Tuple

import requests
from requests_toolbelt import MultipartEncoder

from minegauler.shared import highscores as hs
from minegauler.shared.types import Difficulty


logger = logging.getLogger(__name__)


USER_NAMES = dict()
USER_NAMES_FILE = pathlib.Path(__file__).parent / "users.json"
NO_TAG_USERS = {"_paula", "_felix", "_kunz", "esinghal"}

BOT_NAME = "minegaulerbot"
_BOT_ACCESS_TOKEN = ""
_BOT_EMAIL = f"{BOT_NAME}@webex.bot"
_WEBEX_GROUP_ROOM_ID = (
    "Y2lzY29zcGFyazovL3VzL1JPT00vNzYyNjI4NTAtMzg3Ni0xMWVhLTlhM2ItODMyNzMyZDlkZTg3"
)


# ------------------------------------------------------------------------------
# External
# ------------------------------------------------------------------------------


def set_bot_access_token(token: str) -> None:
    global _BOT_ACCESS_TOKEN
    _BOT_ACCESS_TOKEN = token


def get_message(msg_id: str) -> str:
    response = requests.get(
        f"https://api.ciscospark.com/v1/messages/{msg_id}",
        headers={"Authorization": f"Bearer {_BOT_ACCESS_TOKEN}"},
    )
    response.raise_for_status()
    return response.json()["text"]


def send_message(
    room_id: str, text: str, *, is_person_id=False, markdown=False
) -> requests.Response:
    logger.debug(
        "Sending message to %s:\n%s", "person" if is_person_id else "room", text
    )
    id_field = "toPersonId" if is_person_id else "roomId"
    text_field = "markdown" if markdown else "text"
    multipart = MultipartEncoder({text_field: text, id_field: room_id})
    response = requests.post(
        "https://api.ciscospark.com/v1/messages",
        data=multipart,
        headers={
            "Authorization": f"Bearer {_BOT_ACCESS_TOKEN}",
            "Content-Type": multipart.content_type,
        },
    )
    response.raise_for_status()
    return response


def send_myself_message(text: str) -> requests.Response:
    return send_message(_get_my_id(), text, is_person_id=True)


def send_group_message(text: str) -> requests.Response:
    return send_message(_WEBEX_GROUP_ROOM_ID, text)


def send_new_best_message(h: hs.HighscoreStruct) -> None:
    """Send a group message when a new personal time record is set."""
    diff = h.difficulty.name.lower()
    drag_select = "on" if h.drag_select else "off"
    send_group_message(
        f"New personal record of {h.elapsed:.2f} set by {h.name} on {diff}!\n"
        f"Settings: drag-select={drag_select}, per-cell={h.per_cell}"
    )


def user_from_email(email: str) -> str:
    return email.split("@", maxsplit=1)[0]


def user_to_email(user: str) -> str:
    return f"{user}@cisco.com"


def tag_user(user: str) -> str:
    if user.strip() and user not in NO_TAG_USERS:
        return f"<@personEmail:{user_to_email(user)}|{user}>"
    else:
        return user


def set_user_nickname(user: str, nickname: str) -> None:
    USER_NAMES[user] = nickname
    with open(USER_NAMES_FILE, "w") as f:
        json.dump(USER_NAMES, f)


def get_highscore_times(
    difficulty: Optional[Difficulty],
    drag_select: Optional[bool] = None,
    per_cell: Optional[int] = None,
    users: Optional[Iterable[str]] = None,
) -> List[Tuple[str, float]]:
    if difficulty is Difficulty.CUSTOM:
        raise ValueError("No highscores for custom difficulty")
    if users is None:
        users = USER_NAMES.values()
    lower_users = {u.lower(): u for u in users}

    if difficulty:
        highscores = hs.filter_and_sort(
            _get_highscores(
                difficulty=difficulty, drag_select=drag_select, per_cell=per_cell,
            )
        )
        times = {
            lower_users[h.name.lower()]: h.elapsed
            for h in highscores
            if h.name.lower() in lower_users
        }
    else:
        times = {
            u: _get_combined_highscore(u, drag_select=drag_select, per_cell=per_cell)
            for u in users
        }

    return sorted(times.items(), key=lambda x: x[1])


Matchup = collections.namedtuple("Matchup", "user1, time1, user2, time2, percent")


def get_matchups(
    times: Iterable[Tuple[str, float]], include_users: Optional[Iterable[str]] = None
) -> List[Matchup]:
    times = sorted(times, key=lambda x: x[1], reverse=True)
    matchups = set()
    while times:
        # Avoid repeating matchups or comparing users against themselves.
        user1, time1 = times.pop()
        for user2, time2 in times:
            if (
                include_users
                and user1 not in include_users
                and user2 not in include_users
            ):
                continue
            assert time2 >= time1
            percent = 100 * (time2 - time1) / time1
            matchups.add(Matchup(user1, time1, user2, time2, percent))

    return sorted(matchups, key=lambda x: x.percent)


PlayerInfo = collections.namedtuple(
    "PlayerInfo", "username, nickname, combined_time, types_played, last_highscore"
)


def get_player_info(username: str) -> PlayerInfo:
    name = USER_NAMES[username]
    highscores = _get_highscores(name=name)
    combined_time = _get_combined_highscore(name)
    last_highscore = max(h.timestamp for h in highscores) if highscores else None
    hs_types = len(
        {(h.difficulty.lower(), h.drag_select, h.per_cell) for h in highscores}
    )
    return PlayerInfo(username, name, combined_time, hs_types, last_highscore)


# ------------------------------------------------------------------------------
# Internal
# ------------------------------------------------------------------------------


def _strbool(b: bool) -> str:
    return "True" if b else "False"


def _get_highscores(*args, **kwargs) -> Iterable[hs.HighscoreStruct]:
    return hs.get_highscores(hs.HighscoresDatabases.REMOTE, *args, **kwargs)


def _get_combined_highscore(
    name: str, *, per_cell: Optional[int] = None, drag_select: Optional[bool] = None
) -> float:
    total = 0
    for diff in ["b", "i", "e"]:
        all_highscores = _get_highscores(
            name=name, drag_select=drag_select, per_cell=per_cell,
        )
        highscores = [h.elapsed for h in all_highscores if h.difficulty.lower() == diff]
        total += min(highscores) if highscores else 1000
    return total


def _get_person_id(name_or_email: str) -> str:
    if "@" in name_or_email:
        params = {"email": name_or_email}
    else:
        params = {"displayName": name_or_email}
    response = requests.get(
        f"https://api.ciscospark.com/v1/people",
        params=params,
        headers={"Authorization": f"Bearer {_BOT_ACCESS_TOKEN}"},
    )
    response.raise_for_status()
    return response.json()["items"][0]["id"]


def _get_my_id() -> str:
    return _get_person_id("Lewis Gaul")


def _get_bot_id() -> str:
    return _get_person_id("Minegauler Bot")
