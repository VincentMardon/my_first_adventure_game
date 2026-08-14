from my_first_adventure_game.game.scoring import (
    guide_objective_completion_points,
)


def test_guide_objective_completion_awards_five_hundred_points() -> None:
    assert guide_objective_completion_points() == 500
