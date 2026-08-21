import pygame

from my_first_adventure_game.engine.world import Entity
from my_first_adventure_game.game.entities import (
    CARETAKER_SIDESTEP_TARGET_ID,
    NPC,
    CaretakerBehavior,
    CaretakerPhase,
    Player,
    WallStain,
)


def _create_caretaker() -> NPC:
    return NPC(
        name="Caretaker",
        entity=Entity(
            entity_id="npc-clearing-caretaker",
            position=pygame.Vector2(560.0, 96.0),
            size=pygame.Vector2(24.0, 32.0),
        ),
        dialogue_lines=("I have work to do.",),
        movement_speed=80.0,
    )


def _create_player(position: tuple[float, float]) -> Player:
    return Player(
        entity=Entity(
            entity_id="player",
            position=pygame.Vector2(position),
            size=pygame.Vector2(24.0, 24.0),
        ),
        health=3,
    )


def _create_stain() -> WallStain:
    return WallStain(
        wall_id="clearing-wall-top",
        contact_position=(640.0, 96.0),
        surface_normal=(0.0, 1.0),
    )


def test_update_targets_stain_approach_when_position_is_free() -> None:
    caretaker = _create_caretaker()
    player = _create_player((700.0, 200.0))
    behavior = CaretakerBehavior(caretaker, player)

    behavior.return_to_stain(_create_stain())
    behavior.update_target()

    assert behavior.phase is CaretakerPhase.RETURNING_TO_STAIN
    assert caretaker.movement_target == pygame.Vector2(628.0, 96.0)
    assert caretaker.movement_target_id == "clearing-wall-top"
    assert caretaker.movement_target_entity is None


def test_update_targets_nearest_side_when_player_blocks_stain() -> None:
    caretaker = _create_caretaker()
    player = _create_player((628.0, 96.0))
    behavior = CaretakerBehavior(caretaker, player)

    behavior.return_to_stain(_create_stain())
    behavior.update_target()

    assert behavior.phase is CaretakerPhase.SIDESTEPPING
    assert caretaker.movement_target == pygame.Vector2(604.0, 96.0)
    assert caretaker.movement_target_id == CARETAKER_SIDESTEP_TARGET_ID
    assert caretaker.movement_target_entity is None


def test_update_returns_to_stain_when_player_moves_away() -> None:
    caretaker = _create_caretaker()
    player = _create_player((628.0, 96.0))
    behavior = CaretakerBehavior(caretaker, player)

    behavior.return_to_stain(_create_stain())
    behavior.update_target()

    assert behavior.phase is CaretakerPhase.SIDESTEPPING
    assert caretaker.movement_target_id == CARETAKER_SIDESTEP_TARGET_ID

    player.entity.position.update(700.0, 200.0)

    behavior.update_target()

    assert behavior.phase is CaretakerPhase.RETURNING_TO_STAIN
    assert caretaker.movement_target == pygame.Vector2(628.0, 96.0)
    assert caretaker.movement_target_id == "clearing-wall-top"


def test_complete_task_clears_state_and_movement_target() -> None:
    caretaker = _create_caretaker()
    player = _create_player((700.0, 200.0))
    behavior = CaretakerBehavior(caretaker, player)

    behavior.return_to_stain(_create_stain())
    behavior.update_target()

    behavior.complete_task()

    assert behavior.phase is CaretakerPhase.IDLE
    assert caretaker.movement_target is None
    assert caretaker.movement_target_id is None
    assert caretaker.movement_target_entity is None

    behavior.update_target()

    assert caretaker.movement_target is None
    assert caretaker.movement_target_id is None
