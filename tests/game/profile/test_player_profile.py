import pytest

from my_first_adventure_game.game.profile import (
    PROFILE_VERSION,
    PlayerProfile,
    profile_from_data,
    profile_to_data,
)
from my_first_adventure_game.game.statistics import SessionStatistics


def test_player_profile_starts_empty() -> None:
    profile = PlayerProfile()

    assert profile.games_started == 0
    assert profile.games_finished == 0
    assert profile.victories == 0
    assert profile.best_score == 0
    assert profile.total_score == 0
    assert profile.items_collected == 0
    assert profile.obstacles_destroyed == 0
    assert profile.enemies_defeated == 0
    assert profile.wall_stains_cleaned == 0


def test_record_game_started_increments_count() -> None:
    profile = PlayerProfile()

    profile.record_game_started()

    assert profile.games_started == 1


def test_record_defeat_accumulates_finished_session() -> None:
    profile = PlayerProfile()
    statistics = SessionStatistics()
    statistics.record_item_collected()
    statistics.record_item_collected()
    statistics.record_obstacle_destroyed()
    statistics.record_enemy_defeated()
    statistics.record_wall_stain_cleaned()
    statistics.record_wall_stain_cleaned()

    profile.record_game_finished(
        score=300,
        statistics=statistics,
        victory=False,
    )

    assert profile.games_finished == 1
    assert profile.victories == 0
    assert profile.best_score == 300
    assert profile.total_score == 300
    assert profile.items_collected == 2
    assert profile.obstacles_destroyed == 1
    assert profile.enemies_defeated == 1
    assert profile.wall_stains_cleaned == 2


def test_record_victory_preserves_highest_score_across_sessions() -> None:
    profile = PlayerProfile()
    first_statistics = SessionStatistics()
    first_statistics.record_item_collected()
    second_statistics = SessionStatistics()
    second_statistics.record_enemy_defeated()

    profile.record_game_finished(
        score=900,
        statistics=first_statistics,
        victory=True,
    )
    profile.record_game_finished(
        score=400,
        statistics=second_statistics,
        victory=False,
    )

    assert profile.games_finished == 2
    assert profile.victories == 1
    assert profile.best_score == 900
    assert profile.total_score == 1300
    assert profile.items_collected == 1
    assert profile.obstacles_destroyed == 0
    assert profile.enemies_defeated == 1


def test_profile_to_data_includes_version_and_statistics() -> None:
    assert PROFILE_VERSION == 2

    profile = PlayerProfile(
        games_started=4,
        games_finished=3,
        victories=2,
        best_score=1400,
        total_score=2900,
        items_collected=8,
        obstacles_destroyed=3,
        enemies_defeated=5,
        wall_stains_cleaned=6,
    )

    data = profile_to_data(profile)

    assert data == {
        "version": PROFILE_VERSION,
        "games_started": 4,
        "games_finished": 3,
        "victories": 2,
        "best_score": 1400,
        "total_score": 2900,
        "items_collected": 8,
        "obstacles_destroyed": 3,
        "enemies_defeated": 5,
        "wall_stains_cleaned": 6,
    }


def test_profile_from_data_restores_profile() -> None:
    data = {
        "version": PROFILE_VERSION,
        "games_started": 4,
        "games_finished": 3,
        "victories": 2,
        "best_score": 1400,
        "total_score": 2900,
        "items_collected": 8,
        "obstacles_destroyed": 3,
        "enemies_defeated": 5,
        "wall_stains_cleaned": 6,
    }

    profile = profile_from_data(data)

    assert profile == PlayerProfile(
        games_started=4,
        games_finished=3,
        victories=2,
        best_score=1400,
        total_score=2900,
        items_collected=8,
        obstacles_destroyed=3,
        enemies_defeated=5,
        wall_stains_cleaned=6,
    )


def test_profile_from_data_returns_empty_profile_for_unsupported_version() -> None:
    data = {
        "version": 999,
        "games_started": 4,
    }

    profile = profile_from_data(data)

    assert profile == PlayerProfile()


@pytest.mark.parametrize(
    "invalid_value",
    (
        "4",
        -1,
        True,
    ),
)
def test_profile_from_data_returns_empty_profile_for_invalid_counter(
    invalid_value: object,
) -> None:
    data = profile_to_data(PlayerProfile())
    data["games_started"] = invalid_value

    profile = profile_from_data(data)

    assert profile == PlayerProfile()


@pytest.mark.parametrize(
    "invalid_counts",
    (
        {
            "games_started": 1,
            "games_finished": 2,
        },
        {
            "games_finished": 1,
            "victories": 2,
        },
        {
            "best_score": 500,
            "total_score": 400,
        },
    ),
)
def test_profile_from_data_returns_empty_profile_for_inconsistent_counts(
    invalid_counts: dict[str, int],
) -> None:
    data = profile_to_data(PlayerProfile())
    data.update(invalid_counts)

    profile = profile_from_data(data)

    assert profile == PlayerProfile()


def test_profile_from_data_migrates_version_one_profile() -> None:
    data = {
        "version": 1,
        "games_started": 4,
        "games_finished": 3,
        "victories": 2,
        "best_score": 1400,
        "total_score": 2900,
        "items_collected": 8,
        "obstacles_destroyed": 3,
        "enemies_defeated": 5,
    }

    profile = profile_from_data(data)

    assert profile == PlayerProfile(
        games_started=4,
        games_finished=3,
        victories=2,
        best_score=1400,
        total_score=2900,
        items_collected=8,
        obstacles_destroyed=3,
        enemies_defeated=5,
        wall_stains_cleaned=0,
    )
