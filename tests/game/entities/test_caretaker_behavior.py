import pygame

from my_first_adventure_game.engine.collisions import AABB
from my_first_adventure_game.engine.world import Entity
from my_first_adventure_game.game.entities import (
    CARETAKER_ROUNDING_TARGET_ID,
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


def test_update_targets_nearest_outer_corner_when_player_blocks_stain() -> None:
    caretaker = _create_caretaker()
    caretaker.entity.position.update(628.0, 120.0)
    player = _create_player((628.0, 96.0))
    behavior = CaretakerBehavior(caretaker, player)

    behavior.return_to_stain(_create_stain())
    behavior.update_target()

    assert behavior.phase is CaretakerPhase.ROUNDING_PLAYER
    assert caretaker.movement_target == pygame.Vector2(604.0, 120.0)
    assert caretaker.movement_target_id == CARETAKER_ROUNDING_TARGET_ID
    assert caretaker.movement_target_entity is None


def test_update_keeps_chosen_side_while_rounding_player() -> None:
    caretaker = _create_caretaker()
    caretaker.entity.position.update(628.0, 120.0)
    player = _create_player((628.0, 96.0))
    behavior = CaretakerBehavior(caretaker, player)

    behavior.return_to_stain(_create_stain())
    behavior.update_target()

    assert caretaker.movement_target == pygame.Vector2(604.0, 120.0)

    caretaker.entity.position.update(640.0, 110.0)

    behavior.update_target()

    assert behavior.phase is CaretakerPhase.ROUNDING_PLAYER
    assert caretaker.movement_target == pygame.Vector2(604.0, 120.0)
    assert caretaker.movement_target_id == CARETAKER_ROUNDING_TARGET_ID


def test_update_returns_to_stain_when_player_moves_away() -> None:
    caretaker = _create_caretaker()
    caretaker.entity.position.update(628.0, 120.0)
    player = _create_player((628.0, 96.0))
    behavior = CaretakerBehavior(caretaker, player)

    behavior.return_to_stain(_create_stain())
    behavior.update_target()

    assert behavior.phase is CaretakerPhase.ROUNDING_PLAYER
    assert caretaker.movement_target_id == CARETAKER_ROUNDING_TARGET_ID

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


def test_align_with_player_targets_side_against_walls() -> None:
    caretaker = _create_caretaker()
    caretaker.entity.position.update(628.0, 120.0)
    player = _create_player((628.0, 96.0))
    behavior = CaretakerBehavior(caretaker, player)

    behavior.return_to_stain(_create_stain())
    behavior.update_target()

    caretaker.entity.position.update(caretaker.movement_target)

    behavior.align_with_player()

    assert behavior.phase is CaretakerPhase.SIDESTEPPING
    assert caretaker.movement_target == pygame.Vector2(604.0, 96.0)
    assert caretaker.movement_target_id == CARETAKER_SIDESTEP_TARGET_ID
    assert caretaker.movement_target_entity is None


def test_start_pushing_clears_sidestep_target_without_moving_player() -> None:
    caretaker = _create_caretaker()
    caretaker.entity.position.update(604.0, 96.0)
    player = _create_player((628.0, 96.0))
    behavior = CaretakerBehavior(caretaker, player)

    behavior.return_to_stain(_create_stain())
    behavior.update_target()

    caretaker.entity.position.update(caretaker.movement_target)
    behavior.align_with_player()

    caretaker.entity.position.update(caretaker.movement_target)

    player_position = player.entity.position.copy()

    behavior.start_pushing()

    assert behavior.phase is CaretakerPhase.PUSHING_PLAYER
    assert player.entity.position == player_position
    assert caretaker.movement_target is None
    assert caretaker.movement_target_id is None
    assert caretaker.movement_target_entity is None


def test_push_player_moves_both_entities_incrementally() -> None:
    caretaker = _create_caretaker()
    caretaker.entity.position.update(604.0, 96.0)
    player = _create_player((628.0, 96.0))
    behavior = CaretakerBehavior(caretaker, player)

    behavior.return_to_stain(_create_stain())
    behavior.update_target()
    behavior.start_pushing()

    applied_movement = behavior.push_player(0.1, ())

    assert applied_movement == pygame.Vector2(8.0, 0.0)
    assert player.entity.position == pygame.Vector2(636.0, 96.0)
    assert caretaker.entity.position == pygame.Vector2(612.0, 96.0)


def test_push_player_stops_at_solid_bounds() -> None:
    caretaker = _create_caretaker()
    caretaker.entity.position.update(604.0, 96.0)
    player = _create_player((628.0, 96.0))
    behavior = CaretakerBehavior(caretaker, player)
    blocking_wall = AABB(
        x=660.0,
        y=96.0,
        width=32.0,
        height=32.0,
    )

    behavior.return_to_stain(_create_stain())
    behavior.update_target()
    behavior.start_pushing()

    applied_movement = behavior.push_player(0.2, (blocking_wall,))

    assert applied_movement == pygame.Vector2(8.0, 0.0)
    assert player.entity.position == pygame.Vector2(636.0, 96.0)
    assert caretaker.entity.position == pygame.Vector2(612.0, 96.0)
    assert behavior.phase is CaretakerPhase.PUSHING_PLAYER


def test_update_advances_active_push() -> None:
    caretaker = _create_caretaker()
    caretaker.entity.position.update(604.0, 96.0)
    player = _create_player((628.0, 96.0))
    behavior = CaretakerBehavior(caretaker, player)

    behavior.return_to_stain(_create_stain())
    behavior.update_target()
    behavior.start_pushing()

    behavior.update(0.1, ())

    assert behavior.phase is CaretakerPhase.PUSHING_PLAYER
    assert player.entity.position == pygame.Vector2(636.0, 96.0)
    assert caretaker.entity.position == pygame.Vector2(612.0, 96.0)


def test_update_returns_to_stain_after_player_clears_approach() -> None:
    caretaker = _create_caretaker()
    caretaker.entity.position.update(604.0, 96.0)
    player = _create_player((628.0, 96.0))
    behavior = CaretakerBehavior(caretaker, player)

    behavior.return_to_stain(_create_stain())
    behavior.update_target()
    behavior.start_pushing()

    behavior.update(0.3, ())

    assert player.entity.position == pygame.Vector2(652.0, 96.0)
    assert caretaker.entity.position == pygame.Vector2(628.0, 96.0)
    assert behavior.phase is CaretakerPhase.RETURNING_TO_STAIN
    assert caretaker.movement_target == pygame.Vector2(628.0, 96.0)
    assert caretaker.movement_target_id == "clearing-wall-top"
    assert caretaker.movement_target_entity is None


def test_update_skips_rounding_when_caretaker_is_already_on_player_side() -> None:
    caretaker = _create_caretaker()
    caretaker.entity.position.update(590.0, 108.0)
    player = _create_player((628.0, 96.0))
    behavior = CaretakerBehavior(caretaker, player)

    behavior.return_to_stain(_create_stain())
    behavior.update_target()

    assert behavior.phase is CaretakerPhase.SIDESTEPPING
    assert caretaker.movement_target == pygame.Vector2(604.0, 96.0)
    assert caretaker.movement_target_id == CARETAKER_SIDESTEP_TARGET_ID
    assert caretaker.movement_target_entity is None


def test_update_selects_new_side_after_player_reblocks_stain() -> None:
    caretaker = _create_caretaker()
    caretaker.entity.position.update(628.0, 120.0)
    player = _create_player((628.0, 96.0))
    behavior = CaretakerBehavior(caretaker, player)

    behavior.return_to_stain(_create_stain())
    behavior.update_target()

    assert caretaker.movement_target == pygame.Vector2(604.0, 120.0)

    player.entity.position.update(700.0, 200.0)
    behavior.update_target()

    caretaker.entity.position.update(652.0, 96.0)
    player.entity.position.update(628.0, 96.0)
    behavior.update_target()

    assert behavior.phase is CaretakerPhase.SIDESTEPPING
    assert caretaker.movement_target == pygame.Vector2(652.0, 96.0)
    assert caretaker.movement_target_id == CARETAKER_SIDESTEP_TARGET_ID
