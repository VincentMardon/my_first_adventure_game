from collections.abc import Callable

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.graphics import Animation, draw_text
from my_first_adventure_game.engine.input import InputState, movement_axis
from my_first_adventure_game.engine.scenes import Scene
from my_first_adventure_game.engine.world import Entity, move_entity
from my_first_adventure_game.game.events import ItemCollected
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scoring import SessionScore

PLAYER_SPEED = 160.0
WALL_COLOR = (84, 104, 92)
COLLECTIBLE_COLOR = (112, 200, 224)
BACKGROUND_COLOR = (18, 32, 24)
SCORE_COLOR = (240, 240, 240)
SCORE_CENTER = (80, 24)
SCORE_FONT_PATH = pygame.font.get_default_font()
SCORE_FONT_SIZE = 24


class GameplayScene(Scene):
    """Run the concrete top-down gameplay state."""

    def __init__(
        self,
        input_state: InputState[GameAction],
        font_cache: FontCache,
        session_score: SessionScore,
        player: Entity,
        walls: tuple[Entity, ...],
        collectibles: tuple[Entity, ...],
        on_item_collected: Callable[[ItemCollected], None],
        player_idle_animation: Animation,
        player_movement_animation: Animation,
        player_collection_animation: Animation,
    ) -> None:
        self._input_state = input_state
        self._font_cache = font_cache
        self._session_score = session_score
        self._player = player
        self._walls = walls
        self._collectibles = collectibles
        self._on_item_collected = on_item_collected
        self._player_idle_animation = player_idle_animation
        self._player_movement_animation = player_movement_animation
        self._player_animation = player_idle_animation
        self._player_collection_animation = player_collection_animation
        self._player_is_collecting = False

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
        collection_started = False

        for collectible in self._collectibles:
            if collectible.active and player_bounds.overlaps(collectible.bounds):
                collectible.active = False
                self._on_item_collected(ItemCollected(item_id=collectible.entity_id))
                collection_started = True

        if collection_started:
            self._player_is_collecting = True
            self._player_animation = self._player_collection_animation
            self._player_collection_animation.reset()
        elif not self._player_is_collecting:
            next_player_animation = (
                self._player_movement_animation
                if axis.length_squared() > 0.0
                else self._player_idle_animation
            )

            if next_player_animation is not self._player_animation:
                self._player_animation = next_player_animation
                self._player_animation.reset()

        self._player_animation.update(delta_time)

        if self._player_is_collecting and self._player_collection_animation.finished:
            self._player_is_collecting = False

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

        surface.blit(
            self._player_animation.current_frame,
            _entity_rect(self._player),
        )

        score_font = self._font_cache.load(
            SCORE_FONT_PATH,
            SCORE_FONT_SIZE,
        )
        draw_text(
            surface,
            f"Score: {self._session_score.value}",
            score_font,
            SCORE_COLOR,
            center=SCORE_CENTER,
        )


def _entity_rect(entity: Entity) -> pygame.Rect:
    return pygame.Rect(
        round(entity.position.x),
        round(entity.position.y),
        round(entity.size.x),
        round(entity.size.y),
    )
