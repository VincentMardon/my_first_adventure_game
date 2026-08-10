from collections.abc import Callable

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.collisions import AABB
from my_first_adventure_game.engine.graphics import Animation, draw_text
from my_first_adventure_game.engine.input import InputState, movement_axis
from my_first_adventure_game.engine.scenes import Scene
from my_first_adventure_game.engine.world import Entity, move_entity
from my_first_adventure_game.game.entities import Enemy
from my_first_adventure_game.game.events import (
    EnemyDefeated,
    ItemCollected,
    ObstacleDestroyed,
)
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scoring import SessionScore

PLAYER_SPEED = 160.0
PLAYER_ATTACK_DAMAGE = 1
WALL_COLOR = (84, 104, 92)
ENEMY_COLOR = (200, 72, 96)
COLLECTIBLE_COLOR = (112, 200, 224)
BACKGROUND_COLOR = (18, 32, 24)
SCORE_COLOR = (240, 240, 240)
SCORE_CENTER = (80, 24)
SCORE_FONT_PATH = pygame.font.get_default_font()
SCORE_FONT_SIZE = 24
ATTACK_REACH = 16.0


class GameplayScene(Scene):
    """Run the concrete top-down gameplay state."""

    def __init__(
        self,
        input_state: InputState[GameAction],
        font_cache: FontCache,
        session_score: SessionScore,
        player: Entity,
        walls: tuple[Entity, ...],
        enemies: tuple[Enemy, ...],
        on_enemy_defeated: Callable[[EnemyDefeated], None],
        collectibles: tuple[Entity, ...],
        on_item_collected: Callable[[ItemCollected], None],
        destructible_obstacles: tuple[Entity, ...],
        on_obstacle_destroyed: Callable[[ObstacleDestroyed], None],
        player_idle_animation: Animation,
        player_movement_animation: Animation,
        player_collection_animation: Animation,
        player_attack_animation: Animation,
    ) -> None:
        self._input_state = input_state
        self._font_cache = font_cache
        self._session_score = session_score
        self._player = player
        self._walls = walls
        self._enemies = enemies
        self._on_enemy_defeated = on_enemy_defeated
        self._collectibles = collectibles
        self._on_item_collected = on_item_collected
        self._destructible_obstacles = destructible_obstacles
        self._on_obstacle_destroyed = on_obstacle_destroyed
        self._player_idle_animation = player_idle_animation
        self._player_movement_animation = player_movement_animation
        self._player_animation = player_idle_animation
        self._player_collection_animation = player_collection_animation
        self._player_is_collecting = False
        self._player_attack_animation = player_attack_animation
        self._player_is_attacking = False

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
        solid_bounds = (
            *(wall.bounds for wall in self._walls if wall.active),
            *(enemy.entity.bounds for enemy in self._enemies if enemy.entity.active),
        )

        move_entity(self._player, movement, solid_bounds)

        player_bounds = self._player.bounds

        attack_started = self._input_state.is_pressed(GameAction.ATTACK)

        if attack_started:
            attack_bounds = AABB(
                x=player_bounds.x - ATTACK_REACH,
                y=player_bounds.y - ATTACK_REACH,
                width=player_bounds.width + ATTACK_REACH * 2.0,
                height=player_bounds.height + ATTACK_REACH * 2.0,
            )

            for enemy in self._enemies:
                if (
                    enemy.entity.active
                    and attack_bounds.overlaps(enemy.entity.bounds)
                    and enemy.take_damage(PLAYER_ATTACK_DAMAGE)
                ):
                    self._on_enemy_defeated(
                        EnemyDefeated(enemy_id=enemy.entity.entity_id)
                    )

            for obstacle in self._destructible_obstacles:
                if obstacle.active and attack_bounds.overlaps(obstacle.bounds):
                    obstacle.active = False
                    self._on_obstacle_destroyed(
                        ObstacleDestroyed(obstacle_id=obstacle.entity_id)
                    )

        collection_started = False

        for collectible in self._collectibles:
            if collectible.active and player_bounds.overlaps(collectible.bounds):
                collectible.active = False
                self._on_item_collected(ItemCollected(item_id=collectible.entity_id))
                collection_started = True

        if collection_started:
            self._player_is_collecting = True
            self._player_is_attacking = False
            self._player_animation = self._player_collection_animation
            self._player_collection_animation.reset()
        elif attack_started and not self._player_is_collecting:
            self._player_is_attacking = True
            self._player_animation = self._player_attack_animation
            self._player_attack_animation.reset()
        elif not self._player_is_collecting and not self._player_is_attacking:
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
        elif self._player_is_attacking and self._player_attack_animation.finished:
            self._player_is_attacking = False

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND_COLOR)

        for wall in self._walls:
            if wall.active:
                pygame.draw.rect(
                    surface,
                    WALL_COLOR,
                    _entity_rect(wall),
                )

        for enemy in self._enemies:
            if enemy.entity.active:
                pygame.draw.rect(
                    surface,
                    ENEMY_COLOR,
                    _entity_rect(enemy.entity),
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
