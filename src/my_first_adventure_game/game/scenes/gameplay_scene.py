from collections.abc import Callable

import pygame

from my_first_adventure_game.engine.input import InputState, movement_axis
from my_first_adventure_game.engine.scenes import Scene
from my_first_adventure_game.engine.world import Entity, move_entity
from my_first_adventure_game.game.events import ItemCollected
from my_first_adventure_game.game.input import GameAction

PLAYER_SPEED = 160.0
PLAYER_COLOR = (224, 196, 96)
WALL_COLOR = (84, 104, 92)
COLLECTIBLE_COLOR = (112, 200, 224)
BACKGROUND_COLOR = (18, 32, 24)


class GameplayScene(Scene):
    """Run the concrete top-down gameplay state."""

    def __init__(
        self,
        input_state: InputState[GameAction],
        player: Entity,
        walls: tuple[Entity, ...],
        collectibles: tuple[Entity, ...],
        on_item_collected: Callable[[ItemCollected], None],
    ) -> None:
        self._input_state = input_state
        self._player = player
        self._walls = walls
        self._collectibles = collectibles
        self._on_item_collected = on_item_collected

    def handle_event(self, event: pygame.event.Event) -> None:
        return None

    def update(self, delta_time: float) -> None:
        axis = movement_axis(
            self._input_state,
            left=GameAction.MOVE_LEFT,
            right=GameAction.MOVE_RIGHT,
            up=GameAction.MOVE_UP,
            down=GameAction.MOVE_DOWN,
        )
        movement = axis * PLAYER_SPEED * delta_time
        solid_bounds = tuple(wall.bounds for wall in self._walls)

        move_entity(self._player, movement, solid_bounds)

        player_bounds = self._player.bounds

        for collectible in self._collectibles:
            if collectible.active and player_bounds.overlaps(collectible.bounds):
                collectible.active = False
                self._on_item_collected(ItemCollected(item_id=collectible.entity_id))

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND_COLOR)

        for wall in self._walls:
            pygame.draw.rect(
                surface,
                WALL_COLOR,
                _entity_rect(wall),
            )

        for collectible in self._collectibles:
            if collectible.active:
                pygame.draw.rect(
                    surface,
                    COLLECTIBLE_COLOR,
                    _entity_rect(collectible),
                )

        pygame.draw.rect(
            surface,
            PLAYER_COLOR,
            _entity_rect(self._player),
        )


def _entity_rect(entity: Entity) -> pygame.Rect:
    return pygame.Rect(
        round(entity.position.x),
        round(entity.position.y),
        round(entity.size.x),
        round(entity.size.y),
    )
