from pathlib import Path
from unittest.mock import Mock

import pytest

import my_first_adventure_game.game.profile.profile_store as profile_store
from my_first_adventure_game.game.profile import (
    APP_AUTHOR,
    APP_NAME,
    PROFILE_FILENAME,
    PlayerProfile,
    get_profile_path,
    load_profile,
    save_profile,
)


def test_load_profile_returns_empty_profile_when_file_is_missing(
    tmp_path: Path,
) -> None:
    profile = load_profile(tmp_path / "missing.json")

    assert profile == PlayerProfile()


def test_load_profile_returns_empty_profile_for_invalid_json(
    tmp_path: Path,
) -> None:
    path = tmp_path / "profile.json"
    path.write_text("{invalid json", encoding="utf-8")

    profile = load_profile(path)

    assert profile == PlayerProfile()


def test_save_and_load_profile_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "profile.json"
    profile = PlayerProfile(
        games_started=4,
        games_finished=3,
        victories=2,
        best_score=1400,
        total_score=2900,
        items_collected=8,
        obstacles_destroyed=3,
        enemies_defeated=5,
    )

    save_profile(path, profile)
    loaded_profile = load_profile(path)

    assert loaded_profile == profile


def test_save_profile_propagates_storage_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = tmp_path / "profile.json"

    def fail_save(_path: Path, _data: object) -> None:
        raise OSError("disk full")

    monkeypatch.setattr(
        profile_store,
        "save_json_atomic",
        fail_save,
    )

    with pytest.raises(OSError, match="disk full"):
        save_profile(path, PlayerProfile())


def test_get_profile_path_uses_user_data_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user_data_directory = tmp_path / "user-data"
    resolve_user_data_path = Mock(return_value=user_data_directory)

    monkeypatch.setattr(
        profile_store,
        "user_data_path",
        resolve_user_data_path,
    )

    path = get_profile_path()

    assert path == user_data_directory / PROFILE_FILENAME
    resolve_user_data_path.assert_called_once_with(
        appname=APP_NAME,
        appauthor=APP_AUTHOR,
    )
