from my_first_adventure_game.game.progression import (
    GuideObjective,
    GuideObjectiveState,
)


def test_guide_objective_starts_not_started() -> None:
    objective = GuideObjective()

    assert objective.state is GuideObjectiveState.NOT_STARTED


def test_start_activates_guide_objective() -> None:
    objective = GuideObjective()

    objective.start()

    assert objective.state is GuideObjectiveState.ACTIVE


def test_mark_ready_to_complete_prepares_active_objective() -> None:
    objective = GuideObjective()
    objective.start()

    objective.mark_ready_to_complete()

    assert objective.state is GuideObjectiveState.READY_TO_COMPLETE


def test_complete_finishes_ready_objective() -> None:
    objective = GuideObjective()
    objective.start()
    objective.mark_ready_to_complete()

    objective.complete()

    assert objective.state is GuideObjectiveState.COMPLETED


def test_status_text_describes_current_objective_state() -> None:
    objective = GuideObjective()

    assert objective.status_text == "Objective: Talk to the Guide"

    objective.start()

    assert objective.status_text == "Objective: Collect every item"

    objective.mark_ready_to_complete()

    assert objective.status_text == "Objective: Return to the Guide"

    objective.complete()

    assert objective.status_text == "Objective: Complete"
