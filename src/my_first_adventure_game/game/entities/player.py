from dataclasses import dataclass

from my_first_adventure_game.engine.world import Entity


@dataclass(slots=True)
class Player:
    """Represent the concrete player with spatial state and health.

    Attributes:
        entity: Spatial entity used for identity, geometry, and active state.
        health: Current player health.
    """

    entity: Entity
    health: int

    def __post_init__(self) -> None:
        if self.health <= 0:
            raise ValueError("health must be positive.")

    def take_damage(self, damage: int) -> bool:
        """Apply damage and report whether this hit defated the player."""
        if damage <= 0:
            raise ValueError("damage must be positive.")

        if self.health == 0:
            return False

        self.health = max(0, self.health - damage)

        if self.health > 0:
            return False

        self.entity.active = False
        return True
