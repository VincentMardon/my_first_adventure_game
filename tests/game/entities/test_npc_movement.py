import pygame
import pytest

from my_first_adventure_game.engine.collisions import AABB
from my_first_adventure_game.engine.world import Entity
from my_first_adventure_game.game.entities import NPC, move_npc_towards


def make_npc(
    *,
    position: tuple[float, float] = (0.0, 0.0),
) -> NPC:
    return NPC(
        name="Caretaker",
        entity=Entity(
            entity_id="caretaker",
            position=pygame.Vector2(position),
            size=pygame.Vector2(10.0, 10.0),
        ),
        dialogue_lines=("These floors will not clean themselves.",),
    )


def test_move_npc_towards_applies_speed_over_elapsed_time() -> None:
    npc = make_npc()

    movement = move_npc_towards(
        npc,
        target=pygame.Vector2(30.0, 40.0),
        speed=20.0,
        delta_time=0.1,
        solid_bounds=(),
    )

    assert movement.x == pytest.approx(1.2)
    assert movement.y == pytest.approx(1.6)
    assert npc.entity.position.x == pytest.approx(1.2)
    assert npc.entity.position.y == pytest.approx(1.6)


def test_move_npc_towards_stops_at_target() -> None:
    npc = make_npc()

    movement = move_npc_towards(
        npc,
        target=pygame.Vector2(1.0, 1.0),
        speed=20.0,
        delta_time=1.0,
        solid_bounds=(),
    )

    assert movement == pygame.Vector2(1.0, 1.0)
    assert npc.entity.position == pygame.Vector2(1.0, 1.0)


def test_move_npc_towards_respects_solid_bounds() -> None:
    npc = make_npc()
    wall = AABB(x=15.0, y=0.0, width=10.0, height=10.0)

    movement = move_npc_towards(
        npc,
        target=pygame.Vector2(30.0, 0.0),
        speed=20.0,
        delta_time=1.0,
        solid_bounds=(wall,),
    )

    assert movement == pygame.Vector2(5.0, 0.0)
    assert npc.entity.position == pygame.Vector2(5.0, 0.0)
