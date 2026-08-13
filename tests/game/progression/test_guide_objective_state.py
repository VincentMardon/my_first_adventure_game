from my_first_adventure_game.game.progression import GuideObjectiveState


def test_guide_objective_states_follow_expected_order() -> None:
    assert tuple(GuideObjectiveState) == (
        GuideObjectiveState.NOT_STARTED,
        GuideObjectiveState.ACTIVE,
        GuideObjectiveState.READY_TO_COMPLETE,
        GuideObjectiveState.COMPLETED,
    )
