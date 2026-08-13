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
