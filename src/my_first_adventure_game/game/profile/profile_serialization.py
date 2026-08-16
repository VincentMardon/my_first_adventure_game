from my_first_adventure_game.game.profile.player_profile import PlayerProfile

PROFILE_VERSION = 1


def _read_counter(data: dict[object, object], name: str) -> int:
    value = data.get(name)

    if type(value) is not int or value < 0:
        raise ValueError(f"Invalid profile counter: {name}")

    return value


def profile_to_data(profile: PlayerProfile) -> dict[str, int]:
    """Convert a player profile into versioned JSON-compatible data."""
    return {
        "version": PROFILE_VERSION,
        "games_started": profile.games_started,
        "games_finished": profile.games_finished,
        "victories": profile.victories,
        "best_score": profile.best_score,
        "total_score": profile.total_score,
        "items_collected": profile.items_collected,
        "obstacles_destroyed": profile.obstacles_destroyed,
        "enemies_defeated": profile.enemies_defeated,
    }


def profile_from_data(data: object) -> PlayerProfile:
    """Build a player profile from supported versioned data."""
    if not isinstance(data, dict):
        return PlayerProfile()

    if data.get("version") != PROFILE_VERSION:
        return PlayerProfile()

    try:
        games_started = _read_counter(data, "games_started")
        games_finished = _read_counter(data, "games_finished")
        victories = _read_counter(data, "victories")
        best_score = _read_counter(data, "best_score")
        total_score = _read_counter(data, "total_score")
        items_collected = _read_counter(data, "items_collected")
        obstacles_destroyed = _read_counter(data, "obstacles_destroyed")
        enemies_defeated = _read_counter(data, "enemies_defeated")
    except ValueError:
        return PlayerProfile()

    if games_finished > games_started:
        return PlayerProfile()

    if victories > games_finished:
        return PlayerProfile()

    if best_score > total_score:
        return PlayerProfile()

    return PlayerProfile(
        games_started=games_started,
        games_finished=games_finished,
        victories=victories,
        best_score=best_score,
        total_score=total_score,
        items_collected=items_collected,
        obstacles_destroyed=obstacles_destroyed,
        enemies_defeated=enemies_defeated,
    )
