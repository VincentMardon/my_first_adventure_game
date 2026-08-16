import json
from pathlib import Path

from platformdirs import user_data_path

from my_first_adventure_game.engine.persistence import (
    load_json,
    save_json_atomic,
)
from my_first_adventure_game.game.profile.player_profile import PlayerProfile
from my_first_adventure_game.game.profile.profile_serialization import (
    profile_from_data,
    profile_to_data,
)

APP_AUTHOR = "Vincent Mardon"
APP_NAME = "My First Adventure Game"
PROFILE_FILENAME = "profile.json"


def load_profile(path: Path) -> PlayerProfile:
    """Load a profile or return an empty profile when data cannot be read."""
    try:
        data = load_json(path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return PlayerProfile()

    return profile_from_data(data)


def save_profile(path: Path, profile: PlayerProfile) -> None:
    """Save a player profile atomically."""
    save_json_atomic(path, profile_to_data(profile))


def get_profile_path() -> Path:
    """Return the platform-specific path of the player profile."""
    return (
        user_data_path(
            appname=APP_NAME,
            appauthor=APP_AUTHOR,
        )
        / PROFILE_FILENAME
    )
