from my_first_adventure_game.game.statistics import SessionStatistics


def test_statistics_start_at_zero() -> None:
    statistics = SessionStatistics()

    assert statistics.items_collected == 0
    assert statistics.obstacles_destroyed == 0
    assert statistics.enemies_defeated == 0
    assert statistics.wall_stains_cleaned == 0


def test_record_item_collected_increments_count() -> None:
    statistics = SessionStatistics()

    statistics.record_item_collected()

    assert statistics.items_collected == 1


def test_record_obstacle_destroyed_increments_count() -> None:
    statistics = SessionStatistics()

    statistics.record_obstacle_destroyed()

    assert statistics.obstacles_destroyed == 1


def test_record_enemy_defeated_increments_count() -> None:
    statistics = SessionStatistics()

    statistics.record_enemy_defeated()

    assert statistics.enemies_defeated == 1


def test_record_wall_stain_cleaned_increments_count() -> None:
    statistics = SessionStatistics()

    statistics.record_wall_stain_cleaned()

    assert statistics.wall_stains_cleaned == 1
