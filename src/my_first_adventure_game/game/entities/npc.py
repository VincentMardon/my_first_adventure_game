from dataclasses import dataclass

import pygame

from my_first_adventure_game.engine.world import Entity


@dataclass(slots=True)
class NPC:
    """Represent a named non-player character with ordered dialogue lines.

    Attributes:
        name: Non-blank name displayed as the dialogue speaker.
        entity: Spatial entity used for identity, geometry, and active state.
        dialogue_lines: Ordered text lines displayed during interaction.
        movement_target: Optional destination for autonomous movement.
        movement_target_entity: Optional spatial entity followed during
            autonomous movement.
        movement_speed: Movement speed expressed in pixels per second.
    """

    name: str
    entity: Entity
    dialogue_lines: tuple[str, ...]
    movement_target: pygame.Vector2 | None = None
    movement_target_entity: Entity | None = None
    movement_speed: float = 0.0

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name must not be blank")
        if not self.dialogue_lines:
            raise ValueError("dialogue_lines must not be empty")

        if any(not line.strip() for line in self.dialogue_lines):
            raise ValueError("dialogue_lines must not contain blank lines")

        if self.movement_speed < 0.0:
            raise ValueError("movement_speed must not be negative")

        if self.movement_target is not None and self.movement_target_entity is not None:
            raise ValueError("movement targets must be mutually exclusive")

        if (
            self.movement_target is not None or self.movement_target_entity is not None
        ) and self.movement_speed == 0.0:
            raise ValueError(
                "movement_speed must be positive when a movement target is set"
            )

        if self.movement_target is not None:
            self.movement_target = pygame.Vector2(self.movement_target)
