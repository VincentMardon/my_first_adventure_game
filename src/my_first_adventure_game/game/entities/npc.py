from dataclasses import dataclass

from my_first_adventure_game.engine.world import Entity


@dataclass(slots=True)
class NPC:
    """Represent a concrete non-player character with one dialog line.

    Attributes:
        entity: Spatial entity used for identity, geometry, and active state.
        dialogue_text: Text displayed when the player speaks to this character.
    """

    entity: Entity
    dialogue_text: str

    def __post_init__(self) -> None:
        if not self.dialogue_text.strip():
            raise ValueError("dialogue_text must not be blank")
