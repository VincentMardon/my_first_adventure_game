from my_first_adventure_game.game.progression import (
    GuideObjective,
    GuideObjectiveState,
)


def test_guide_objective_starts_not_started() -> None:
    objective = GuideObjective(total_items=2)

    assert objective.state is GuideObjectiveState.NOT_STARTED


def test_start_activates_guide_objective() -> None:
    objective = GuideObjective(total_items=2)

    objective.start()

    assert objective.state is GuideObjectiveState.ACTIVE


def test_mark_ready_to_complete_prepares_active_objective() -> None:
    objective = GuideObjective(total_items=2)
    objective.start()

    objective.mark_ready_to_complete()

    assert objective.state is GuideObjectiveState.READY_TO_COMPLETE


def test_complete_finishes_ready_objective() -> None:
    objective = GuideObjective(total_items=2)
    objective.start()
    objective.mark_ready_to_complete()

    objective.complete()

    assert objective.state is GuideObjectiveState.COMPLETED


def test_status_text_describes_current_objective_state() -> None:
    objective = GuideObjective(total_items=2)

    assert objective.status_text == "Objective: Talk to the Guide"

    objective.start()

    assert objective.status_text == "Objective: Collect items (0/2)"

    objective.mark_ready_to_complete()

    assert objective.status_text == "Objective: Return to the Guide"

    objective.complete()

    assert objective.status_text == "Objective: Complete"


def test_guide_objective_starts_with_no_collected_items() -> None:
    objective = GuideObjective(total_items=2)

    assert objective.total_items == 2
    assert objective.collected_items == 0


def test_record_item_collected_advances_active_objective_progress() -> None:
    objective = GuideObjective(total_items=2)
    objective.start()

    objective.record_item_collected()

    assert objective.collected_items == 1
    assert objective.state is GuideObjectiveState.ACTIVE


def test_record_final_item_marks_objective_ready_to_complete() -> None:
    objective = GuideObjective(total_items=2)
    objective.start()
    objective.record_item_collected()

    objective.record_item_collected()

    assert objective.collected_items == 2
    assert objective.state is GuideObjectiveState.READY_TO_COMPLETE


def test_active_status_text_reports_collected_item_count() -> None:
    objective = GuideObjective(total_items=2)
    objective.start()
    objective.record_item_collected()

    assert objective.status_text == "Objective: Collect items (1/2)"
