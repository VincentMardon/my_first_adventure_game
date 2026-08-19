from dataclasses import FrozenInstanceError

import pygame
import pytest

from my_first_adventure_game.game.entities import WallStain


def test_wall_stain_describes_dirty_wall_surface() -> None:
    stain = WallStain(
        wall_id="clearing-wall-top",
        contact_position=(640.0, 96.0),
        surface_normal=(0.0, 1.0),
    )

    assert stain.wall_id == "clearing-wall-top"
    assert stain.contact_position == (640.0, 96.0)
    assert stain.surface_normal == (0.0, 1.0)


def test_wall_stain_is_immutable() -> None:
    stain = WallStain(
        wall_id="clearing-wall-top",
        contact_position=(640.0, 96.0),
        surface_normal=(0.0, 1.0),
    )

    with pytest.raises(FrozenInstanceError):
        stain.contact_position = (700.0, 96.0)


@pytest.mark.parametrize(
    ("surface_normal", "expected_position"),
    [
        ((-1.0, 0.0), (106.0, 188.0)),
        ((1.0, 0.0), (130.0, 188.0)),
        ((0.0, -1.0), (118.0, 176.0)),
        ((0.0, 1.0), (118.0, 200.0)),
    ],
)
def test_wall_stain_calculates_approach_position(
    surface_normal: tuple[float, float],
    expected_position: tuple[float, float],
) -> None:
    stain = WallStain(
        wall_id="wall",
        contact_position=(130.0, 200.0),
        surface_normal=surface_normal,
    )

    position = stain.approach_position(pygame.Vector2(24.0, 24.0))

    assert position == pygame.Vector2(expected_position)
