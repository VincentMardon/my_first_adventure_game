from collections.abc import Callable

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.collisions import AABB
from my_first_adventure_game.engine.graphics import Animation, draw_text
from my_first_adventure_game.engine.input import InputState, movement_axis
from my_first_adventure_game.engine.scenes import Scene
from my_first_adventure_game.engine.world import Entity, move_entity
from my_first_adventure_game.game.entities import NPC, move_npc_towards
from my_first_adventure_game.game.events import (
    EnemyDefeated,
    ItemCollected,
    NPCTargetReached,
    ObstacleDestroyed,
    PlayerDefeated,
    WallTouched,
)
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.levels import GameMap, MapExit
from my_first_adventure_game.game.progression import GuideObjective
from my_first_adventure_game.game.scoring import SessionScore

ATTACK_REACH = 16.0
COLLECTIBLE_COLOR = (112, 200, 224)
ENEMY_COLOR = (200, 72, 96)
ENEMY_CONTACT_DAMAGE = 1
ENEMY_CONTACT_REACH = 1.0
ENEMY_HIT_COLOR = (255, 224, 224)
ENEMY_HIT_DURATION = 0.15
EXIT_COLOR = (168, 112, 240)
HEALTH_COLOR = (248, 112, 112)
HEALTH_CENTER = (80, 52)
INTERACTION_REACH = 16.0
NPC_COLOR = (112, 160, 240)
OBJECTIVE_CENTER = (640, 24)
OBJECTIVE_COLOR = (200, 220, 240)
PLAYER_ATTACK_DAMAGE = 1
PLAYER_SPEED = 160.0
PLAYER_INVULNERABILITY_DURATION = 1.0
SCORE_COLOR = (240, 240, 240)
SCORE_CENTER = (80, 24)
SCORE_FONT_PATH = pygame.font.get_default_font()
SCORE_FONT_SIZE = 24
WALL_COLOR = (84, 104, 92)


