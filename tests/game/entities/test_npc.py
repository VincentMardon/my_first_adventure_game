import pygame
import pytest

from my_first_adventure_game.engine.world import Entity
from my_first_adventure_game.game.entities import NPC


def test_npc_stores_spatial_entity_and_dialogue_text() -> None:
    entity = Entity(
        entity_id="npc-1",
        position=pygame.Vector2(160.0, 120.0),
        size=pygame.Vector2(24.0, 32.0),
    )

    npc = NPC(
        entity=entity,
        dialogue_text="Welcome, traveler!",
    )

    assert npc.entity is entity
    assert npc.dialogue_text == "Welcome, traveler!"


@pytest.mark.parametrize("dialogue_text", ["", "   "])
def test_npc_requires_non_empty_dialogue_text(dialogue_text: str) -> None:
    entity = Entity(
        entity_id="npc-1",
        position=pygame.Vector2(),
        size=pygame.Vector2(24.0, 32.0),
    )

    with pytest.raises(ValueError, match="dialogue_text must not be blank"):
        NPC(
            entity=entity,
            dialogue_text=dialogue_text,
        )
