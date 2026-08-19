from dataclasses import dataclass

import pygame


@dataclass(frozen=True, slots=True)
class WallStain:
    """Describe a dirty point on a wall surface.

    Attributes:
        wall_id: Stable identifier of the dirty wall.
        contact_position: Contact point on the wall surface.
        surface_normal: Axis-aligned unit vector pointing away from the wall.
    """

    wall_id: str
    contact_position: tuple[float, float]
    surface_normal: tuple[float, float]

    def approach_position(
        self,
        entity_size: pygame.Vector2,
    ) -> pygame.Vector2:
        """Return the top-left position placing an entity against the stain."""
        half_width = entity_size.x / 2.0
        half_height = entity_size.y / 2.0

        return pygame.Vector2(
            self.contact_position[0] - half_width + self.surface_normal[0] * half_width,
            self.contact_position[1]
            - half_height
            + self.surface_normal[1] * half_height,
        )
