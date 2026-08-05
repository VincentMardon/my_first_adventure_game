import pygame

from my_first_adventure_game.engine.collisions import AABB


class Entity:
    """Store the minimal spatial state shared by world entities."""

    __slots__ = ("_entity_id", "active", "position", "size")

    def __init__(
        self,
        entity_id: str,
        position: pygame.Vector2,
        size: pygame.Vector2,
        *,
        active: bool = True,
    ) -> None:
        self._entity_id = entity_id
        self.position = position.copy()
        self.size = size.copy()
        self.active = active

    @property
    def entity_id(self) -> str:
        """Return the stable entity identifier."""
        return self._entity_id

    @property
    def bounds(self) -> AABB:
        """Return an immutable snapshot of the current entity geometry."""
        return AABB(
            x=self.position.x,
            y=self.position.y,
            width=self.size.x,
            height=self.size.y,
        )
