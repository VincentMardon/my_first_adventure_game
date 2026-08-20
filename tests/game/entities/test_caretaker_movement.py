import pygame
import pytest

from my_first_adventure_game.engine.collisions import AABB
from my_first_adventure_game.game.entities import (
    WallStain,
    caretaker_sidestep_target,
)


@pytest.mark.parametrize(
    (
        "contact_position",
        "surface_normal",
        "caretaker_position",
        "player_position",
        "expected_target",
    ),
    [
        (
            (640.0, 96.0),
            (0.0, 1.0),
            (560.0, 96.0),
            (628.0, 96.0),
            (604.0, 96.0),
        ),
        (
            (640.0, 96.0),
            (0.0, 1.0),
            (700.0, 96.0),
            (628.0, 96.0),
            (652.0, 96.0),
        ),
        (
            (130.0, 192.0),
            (1.0, 0.0),
            (130.0, 120.0),
            (130.0, 180.0),
            (130.0, 148.0),
        ),
        (
            (130.0, 192.0),
            (1.0, 0.0),
            (130.0, 260.0),
            (130.0, 180.0),
            (130.0, 204.0),
        ),
    ],
)
def testcaretaker_sidestep_target_chooses_nearet_player_side(
    contact_position: tuple[float, float],
    surface_normal: tuple[float, float],
    caretaker_position: tuple[float, float],
    player_position: tuple[float, float],
    expected_target: tuple[float, float],
) -> None:
    stain = WallStain(
        wall_id="wall",
        contact_position=contact_position,
        surface_normal=surface_normal,
    )
    caretaker_bounds = AABB(
        x=caretaker_position[0],
        y=caretaker_position[1],
        width=24.0,
        height=32.0,
    )
    player_bounds = AABB(
        x=player_position[0],
        y=player_position[1],
        width=24.0,
        height=24.0,
    )

    target = caretaker_sidestep_target(
        stain,
        caretaker_bounds,
        player_bounds,
    )

    assert target == pygame.Vector2(expected_target)


def test_caretaker_sidestep_target_uses_current_player_position() -> None:
    stain = WallStain(
        wall_id="wall",
        contact_position=(640.0, 96.0),
        surface_normal=(0.0, 1.0),
    )
    caretaker_bounds = AABB(
        x=560.0,
        y=96.0,
        width=24.0,
        height=32.0,
    )
    initial_player_bounds = AABB(
        x=628.0,
        y=96.0,
        width=24.0,
        height=24.0,
    )
    moved_player_bounds = AABB(
        x=680.0,
        y=96.0,
        width=24.0,
        height=24.0,
    )

    initial_target = caretaker_sidestep_target(
        stain,
        caretaker_bounds,
        initial_player_bounds,
    )
    recalculated_target = caretaker_sidestep_target(
        stain,
        caretaker_bounds,
        moved_player_bounds,
    )

    assert initial_target == pygame.Vector2(604.0, 96.0)
    assert recalculated_target == pygame.Vector2(656.0, 96.0)