class GameplayScene(Scene):
    """Run the concrete top-down gameplay state."""

    def __init__(
        self,
        input_state: InputState[GameAction],
        font_cache: FontCache,
        session_score: SessionScore,
        game_map: GameMap,
        on_pause_requested: Callable[[], None],
        on_player_defeated: Callable[[PlayerDefeated], None],
        on_npc_interacted: Callable[[NPC], None],
        on_npc_target_reached: Callable[[NPCTargetReached], None],
        on_enemy_defeated: Callable[[EnemyDefeated], None],
        on_item_collected: Callable[[ItemCollected], None],
        on_obstacle_destroyed: Callable[[ObstacleDestroyed], None],
        on_wall_touched: Callable[[WallTouched], None],
        player_idle_animation: Animation,
        player_movement_animation: Animation,
        player_collection_animation: Animation,
        player_attack_animation: Animation,
        guide_objective: GuideObjective,
        on_map_exit_reached: Callable[[MapExit], None],
    ) -> None:
        self._input_state = input_state
        self._font_cache = font_cache
        self._session_score = session_score
        self._on_pause_requested = on_pause_requested
        self._player_invulnerability_remaining = 0.0
        self._on_player_defeated = on_player_defeated
        self._on_npc_interacted = on_npc_interacted
        self._on_npc_target_reached = on_npc_target_reached
        self._on_enemy_defeated = on_enemy_defeated
        self._on_item_collected = on_item_collected
        self._on_obstacle_destroyed = on_obstacle_destroyed
        self._on_wall_touched = on_wall_touched
        self._player_idle_animation = player_idle_animation
        self._player_movement_animation = player_movement_animation
        self._player_animation = player_idle_animation
        self._player_collection_animation = player_collection_animation
        self._player_is_collecting = False
        self._player_attack_animation = player_attack_animation
        self._player_is_attacking = False
        self._guide_objective = guide_objective
        self._on_map_exit_reached = on_map_exit_reached
        self.change_map(game_map)

    def handle_event(self, event: pygame.event.Event) -> None:
        return None

    def change_map(self, game_map: GameMap) -> None:
        """Replace the spatial content managed by the gameplay scene."""
        self._player = game_map.player
        self._background_color = game_map.background_color
        self._walls = game_map.walls
        self._enemies = game_map.enemies
        self._npcs = game_map.npcs
        self._collectibles = game_map.collectibles
        self._destructible_obstacles = game_map.destructible_obstacles
        self._exits = game_map.exits
        self._enemy_hit_time_remaining = {
            enemy.entity.entity_id: 0.0 for enemy in game_map.enemies
        }

    def update(self, delta_time: float) -> None:
        if self._input_state.is_pressed(GameAction.PAUSE):
            self._on_pause_requested()
            return

        if not self._player.entity.active:
            return

        if self._input_state.is_pressed(GameAction.INTERACT):
            player_bounds = self._player.entity.bounds

            for npc in self._npcs:
                if npc.entity.active and _within_interaction_reach(
                    player_bounds,
                    npc.entity.bounds,
                ):
                    self._on_npc_interacted(npc)
                    return

        self._player_invulnerability_remaining = max(
            0.0,
            self._player_invulnerability_remaining - delta_time,
        )

        for enemy_id, time_remaining in self._enemy_hit_time_remaining.items():
            self._enemy_hit_time_remaining[enemy_id] = max(
                0.0,
                time_remaining - delta_time,
            )

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
            *(npc.entity.bounds for npc in self._npcs if npc.entity.active),
        )
        player_bounds_before_movement = self._player.entity.bounds
        applied_movement = move_entity(
            self._player.entity,
            movement,
            solid_bounds,
        )
        wall_contact = _find_wall_contact(
            player_bounds_before_movement,
            movement,
            applied_movement,
            self._walls,
        )

        if wall_contact is not None:
            self._on_wall_touched(wall_contact)

        for npc in self._npcs:
            target_entity = npc.movement_target_entity
            target = (
                target_entity.position
                if target_entity is not None
                else npc.movement_target
            )

            if not npc.entity.active or target is None:
                continue

            npc_solid_bounds = (
                *(wall.bounds for wall in self._walls if wall.active),
                *((self._player.entity.bounds,) if self._player.entity.active else ()),
                *(
                    enemy.entity.bounds
                    for enemy in self._enemies
                    if enemy.entity.active
                ),
                *(
                    other_npc.entity.bounds
                    for other_npc in self._npcs
                    if other_npc is not npc and other_npc.entity.active
                ),
            )

            move_npc_towards(
                npc,
                target,
                speed=npc.movement_speed,
                delta_time=delta_time,
                solid_bounds=npc_solid_bounds,
            )

            if (
                target_entity is None
                and npc.movement_target_id is not None
                and npc.entity.position == target
            ):
                self._on_npc_target_reached(
                    NPCTargetReached(
                        npc_id=npc.entity.entity_id,
                        target_id=npc.movement_target_id,
                    )
                )
                return

            if target_entity is not None and _within_interaction_reach(
                npc.entity.bounds,
                target_entity.bounds,
            ):
                self._on_npc_target_reached(
                    NPCTargetReached(
                        npc_id=npc.entity.entity_id,
                        target_id=target_entity.entity_id,
                    )
                )
                return

        player_bounds = self._player.entity.bounds

        for map_exit in self._exits:
            if map_exit.entity.active and player_bounds.overlaps(
                map_exit.entity.bounds
            ):
                self._on_map_exit_reached(map_exit)
                return

        if self._player.entity.active and self._player_invulnerability_remaining <= 0.0:
            contact_bounds = AABB(
                x=player_bounds.x - ENEMY_CONTACT_REACH,
                y=player_bounds.y - ENEMY_CONTACT_REACH,
                width=player_bounds.width + ENEMY_CONTACT_REACH * 2.0,
                height=player_bounds.height + ENEMY_CONTACT_REACH * 2.0,
            )

            for enemy in self._enemies:
                if enemy.entity.active and contact_bounds.overlaps(enemy.entity.bounds):
                    player_defeated = self._player.take_damage(ENEMY_CONTACT_DAMAGE)

                    if player_defeated:
                        self._on_player_defeated(
                            PlayerDefeated(player_id=self._player.entity.entity_id)
                        )
                        return

                    self._player_invulnerability_remaining = (
                        PLAYER_INVULNERABILITY_DURATION
                    )
                    break

        attack_started = self._input_state.is_pressed(GameAction.ATTACK)

        if attack_started:
            attack_bounds = AABB(
                x=player_bounds.x - ATTACK_REACH,
                y=player_bounds.y - ATTACK_REACH,
                width=player_bounds.width + ATTACK_REACH * 2.0,
                height=player_bounds.height + ATTACK_REACH * 2.0,
            )

            for enemy in self._enemies:
                if not enemy.entity.active:
                    continue

                if not attack_bounds.overlaps(enemy.entity.bounds):
                    continue

                defeated = enemy.take_damage(PLAYER_ATTACK_DAMAGE)

                if defeated:
                    self._on_enemy_defeated(
                        EnemyDefeated(enemy_id=enemy.entity.entity_id)
                    )
                else:
                    self._enemy_hit_time_remaining[enemy.entity.entity_id] = (
                        ENEMY_HIT_DURATION
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
        surface.fill(self._background_color)

        for wall in self._walls:
            if wall.active:
                pygame.draw.rect(
                    surface,
                    WALL_COLOR,
                    _entity_rect(wall),
                )

        for enemy in self._enemies:
            if enemy.entity.active:
                color = (
                    ENEMY_HIT_COLOR
                    if self._enemy_hit_time_remaining[enemy.entity.entity_id] > 0.0
                    else ENEMY_COLOR
                )
                pygame.draw.rect(surface, color, _entity_rect(enemy.entity))

        for npc in self._npcs:
            if npc.entity.active:
                pygame.draw.rect(
                    surface,
                    NPC_COLOR,
                    _entity_rect(npc.entity),
                )

        for collectible in self._collectibles:
            if collectible.active:
                pygame.draw.rect(
                    surface,
                    COLLECTIBLE_COLOR,
                    _entity_rect(collectible),
                )

        for map_exit in self._exits:
            if map_exit.entity.active:
                pygame.draw.rect(surface, EXIT_COLOR, _entity_rect(map_exit.entity))

        surface.blit(
            self._player_animation.current_frame,
            _entity_rect(self._player.entity),
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
        draw_text(
            surface,
            f"Health: {self._player.health}",
            score_font,
            HEALTH_COLOR,
            center=HEALTH_CENTER,
        )
        draw_text(
            surface,
            self._guide_objective.status_text,
            score_font,
            OBJECTIVE_COLOR,
            center=OBJECTIVE_CENTER,
        )


def _entity_rect(entity: Entity) -> pygame.Rect:
    return pygame.Rect(
        round(entity.position.x),
        round(entity.position.y),
        round(entity.size.x),
        round(entity.size.y),
    )


def _find_wall_contact(
    initial_bounds: AABB,
    requested_movement: pygame.Vector2,
    applied_movement: pygame.Vector2,
    walls: tuple[Entity, ...],
) -> WallTouched | None:
    horizontal_bounds = AABB(
        x=initial_bounds.x + applied_movement.x,
        y=initial_bounds.y,
        width=initial_bounds.width,
        height=initial_bounds.height,
    )
    final_bounds = AABB(
        x=horizontal_bounds.x,
        y=horizontal_bounds.y + applied_movement.y,
        width=horizontal_bounds.width,
        height=horizontal_bounds.height,
    )

    for wall in walls:
        if not wall.active:
            continue

        wall_bounds = wall.bounds

        if applied_movement.x != requested_movement.x and _touches_horizontally(
            horizontal_bounds,
            wall_bounds,
            requested_movement.x,
        ):
            contact_x = (
                wall_bounds.left if requested_movement.x > 0.0 else wall_bounds.right
            )
            contact_y = min(
                max(
                    horizontal_bounds.y + horizontal_bounds.height / 2.0,
                    wall_bounds.top,
                ),
                wall_bounds.bottom,
            )
            surface_normal = (-1.0, 0.0) if requested_movement.x > 0.0 else (1.0, 0.0)

            return WallTouched(
                wall_id=wall.entity_id,
                contact_position=(contact_x, contact_y),
                surface_normal=surface_normal,
            )

        if applied_movement.y != requested_movement.y and _touches_vertically(
            final_bounds,
            wall_bounds,
            requested_movement.y,
        ):
            contact_x = min(
                max(
                    final_bounds.x + final_bounds.width / 2.0,
                    wall_bounds.left,
                ),
                wall_bounds.right,
            )
            contact_y = (
                wall_bounds.top if requested_movement.y > 0.0 else wall_bounds.bottom
            )
            surface_normal = (0.0, -1.0) if requested_movement.y > 0.0 else (0.0, 1.0)
            return WallTouched(
                wall_id=wall.entity_id,
                contact_position=(contact_x, contact_y),
                surface_normal=surface_normal,
            )

    return None


def _touches_horizontally(
    moving_bounds: AABB,
    wall_bounds: AABB,
    movement: float,
) -> bool:
    vertical_overlap = (
        moving_bounds.top < wall_bounds.bottom
        and moving_bounds.bottom > wall_bounds.top
    )

    return vertical_overlap and (
        (movement > 0.0 and moving_bounds.right == wall_bounds.left)
        or (movement < 0.0 and moving_bounds.left == wall_bounds.right)
    )


def _touches_vertically(
    moving_bounds: AABB,
    wall_bounds: AABB,
    movement: float,
) -> bool:
    horizontal_overlap = (
        moving_bounds.left < wall_bounds.right
        and moving_bounds.right > wall_bounds.left
    )

    return horizontal_overlap and (
        (movement > 0.0 and moving_bounds.bottom == wall_bounds.top)
        or (movement < 0.0 and moving_bounds.top == wall_bounds.bottom)
    )


def _within_interaction_reach(
    source_bounds: AABB,
    target_bounds: AABB,
) -> bool:
    reach_bounds = AABB(
        x=source_bounds.x - INTERACTION_REACH,
        y=source_bounds.y - INTERACTION_REACH,
        width=source_bounds.width + INTERACTION_REACH * 2.0,
        height=source_bounds.height + INTERACTION_REACH * 2.0,
    )

    return reach_bounds.overlaps(target_bounds)
