import pygame
import pytest

from my_first_adventure_game.engine.world import Entity
from my_first_adventure_game.game.entities import NPC


def _create_entity() -> Entity:
    return Entity(
        entity_id="npc-1",
        position=pygame.Vector2(160.0, 120.0),
        size=pygame.Vector2(24.0, 32.0),
    )


def test_npc_stores_name_spatial_entity_and_dialogue_lines() -> None:
    entity = _create_entity()
    dialogue_lines = (
        "Welcome, traveler!",
        "The road ahead is dangerous.",
    )

    npc = NPC(
        entity=entity,
        name="Guide",
        dialogue_lines=dialogue_lines,
    )

    assert npc.name == "Guide"
    assert npc.entity is entity
    assert npc.dialogue_lines is dialogue_lines


def test_npc_requires_at_least_one_dialogue_line() -> None:
    with pytest.raises(
        ValueError,
        match="dialogue_lines must not be empty",
    ):
        NPC(
            name="Guide",
            entity=_create_entity(),
            dialogue_lines=(),
        )


@pytest.mark.parametrize(
    "dialogue_lines",
    [
        ("",),
        ("   ",),
        ("Welcome, traveler!", ""),
        ("Welcome, traveler!", "   "),
    ],
)
def test_npc_requires_non_blank_dialogue_lines(
    dialogue_lines: tuple[str, ...],
) -> None:
    with pytest.raises(
        ValueError,
        match="dialogue_lines must not contain blank lines",
    ):
        NPC(
            name="Guide",
            entity=_create_entity(),
            dialogue_lines=dialogue_lines,
        )


@pytest.mark.parametrize("name", ["", "   "])
def test_npc_requires_non_blank_name(name: str) -> None:
    with pytest.raises(
        ValueError,
        match="name must not be blank",
    ):
        NPC(
            name=name,
            entity=_create_entity(),
            dialogue_lines=("Welcome, traveler!",),
        )


def test_npc_is_stationary_by_default() -> None:
    npc = NPC(
        name="Guide",
        entity=_create_entity(),
        dialogue_lines=("Welcome, traveler!",),
    )

    assert npc.movement_target is None
    assert npc.movement_target_id is None
    assert npc.movement_speed == 0.0
    assert npc.movement_target_entity is None


def test_npc_copies_movement_target() -> None:
    movement_target = pygame.Vector2(320.0, 240.0)

    npc = NPC(
        name="Caretaker",
        entity=_create_entity(),
        dialogue_lines=("I have work to do.",),
        movement_target=movement_target,
        movement_target_id="dirty-wall",
        movement_speed=80.0,
    )

    movement_target.update(0.0, 0.0)

    assert npc.movement_target == pygame.Vector2(320.0, 240.0)
    assert npc.movement_target is not movement_target
    assert npc.movement_target_id == "dirty-wall"
    assert npc.movement_speed == 80.0


def test_npc_rejects_negative_movement_speed() -> None:
    with pytest.raises(
        ValueError,
        match="movement_speed must not be negative",
    ):
        NPC(
            name="Caretaker",
            entity=_create_entity(),
            dialogue_lines=("I have work to do.",),
            movement_speed=-1.0,
        )


def test_npc_requires_positive_speed_for_movement_target() -> None:
    with pytest.raises(
        ValueError,
        match="movement_speed must be positive when a movement target is set",
    ):
        NPC(
            name="Caretaker",
            entity=_create_entity(),
            dialogue_lines=("I have work to do.",),
            movement_target=pygame.Vector2(320.0, 240.0),
        )


def test_npc_keeps_movement_target_entity_reference() -> None:
    target_entity = Entity(
        entity_id="player",
        position=pygame.Vector2(320.0, 240.0),
        size=pygame.Vector2(24.0, 24.0),
    )

    npc = NPC(
        name="Caretaker",
        entity=_create_entity(),
        dialogue_lines=("Stop dirtying my walls!",),
        movement_target_entity=target_entity,
        movement_speed=80.0,
    )

    target_entity.position.update(480.0, 360.0)

    assert npc.movement_target_entity is target_entity
    assert npc.movement_target_entity.position == pygame.Vector2(480.0, 360.0)


def test_npc_requires_positive_speed_for_movement_target_entity() -> None:
    with pytest.raises(
        ValueError,
        match="movement_speed must be positive when a movement target is set",
    ):
        NPC(
            name="Caretaker",
            entity=_create_entity(),
            dialogue_lines=("Stop dirtying my walls!",),
            movement_target_entity=Entity(
                entity_id="player",
                position=pygame.Vector2(320.0, 240.0),
                size=pygame.Vector2(24.0, 24.0),
            ),
        )


def test_npc_rejects_multiple_movement_targets() -> None:
    with pytest.raises(
        ValueError,
        match="movement targets must be mutually exclusive",
    ):
        NPC(
            name="Caretaker",
            entity=_create_entity(),
            dialogue_lines=("I have work to do.",),
            movement_target=pygame.Vector2(320.0, 240.0),
            movement_target_entity=Entity(
                entity_id="player",
                position=pygame.Vector2(480.0, 360.0),
                size=pygame.Vector2(24.0, 24.0),
            ),
            movement_speed=80.0,
        )


def test_npc_requires_fixed_target_for_movement_target_id() -> None:
    with pytest.raises(
        ValueError,
        match="movement_target_id requires a fixed movement target",
    ):
        NPC(
            name="Caretaker",
            entity=_create_entity(),
            dialogue_lines=("I have work to do.",),
            movement_target_id="dirty-wall",
        )


@pytest.mark.parametrize("movement_target_id", ["", "   "])
def test_nep_requires_non_blank_movement_target_id(
    movement_target_id: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="movement_target_id must not be blank",
    ):
        NPC(
            name="Caretaker",
            entity=_create_entity(),
            dialogue_lines=("I have work to do.",),
            movement_target=pygame.Vector2(320.0, 240.0),
            movement_target_id=movement_target_id,
            movement_speed=80.0,
        )
