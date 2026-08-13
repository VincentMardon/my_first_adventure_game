from dataclasses import dataclass

from my_first_adventure_game.engine.world import Entity


@dataclass(slots=True)
class NPC:
    """Represent a concrete non-player character with ordered dialogue lines.

    Attributes:
        entity: Spatial entity used for identity, geometry, and active state.
        dialogue_lines: Ordered text lines displayed during interaction.
    """

    entity: Entity
    dialogue_lines: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.dialogue_lines:
            raise ValueError("dialogue_lines must not be empty")

        if any(not line.strip() for line in self.dialogue_lines):
            raise ValueError("dialogue_lines must not contain blank lines")
