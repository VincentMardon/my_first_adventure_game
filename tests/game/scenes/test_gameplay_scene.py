from collections.abc import Callable
from unittest.mock import Mock, call

import pygame
import pytest

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.graphics import Animation
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.engine.world import Entity, World
from my_first_adventure_game.game.entities import NPC, Enemy, Player
from my_first_adventure_game.game.events import (
    EnemyDefeated,
    ItemCollected,
    NPCTargetReached,
    ObstacleDestroyed,
    PlayerDefeated,
    WallTouched,
)
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.levels import (
    GameMap,
    MapExit,
    create_clearing_map,
)
from my_first_adventure_game.game.progression import GuideObjective
from my_first_adventure_game.game.scenes import gameplay_scene
from my_first_adventure_game.game.scenes.gameplay_scene import (
    COLLECTIBLE_COLOR,
    ENEMY_COLOR,
    ENEMY_CONTACT_REACH,
    ENEMY_HIT_COLOR,
    ENEMY_HIT_DURATION,
    EXIT_COLOR,
    HEALTH_CENTER,
    HEALTH_COLOR,
    NPC_COLOR,
    OBJECTIVE_CENTER,
    OBJECTIVE_COLOR,
    PLAYER_INVULNERABILITY_DURATION,
    PLAYER_SPEED,
    SCORE_CENTER,
    SCORE_COLOR,
    SCORE_FONT_PATH,
    SCORE_FONT_SIZE,
    WALL_COLOR,
    GameplayScene,
)
from my_first_adventure_game.game.scoring import SessionScore

TEST_BACKGROUND_COLOR = (18, 32, 24)


def _create_gameplay_scene(
    *,
    input_state: InputState[GameAction] | None = None,
    font_cache: FontCache | None = None,
    session_score: SessionScore | None = None,
    game_map: GameMap | None = None,
    player: Player | None = None,
    on_pause_requested: Callable[[], None] | None = None,
    on_player_defeated: Callable[[PlayerDefeated], None] | None = None,
    walls: tuple[Entity, ...] = (),
    enemies: tuple[Enemy, ...] = (),
    npcs: tuple[NPC, ...] = (),
    on_npc_interacted: Callable[[NPC], None] | None = None,
    on_npc_target_reached: Callable[[NPCTargetReached], None] | None = None,
    on_enemy_defeated: Callable[[EnemyDefeated], None] | None = None,
    collectibles: tuple[Entity, ...] = (),
    on_item_collected: Callable[[ItemCollected], None] | None = None,
    destructible_obstacles: tuple[Entity, ...] = (),
    on_obstacle_destroyed: Callable[[ObstacleDestroyed], None] | None = None,
    on_wall_touched: Callable[[WallTouched], None] | None = None,
    player_idle_animation: Animation | None = None,
    player_movement_animation: Animation | None = None,
    player_collection_animation: Animation | None = None,
    player_attack_animation: Animation | None = None,
    guide_objective: GuideObjective | None = None,
    exits: tuple[MapExit, ...] = (),
    on_map_exit_reached: Callable[[MapExit], None] | None = None,
) -> GameplayScene:
    if input_state is None:
        input_state_mock = Mock(spec=InputState)
        input_state_mock.is_pressed.return_value = False
        input_state = input_state_mock

    if player is None:
        player = Player(
            entity=Entity(
                entity_id="player",
                position=pygame.Vector2(100.0, 80.0),
                size=pygame.Vector2(24.0, 24.0),
            ),
            health=3,
        )

    if game_map is None:
        game_map = GameMap(
            map_id="test",
            background_color=TEST_BACKGROUND_COLOR,
            world=Mock(spec=World),
            player=player,
            walls=walls,
            enemies=enemies,
            npcs=npcs,
            destructible_obstacles=destructible_obstacles,
            collectibles=collectibles,
            exits=exits,
        )

    return GameplayScene(
        input_state=input_state,
        font_cache=font_cache or Mock(spec=FontCache),
        session_score=session_score or Mock(spec=SessionScore),
        game_map=game_map,
        on_pause_requested=on_pause_requested or Mock(),
        on_player_defeated=on_player_defeated or Mock(),
        on_npc_interacted=on_npc_interacted or Mock(),
        on_npc_target_reached=on_npc_target_reached or Mock(),
        on_enemy_defeated=on_enemy_defeated or Mock(),
        on_item_collected=on_item_collected or Mock(),
        on_obstacle_destroyed=on_obstacle_destroyed or Mock(),
        on_wall_touched=on_wall_touched or Mock(),
        player_idle_animation=player_idle_animation or Mock(spec=Animation),
        player_movement_animation=(player_movement_animation or Mock(spec=Animation)),
        player_collection_animation=(
            player_collection_animation or Mock(spec=Animation)
        ),
        player_attack_animation=player_attack_animation or Mock(spec=Animation),
        guide_objective=guide_objective or GuideObjective(total_items=2),
        on_map_exit_reached=on_map_exit_reached or Mock(),
    )


def test_update_moves_player_from_directional_actions(monkeypatch) -> None:
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    player = Player(
        entity=Entity(
            entity_id="player",
            position=pygame.Vector2(100.0, 80.0),
            size=pygame.Vector2(24.0, 24.0),
        ),
        health=3,
    )
    wall = Entity(
        entity_id="wall",
        position=pygame.Vector2(200.0, 80.0),
        size=pygame.Vector2(32.0, 32.0),
    )
    enemy = Enemy(
        Entity(
            entity_id="enemy",
            position=pygame.Vector2(260.0, 80.0),
            size=pygame.Vector2(32.0, 32.0),
        ),
        health=2,
    )
    npc = NPC(
        name="Guide",
        entity=Entity(
            entity_id="npc",
            position=pygame.Vector2(320.0, 80.0),
            size=pygame.Vector2(24.0, 32.0),
        ),
        dialogue_lines=("Welcome, traveler!",),
    )

    movement_axis = Mock(return_value=pygame.Vector2(0.6, 0.8))
    move_entity = Mock(return_value=pygame.Vector2())

    player_idle_animation = Mock(spec=Animation)
    player_movement_animation = Mock(spec=Animation)

    monkeypatch.setattr(gameplay_scene, "movement_axis", movement_axis)
    monkeypatch.setattr(gameplay_scene, "move_entity", move_entity)

    scene = _create_gameplay_scene(
        input_state=input_state,
        player=player,
        walls=(wall,),
        enemies=(enemy,),
        npcs=(npc,),
        player_idle_animation=player_idle_animation,
        player_movement_animation=player_movement_animation,
    )

    scene.update(0.5)

    player_movement_animation.reset.assert_called_once_with()
    player_movement_animation.update.assert_called_once_with(0.5)
    player_idle_animation.update.assert_not_called()

    movement_axis.assert_called_once_with(
        input_state,
        left=GameAction.MOVE_LEFT,
        right=GameAction.MOVE_RIGHT,
        up=GameAction.MOVE_UP,
        down=GameAction.MOVE_DOWN,
    )
    move_entity.assert_called_once_with(
        player.entity,
        pygame.Vector2(0.6, 0.8) * PLAYER_SPEED * 0.5,
        (
            wall.bounds,
            enemy.entity.bounds,
            npc.entity.bounds,
        ),
    )


@pytest.mark.parametrize(
    (
        "player_position",
        "wall_position",
        "axis",
        "expected_player_position",
        "contact_position",
        "surface_normal",
    ),
    [
        (
            (100.0, 80.0),
            (130.0, 80.0),
            (1.0, 0.0),
            (106.0, 80.0),
            (130.0, 92.0),
            (-1.0, 0.0),
        ),
        (
            (140.0, 80.0),
            (100.0, 80.0),
            (-1.0, 0.0),
            (132.0, 80.0),
            (132.0, 92.0),
            (1.0, 0.0),
        ),
        (
            (100.0, 80.0),
            (100.0, 110.0),
            (0.0, 1.0),
            (100.0, 86.0),
            (112.0, 110.0),
            (0.0, -1.0),
        ),
        (
            (100.0, 120.0),
            (100.0, 80.0),
            (0.0, -1.0),
            (100.0, 112.0),
            (112.0, 112.0),
            (0.0, 1.0),
        ),
    ],
)
def test_update_reports_wall_contacts(
    monkeypatch,
    player_position: tuple[float, float],
    wall_position: tuple[float, float],
    axis: tuple[float, float],
    expected_player_position: tuple[float, float],
    contact_position: tuple[float, float],
    surface_normal: tuple[float, float],
) -> None:
    player = Player(
        entity=Entity(
            entity_id="player",
            position=pygame.Vector2(player_position),
            size=pygame.Vector2(24.0, 24.0),
        ),
        health=3,
    )
    wall = Entity(
        entity_id="wall",
        position=pygame.Vector2(wall_position),
        size=pygame.Vector2(32.0, 32.0),
    )
    on_wall_touched = Mock()

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2(axis)),
    )

    scene = _create_gameplay_scene(
        player=player,
        walls=(wall,),
        on_wall_touched=on_wall_touched,
    )

    scene.update(0.5)

    assert player.entity.position == pygame.Vector2(expected_player_position)
    on_wall_touched.assert_called_once_with(
        WallTouched(
            wall_id="wall",
            contact_position=contact_position,
            surface_normal=surface_normal,
        )
    )


def test_update_does_not_report_wall_when_npc_blocks_movement(
    monkeypatch,
) -> None:
    player = Player(
        entity=Entity(
            entity_id="player",
            position=pygame.Vector2(100.0, 80.0),
            size=pygame.Vector2(24.0, 24.0),
        ),
        health=3,
    )
    blocking_npc = NPC(
        name="Guide",
        entity=Entity(
            entity_id="blocking-npc",
            position=pygame.Vector2(130.0, 80.0),
            size=pygame.Vector2(24.0, 32.0),
        ),
        dialogue_lines=("You shall not pass.",),
    )
    on_wall_touched = Mock()

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2(1.0, 0.0)),
    )

    scene = _create_gameplay_scene(
        player=player,
        npcs=(blocking_npc,),
        on_wall_touched=on_wall_touched,
    )

    scene.update(0.5)

    assert player.entity.position == pygame.Vector2(106.0, 80.0)
    on_wall_touched.assert_not_called()


def test_update_moves_npc_with_configured_target(monkeypatch) -> None:
    wall = Entity(
        entity_id="wall",
        position=pygame.Vector2(200.0, 200.0),
        size=pygame.Vector2(32.0, 32.0),
    )
    moving_npc = NPC(
        name="Caretaker",
        entity=Entity(
            entity_id="moving-npc",
            position=pygame.Vector2(400.0, 300.0),
            size=pygame.Vector2(24.0, 32.0),
        ),
        dialogue_lines=("I have work to do.",),
        movement_target=pygame.Vector2(500.0, 400.0),
        movement_speed=80.0,
    )
    stationary_npc = NPC(
        name="Guide",
        entity=Entity(
            entity_id="stationary-npc",
            position=pygame.Vector2(600.0, 300.0),
            size=pygame.Vector2(24.0, 32.0),
        ),
        dialogue_lines=("Welcome, traveler!",),
    )
    move_npc_towards = Mock()

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2()),
    )
    monkeypatch.setattr(
        gameplay_scene, "move_entity", Mock(return_value=pygame.Vector2())
    )
    monkeypatch.setattr(
        gameplay_scene,
        "move_npc_towards",
        move_npc_towards,
    )

    scene = _create_gameplay_scene(
        walls=(wall,),
        npcs=(moving_npc, stationary_npc),
    )

    scene.update(0.5)

    move_npc_towards.assert_called_once_with(
        moving_npc,
        moving_npc.movement_target,
        speed=80.0,
        delta_time=0.5,
        solid_bounds=(
            wall.bounds,
            scene._player.entity.bounds,
            stationary_npc.entity.bounds,
        ),
    )


def test_update_reports_when_npc_reaches_named_fixed_target(
    monkeypatch,
) -> None:
    moving_npc = NPC(
        name="Caretaker",
        entity=Entity(
            entity_id="npc-clearing-caretaker",
            position=pygame.Vector2(400.0, 300.0),
            size=pygame.Vector2(24.0, 32.0),
        ),
        dialogue_lines=("I have work to do.",),
        movement_target=pygame.Vector2(440.0, 300.0),
        movement_target_id="clearing-wall-top",
        movement_speed=80.0,
    )
    on_npc_target_reached = Mock()

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2()),
    )
    monkeypatch.setattr(
        gameplay_scene,
        "move_entity",
        Mock(return_value=pygame.Vector2()),
    )

    scene = _create_gameplay_scene(
        npcs=(moving_npc,),
        on_npc_target_reached=on_npc_target_reached,
    )

    scene.update(0.5)

    assert moving_npc.entity.position == pygame.Vector2(440.0, 300.0)
    on_npc_target_reached.assert_called_once_with(
        NPCTargetReached(
            npc_id="npc-clearing-caretaker",
            target_id="clearing-wall-top",
        )
    )


def test_update_does_not_report_blocked_named_fixed_target(
    monkeypatch,
) -> None:
    wall = Entity(
        entity_id="wall",
        position=pygame.Vector2(430.0, 300.0),
        size=pygame.Vector2(32.0, 32.0),
    )
    moving_npc = NPC(
        name="Caretaker",
        entity=Entity(
            entity_id="npc-clearing-caretaker",
            position=pygame.Vector2(400.0, 300.0),
            size=pygame.Vector2(24.0, 32.0),
        ),
        dialogue_lines=("I have work to do.",),
        movement_target=pygame.Vector2(500.0, 300.0),
        movement_target_id="dirty-wall",
        movement_speed=80.0,
    )
    on_npc_target_reached = Mock()

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2()),
    )
    monkeypatch.setattr(
        gameplay_scene,
        "move_entity",
        Mock(return_value=pygame.Vector2()),
    )

    scene = _create_gameplay_scene(
        walls=(wall,),
        npcs=(moving_npc,),
        on_npc_target_reached=on_npc_target_reached,
    )

    scene.update(2.0)

    assert moving_npc.entity.position == pygame.Vector2(406.0, 300.0)
    on_npc_target_reached.assert_not_called()


def test_update_moves_npc_toward_current_target_entity_position(
    monkeypatch,
) -> None:
    player = Player(
        entity=Entity(
            entity_id="player",
            position=pygame.Vector2(320.0, 240.0),
            size=pygame.Vector2(24.0, 24.0),
        ),
        health=3,
    )
    moving_npc = NPC(
        name="Caretaker",
        entity=Entity(
            entity_id="moving-npc",
            position=pygame.Vector2(400.0, 300.0),
            size=pygame.Vector2(24.0, 32.0),
        ),
        dialogue_lines=("Stop dirtying my walls!",),
        movement_target_entity=player.entity,
        movement_speed=80.0,
    )
    move_npc_towards = Mock()

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2()),
    )
    monkeypatch.setattr(
        gameplay_scene,
        "move_entity",
        Mock(return_value=pygame.Vector2()),
    )
    monkeypatch.setattr(
        gameplay_scene,
        "move_npc_towards",
        move_npc_towards,
    )

    scene = _create_gameplay_scene(
        player=player,
        npcs=(moving_npc,),
    )

    scene.update(0.5)

    move_npc_towards.assert_called_once_with(
        moving_npc,
        player.entity.position,
        speed=80.0,
        delta_time=0.5,
        solid_bounds=(player.entity.bounds,),
    )

    move_npc_towards.reset_mock()
    player.entity.position.update(480.0, 360.0)

    scene.update(0.25)

    move_npc_towards.assert_called_once_with(
        moving_npc,
        player.entity.position,
        speed=80.0,
        delta_time=0.25,
        solid_bounds=(player.entity.bounds,),
    )


def test_update_reports_when_npc_reaches_target_entity(
    monkeypatch,
) -> None:
    player = Player(
        entity=Entity(
            entity_id="player",
            position=pygame.Vector2(320.0, 240.0),
            size=pygame.Vector2(24.0, 24.0),
        ),
        health=3,
    )
    moving_npc = NPC(
        name="Caretaker",
        entity=Entity(
            entity_id="npc-clearing-caretaker",
            position=pygame.Vector2(400.0, 240.0),
            size=pygame.Vector2(24.0, 32.0),
        ),
        dialogue_lines=("Stop dirtying my walls!",),
        movement_target_entity=player.entity,
        movement_speed=80.0,
    )
    on_npc_target_reached = Mock()

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2()),
    )
    monkeypatch.setattr(
        gameplay_scene,
        "move_entity",
        Mock(return_value=pygame.Vector2()),
    )

    scene = _create_gameplay_scene(
        player=player,
        npcs=(moving_npc,),
        on_npc_target_reached=on_npc_target_reached,
    )

    scene.update(1.0)

    assert moving_npc.entity.position == pygame.Vector2(344.0, 240.0)
    on_npc_target_reached.assert_called_once_with(
        NPCTargetReached(
            npc_id="npc-clearing-caretaker",
            target_id="player",
        )
    )


def test_draw_renders_spatial_content_and_player(
    monkeypatch,
) -> None:
    surface = Mock(spec=pygame.Surface)
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    wall = Entity(
        entity_id="wall",
        position=pygame.Vector2(160.0, 64.0),
        size=pygame.Vector2(32.0, 48.0),
    )
    inactive_wall = Entity(
        entity_id="inactive-wall",
        position=pygame.Vector2(224.0, 64.0),
        size=pygame.Vector2(32.0, 48.0),
        active=False,
    )
    active_enemy = Enemy(
        Entity(
            entity_id="enemy-active",
            position=pygame.Vector2(272.0, 160.0),
            size=pygame.Vector2(32.0, 32.0),
        ),
        health=2,
    )
    inactive_enemy = Enemy(
        Entity(
            entity_id="enemy-inactive",
            position=pygame.Vector2(320.0, 160.0),
            size=pygame.Vector2(32.0, 32.0),
            active=False,
        ),
        health=2,
    )
    active_npc = NPC(
        name="Guide",
        entity=Entity(
            entity_id="npc-active",
            position=pygame.Vector2(352.0, 160.0),
            size=pygame.Vector2(24.0, 32.0),
        ),
        dialogue_lines=("Welcome, traveler!",),
    )
    inactive_npc = NPC(
        name="Inactive Guide",
        entity=Entity(
            entity_id="npc-inactive",
            position=pygame.Vector2(384.0, 160.0),
            size=pygame.Vector2(24.0, 32.0),
            active=False,
        ),
        dialogue_lines=("You should not see this.",),
    )
    active_collectible = Entity(
        entity_id="collectible-active",
        position=pygame.Vector2(120.0, 96.0),
        size=pygame.Vector2(12.0, 12.0),
    )
    inactive_collectible = Entity(
        entity_id="collectible-inactive",
        position=pygame.Vector2(136.0, 96.0),
        size=pygame.Vector2(12.0, 12.0),
        active=False,
    )
    active_exit = MapExit(
        entity=Entity(
            entity_id="exit-active",
            position=pygame.Vector2(416.0, 144.0),
            size=pygame.Vector2(32.0, 80.0),
        ),
        destination_map_id="clearing",
        destination_position=(128.0, 320.0),
    )
    inactive_exit = MapExit(
        entity=Entity(
            entity_id="exit-inactive",
            position=pygame.Vector2(464.0, 144.0),
            size=pygame.Vector2(32.0, 80.0),
            active=False,
        ),
        destination_map_id="clearing",
        destination_position=(128.0, 320.0),
    )
    score_font = Mock(spec=pygame.font.Font)
    session_score.value = 200
    font_cache.load.return_value = score_font
    draw_text = Mock()
    draw_rect = Mock()
    player_idle_animation = Mock(spec=Animation)
    player_idle_frame = Mock(spec=pygame.Surface)
    player_idle_animation.current_frame = player_idle_frame
    guide_objective = GuideObjective(total_items=2)

    monkeypatch.setattr(gameplay_scene, "draw_text", draw_text)
    monkeypatch.setattr(pygame.draw, "rect", draw_rect)

    scene = _create_gameplay_scene(
        font_cache=font_cache,
        session_score=session_score,
        walls=(wall, inactive_wall),
        enemies=(active_enemy, inactive_enemy),
        npcs=(active_npc, inactive_npc),
        collectibles=(active_collectible, inactive_collectible),
        player_idle_animation=player_idle_animation,
        guide_objective=guide_objective,
        exits=(active_exit, inactive_exit),
    )

    scene.draw(surface)

    font_cache.load.assert_called_once_with(
        SCORE_FONT_PATH,
        SCORE_FONT_SIZE,
    )
    assert draw_text.call_args_list == [
        call(
            surface,
            "Score: 200",
            score_font,
            SCORE_COLOR,
            center=SCORE_CENTER,
        ),
        call(
            surface,
            "Health: 3",
            score_font,
            HEALTH_COLOR,
            center=HEALTH_CENTER,
        ),
        call(
            surface,
            "Objective: Talk to the Guide",
            score_font,
            OBJECTIVE_COLOR,
            center=OBJECTIVE_CENTER,
        ),
    ]
    surface.fill.assert_called_once_with(TEST_BACKGROUND_COLOR)
    assert draw_rect.call_args_list == [
        call(
            surface,
            WALL_COLOR,
            pygame.Rect(160, 64, 32, 48),
        ),
        call(
            surface,
            ENEMY_COLOR,
            pygame.Rect(272, 160, 32, 32),
        ),
        call(
            surface,
            NPC_COLOR,
            pygame.Rect(352, 160, 24, 32),
        ),
        call(
            surface,
            COLLECTIBLE_COLOR,
            pygame.Rect(120, 96, 12, 12),
        ),
        call(
            surface,
            EXIT_COLOR,
            pygame.Rect(416, 144, 32, 80),
        ),
    ]
    surface.blit.assert_called_once_with(
        player_idle_frame,
        pygame.Rect(100, 80, 24, 24),
    )


def test_draw_flashes_enemy_after_non_fatal_damage(
    monkeypatch,
) -> None:
    surface = Mock(spec=pygame.Surface)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.side_effect = (
        False,
        False,
        True,
        False,
        False,
        False,
    )
    enemy = Enemy(
        entity=Entity(
            entity_id="enemy",
            position=pygame.Vector2(124.0, 80.0),
            size=pygame.Vector2(16.0, 16.0),
        ),
        health=2,
    )
    draw_rect = Mock()
    player_collection_animation = Mock(spec=Animation)
    player_collection_animation.finished = False
    player_attack_animation = Mock(spec=Animation)
    player_attack_animation.finished = False

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2()),
    )
    monkeypatch.setattr(
        gameplay_scene, "move_entity", Mock(return_value=pygame.Vector2())
    )
    monkeypatch.setattr(gameplay_scene, "draw_text", Mock())
    monkeypatch.setattr(pygame.draw, "rect", draw_rect)

    scene = _create_gameplay_scene(
        input_state=input_state,
        enemies=(enemy,),
        player_collection_animation=player_collection_animation,
        player_attack_animation=player_attack_animation,
    )

    scene.update(0.016)
    scene.draw(surface)

    draw_rect.assert_called_once_with(
        surface,
        ENEMY_HIT_COLOR,
        pygame.Rect(124, 80, 16, 16),
    )

    draw_rect.reset_mock()

    scene.update(ENEMY_HIT_DURATION)
    scene.draw(surface)

    draw_rect.assert_called_once_with(
        surface,
        ENEMY_COLOR,
        pygame.Rect(124, 80, 16, 16),
    )


def test_update_deactivates_overlapping_collectible_and_reports_event_once(
    monkeypatch,
) -> None:
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    overlapping = Entity(
        entity_id="collectible-overlapping",
        position=pygame.Vector2(108.0, 88.0),
        size=pygame.Vector2(8.0, 8.0),
    )
    distant = Entity(
        entity_id="collectible-distant",
        position=pygame.Vector2(240.0, 160.0),
        size=pygame.Vector2(8.0, 8.0),
    )

    on_item_collected = Mock()
    player_idle_animation = Mock(spec=Animation)
    player_movement_animation = Mock(spec=Animation)
    player_collection_animation = Mock(spec=Animation)
    player_collection_animation.finished = False

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2()),
    )
    monkeypatch.setattr(
        gameplay_scene, "move_entity", Mock(return_value=pygame.Vector2())
    )

    scene = _create_gameplay_scene(
        input_state=input_state,
        collectibles=(overlapping, distant),
        on_item_collected=on_item_collected,
        player_idle_animation=player_idle_animation,
        player_movement_animation=player_movement_animation,
        player_collection_animation=player_collection_animation,
    )

    scene.update(0.016)
    scene.update(0.016)

    on_item_collected.assert_called_once_with(
        ItemCollected(item_id=overlapping.entity_id)
    )
    assert not overlapping.active
    assert distant.active
    player_collection_animation.reset.assert_called_once_with()
    assert player_collection_animation.update.call_args_list == [
        call(0.016),
        call(0.016),
    ]
    player_idle_animation.update.assert_not_called()
    player_movement_animation.update.assert_not_called()


def test_update_resets_animation_when_movement_state_changes(
    monkeypatch,
) -> None:
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    player_idle_animation = Mock(spec=Animation)
    player_movement_animation = Mock(spec=Animation)

    movement_axis = Mock(
        side_effect=(
            pygame.Vector2(1.0, 0.0),
            pygame.Vector2(),
        )
    )

    monkeypatch.setattr(gameplay_scene, "movement_axis", movement_axis)
    monkeypatch.setattr(
        gameplay_scene, "move_entity", Mock(return_value=pygame.Vector2())
    )

    scene = _create_gameplay_scene(
        input_state=input_state,
        player_idle_animation=player_idle_animation,
        player_movement_animation=player_movement_animation,
    )

    scene.update(0.1)
    scene.update(0.2)

    player_movement_animation.reset.assert_called_once_with()
    player_movement_animation.update.assert_called_once_with(0.1)
    player_idle_animation.reset.assert_called_once_with()
    player_idle_animation.update.assert_called_once_with(0.2)


def test_update_returns_to_movement_after_collection_finished(
    monkeypatch,
) -> None:
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    collectible = Entity(
        entity_id="collectible",
        position=pygame.Vector2(108.0, 88.0),
        size=pygame.Vector2(8.0, 8.0),
    )
    player_idle_animation = Mock(spec=Animation)
    player_movement_animation = Mock(spec=Animation)
    player_collection_animation = Mock(spec=Animation)
    player_collection_animation.finished = False

    movement_axis = Mock(
        side_effect=(
            pygame.Vector2(),
            pygame.Vector2(1.0, 0.0),
        )
    )

    def finish_collection_animation(delta_time: float) -> None:
        assert delta_time == 0.1
        player_collection_animation.finished = True

    player_collection_animation.update.side_effect = finish_collection_animation

    monkeypatch.setattr(gameplay_scene, "movement_axis", movement_axis)
    monkeypatch.setattr(
        gameplay_scene, "move_entity", Mock(return_value=pygame.Vector2())
    )

    scene = _create_gameplay_scene(
        input_state=input_state,
        collectibles=(collectible,),
        player_idle_animation=player_idle_animation,
        player_movement_animation=player_movement_animation,
        player_collection_animation=player_collection_animation,
    )

    scene.update(0.1)
    scene.update(0.2)

    player_collection_animation.reset.assert_called_once_with()
    player_collection_animation.update.assert_called_once_with(0.1)
    player_movement_animation.reset.assert_called_once_with()
    player_movement_animation.update.assert_called_once_with(0.2)
    player_idle_animation.update.assert_not_called()


def test_update_destroys_nearby_destructible_on_attack(
    monkeypatch,
) -> None:
    input_state = Mock(spec=InputState)
    input_state.is_pressed.side_effect = (
        False,
        False,
        True,
        False,
        False,
        False,
    )
    player = Player(
        entity=Entity(
            entity_id="player",
            position=pygame.Vector2(100.0, 80.0),
            size=pygame.Vector2(24.0, 24.0),
        ),
        health=3,
    )
    move_entity = Mock(return_value=pygame.Vector2())
    nearby_obstacle = Entity(
        entity_id="destructible-nearby",
        position=pygame.Vector2(124.0, 80.0),
        size=pygame.Vector2(16.0, 16.0),
    )
    distant_obstacle = Entity(
        entity_id="destructible-distant",
        position=pygame.Vector2(240.0, 160.0),
        size=pygame.Vector2(16.0, 16.0),
    )
    on_obstacle_destroyed = Mock()
    player_idle_animation = Mock(spec=Animation)
    player_movement_animation = Mock(spec=Animation)
    player_collection_animation = Mock(spec=Animation)
    player_collection_animation.finished = False
    player_attack_animation = Mock(spec=Animation)
    player_attack_animation.finished = False

    monkeypatch.setattr(
        gameplay_scene, "movement_axis", Mock(return_value=pygame.Vector2())
    )
    monkeypatch.setattr(gameplay_scene, "move_entity", move_entity)

    scene = _create_gameplay_scene(
        input_state=input_state,
        player=player,
        walls=(nearby_obstacle, distant_obstacle),
        destructible_obstacles=(
            nearby_obstacle,
            distant_obstacle,
        ),
        on_obstacle_destroyed=on_obstacle_destroyed,
        player_idle_animation=player_idle_animation,
        player_movement_animation=player_movement_animation,
        player_collection_animation=player_collection_animation,
        player_attack_animation=player_attack_animation,
    )

    scene.update(0.016)
    scene.update(0.016)

    player_attack_animation.reset.assert_called_once_with()
    assert player_attack_animation.update.call_args_list == [
        call(0.016),
        call(0.016),
    ]
    player_idle_animation.update.assert_not_called()
    player_movement_animation.update.assert_not_called()
    player_collection_animation.update.assert_not_called()
    assert input_state.is_pressed.call_args_list == [
        call(GameAction.PAUSE),
        call(GameAction.INTERACT),
        call(GameAction.ATTACK),
        call(GameAction.PAUSE),
        call(GameAction.INTERACT),
        call(GameAction.ATTACK),
    ]
    assert move_entity.call_args_list == [
        call(
            player.entity,
            pygame.Vector2(),
            (nearby_obstacle.bounds, distant_obstacle.bounds),
        ),
        call(
            player.entity,
            pygame.Vector2(),
            (distant_obstacle.bounds,),
        ),
    ]
    on_obstacle_destroyed.assert_called_once_with(
        ObstacleDestroyed(obstacle_id=nearby_obstacle.entity_id)
    )
    assert not nearby_obstacle.active
    assert distant_obstacle.active


def test_update_damages_and_defeats_nearby_enemy_on_attack(
    monkeypatch,
) -> None:
    input_state = Mock(spec=InputState)
    input_state.is_pressed.side_effect = (
        False,
        False,
        True,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        True,
    )
    move_entity = Mock(return_value=pygame.Vector2())
    nearby_enemy = Enemy(
        Entity(
            entity_id="enemy-nearby",
            position=pygame.Vector2(124.0, 80.0),
            size=pygame.Vector2(16.0, 16.0),
        ),
        health=2,
    )

    distant_enemy = Enemy(
        Entity(
            entity_id="enemy-distant",
            position=pygame.Vector2(240.0, 160.0),
            size=pygame.Vector2(16.0, 16.0),
        ),
        health=2,
    )
    on_enemy_defeated = Mock()
    player_idle_animation = Mock(spec=Animation)
    player_movement_animation = Mock(spec=Animation)
    player_collection_animation = Mock(spec=Animation)
    player_collection_animation.finished = False
    player_attack_animation = Mock(spec=Animation)
    player_attack_animation.finished = False

    monkeypatch.setattr(
        gameplay_scene, "movement_axis", Mock(return_value=pygame.Vector2())
    )
    monkeypatch.setattr(gameplay_scene, "move_entity", move_entity)

    scene = _create_gameplay_scene(
        input_state=input_state,
        enemies=(nearby_enemy, distant_enemy),
        on_enemy_defeated=on_enemy_defeated,
        player_idle_animation=player_idle_animation,
        player_movement_animation=player_movement_animation,
        player_collection_animation=player_collection_animation,
        player_attack_animation=player_attack_animation,
    )

    scene.update(0.016)

    assert nearby_enemy.health == 1
    assert nearby_enemy.entity.active
    on_enemy_defeated.assert_not_called()

    scene.update(0.016)
    scene.update(0.016)
    scene.update(0.016)

    player_idle_animation.update.assert_not_called()
    player_movement_animation.update.assert_not_called()
    player_collection_animation.update.assert_not_called()
    assert input_state.is_pressed.call_args_list == [
        call(GameAction.PAUSE),
        call(GameAction.INTERACT),
        call(GameAction.ATTACK),
        call(GameAction.PAUSE),
        call(GameAction.INTERACT),
        call(GameAction.ATTACK),
        call(GameAction.PAUSE),
        call(GameAction.INTERACT),
        call(GameAction.ATTACK),
        call(GameAction.PAUSE),
        call(GameAction.INTERACT),
        call(GameAction.ATTACK),
    ]
    on_enemy_defeated.assert_called_once_with(
        EnemyDefeated(enemy_id=nearby_enemy.entity.entity_id)
    )
    assert nearby_enemy.health == 0
    assert not nearby_enemy.entity.active
    assert distant_enemy.health == 2
    assert distant_enemy.entity.active


def test_update_returns_to_movement_after_attack_finished(
    monkeypatch,
) -> None:
    input_state = Mock(spec=InputState)
    input_state.is_pressed.side_effect = (
        False,
        False,
        True,
        False,
        False,
        False,
    )
    player_idle_animation = Mock(spec=Animation)
    player_movement_animation = Mock(spec=Animation)
    player_collection_animation = Mock(spec=Animation)
    player_collection_animation.finished = False
    player_attack_animation = Mock(spec=Animation)
    player_attack_animation.finished = False

    movement_axis = Mock(
        side_effect=(
            pygame.Vector2(),
            pygame.Vector2(1.0, 0.0),
        )
    )

    def finish_attack_animation(delta_time: float) -> None:
        assert delta_time == 0.1
        player_attack_animation.finished = True

    player_attack_animation.update.side_effect = finish_attack_animation

    monkeypatch.setattr(gameplay_scene, "movement_axis", movement_axis)
    monkeypatch.setattr(
        gameplay_scene, "move_entity", Mock(return_value=pygame.Vector2())
    )

    scene = _create_gameplay_scene(
        input_state=input_state,
        player_idle_animation=player_idle_animation,
        player_movement_animation=player_movement_animation,
        player_collection_animation=player_collection_animation,
        player_attack_animation=player_attack_animation,
    )

    scene.update(0.1)
    scene.update(0.2)

    player_attack_animation.reset.assert_called_once_with()
    player_attack_animation.update.assert_called_once_with(0.1)
    player_movement_animation.reset.assert_called_once_with()
    player_movement_animation.update.assert_called_once_with(0.2)
    player_idle_animation.update.assert_not_called()
    player_collection_animation.update.assert_not_called()


def test_update_enemy_contact_damages_player_after_invulnerability(monkeypatch) -> None:
    player = Player(
        entity=Entity(
            entity_id="player",
            position=pygame.Vector2(100.0, 80.0),
            size=pygame.Vector2(24.0, 24.0),
        ),
        health=3,
    )
    enemy = Enemy(
        entity=Entity(
            entity_id="enemy",
            position=pygame.Vector2(
                player.entity.bounds.right,
                player.entity.position.y,
            ),
            size=pygame.Vector2(16.0, 16.0),
        ),
        health=2,
    )

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2()),
    )
    monkeypatch.setattr(
        gameplay_scene, "move_entity", Mock(return_value=pygame.Vector2())
    )

    scene = _create_gameplay_scene(
        player=player,
        enemies=(enemy,),
    )

    scene.update(0.016)

    assert ENEMY_CONTACT_REACH > 0.0
    assert player.health == 2
    assert player.entity.active

    scene.update(PLAYER_INVULNERABILITY_DURATION / 2.0)

    assert player.health == 2

    scene.update(PLAYER_INVULNERABILITY_DURATION / 2.0)

    assert player.health == 1
    assert player.entity.active


def test_update_reports_player_defeat_once_on_fatal_contact(monkeypatch) -> None:
    player = Player(
        entity=Entity(
            entity_id="player",
            position=pygame.Vector2(100.0, 80.0),
            size=pygame.Vector2(24.0, 24.0),
        ),
        health=1,
    )
    enemy = Enemy(
        entity=Entity(
            entity_id="enemy",
            position=pygame.Vector2(
                player.entity.bounds.right,
                player.entity.position.y,
            ),
            size=pygame.Vector2(16.0, 16.0),
        ),
        health=2,
    )
    on_player_defeated = Mock()
    move_entity = Mock(return_value=pygame.Vector2())

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2()),
    )
    monkeypatch.setattr(gameplay_scene, "move_entity", move_entity)

    scene = _create_gameplay_scene(
        player=player,
        on_player_defeated=on_player_defeated,
        enemies=(enemy,),
    )

    scene.update(0.016)
    scene.update(PLAYER_INVULNERABILITY_DURATION)

    move_entity.assert_called_once_with(
        player.entity,
        pygame.Vector2(),
        (enemy.entity.bounds,),
    )
    assert player.health == 0
    assert not player.entity.active
    on_player_defeated.assert_called_once_with(
        PlayerDefeated(player_id=player.entity.entity_id)
    )


def test_update_requests_pause_without_advancing_gameplay(monkeypatch) -> None:
    input_state = Mock(spec=InputState)
    input_state.is_pressed.side_effect = lambda action: action is GameAction.PAUSE
    on_pause_requested = Mock()
    movement_axis = Mock()
    move_entity = Mock(return_value=pygame.Vector2())
    player_idle_animation = Mock(spec=Animation)

    monkeypatch.setattr(gameplay_scene, "movement_axis", movement_axis)
    monkeypatch.setattr(gameplay_scene, "move_entity", move_entity)

    scene = _create_gameplay_scene(
        input_state=input_state,
        on_pause_requested=on_pause_requested,
        player_idle_animation=player_idle_animation,
    )

    scene.update(0.5)

    input_state.is_pressed.assert_called_once_with(GameAction.PAUSE)
    on_pause_requested.assert_called_once_with()
    movement_axis.assert_not_called()
    move_entity.assert_not_called()
    player_idle_animation.update.assert_not_called()


def test_update_interacts_with_nearby_active_npc_without_advancing_gameplay(
    monkeypatch,
) -> None:
    input_state = Mock(spec=InputState)
    input_state.is_pressed.side_effect = lambda action: action is GameAction.INTERACT
    nearby_npc = NPC(
        name="Guide",
        entity=Entity(
            entity_id="npc-nearby",
            position=pygame.Vector2(124.0, 80.0),
            size=pygame.Vector2(24.0, 32.0),
        ),
        dialogue_lines=("Welcome, traveler!",),
    )
    distant_npc = NPC(
        name="Distant guide",
        entity=Entity(
            entity_id="npc-distant",
            position=pygame.Vector2(320.0, 240.0),
            size=pygame.Vector2(24.0, 32.0),
        ),
        dialogue_lines=("Too far away.",),
    )
    on_npc_interacted = Mock()
    movement_axis = Mock()
    move_entity = Mock(return_value=pygame.Vector2())
    player_idle_animation = Mock(spec=Animation)

    monkeypatch.setattr(gameplay_scene, "movement_axis", movement_axis)
    monkeypatch.setattr(gameplay_scene, "move_entity", move_entity)

    scene = _create_gameplay_scene(
        input_state=input_state,
        npcs=(nearby_npc, distant_npc),
        on_npc_interacted=on_npc_interacted,
        player_idle_animation=player_idle_animation,
    )

    scene.update(0.5)

    assert input_state.is_pressed.call_args_list == [
        call(GameAction.PAUSE),
        call(GameAction.INTERACT),
    ]
    on_npc_interacted.assert_called_once_with(nearby_npc)
    movement_axis.assert_not_called()
    move_entity.assert_not_called()
    player_idle_animation.assert_not_called()


def test_update_does_not_interact_with_distant_npc(monkeypatch) -> None:
    input_state = Mock(spec=InputState)
    input_state.is_pressed.side_effect = lambda action: action is GameAction.INTERACT
    distant_npc = NPC(
        name="Distant guide",
        entity=Entity(
            entity_id="npc-distant",
            position=pygame.Vector2(320.0, 240.0),
            size=pygame.Vector2(24.0, 32.0),
        ),
        dialogue_lines=("Too far away.",),
    )
    on_npc_interacted = Mock()

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2()),
    )
    monkeypatch.setattr(
        gameplay_scene, "move_entity", Mock(return_value=pygame.Vector2())
    )

    scene = _create_gameplay_scene(
        input_state=input_state,
        npcs=(distant_npc,),
        on_npc_interacted=on_npc_interacted,
    )

    scene.update(0.016)

    on_npc_interacted.assert_not_called()


def test_update_reports_overlapping_map_exit(monkeypatch) -> None:
    map_exit = MapExit(
        entity=Entity(
            entity_id="exit-to-clearing",
            position=pygame.Vector2(100.0, 80.0),
            size=pygame.Vector2(32.0, 32.0),
        ),
        destination_map_id="clearing",
        destination_position=(128.0, 320.0),
    )
    on_map_exit_reached = Mock()

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2()),
    )
    monkeypatch.setattr(
        gameplay_scene, "move_entity", Mock(return_value=pygame.Vector2())
    )

    scene = _create_gameplay_scene(
        exits=(map_exit,),
        on_map_exit_reached=on_map_exit_reached,
    )

    scene.update(0.0)

    on_map_exit_reached.assert_called_once_with(map_exit)


def test_change_map_replaces_spatial_content(monkeypatch) -> None:
    surface = Mock(spec=pygame.Surface)
    player = Player(
        entity=Entity(
            entity_id="player",
            position=pygame.Vector2(64.0, 320.0),
            size=pygame.Vector2(24.0, 24.0),
        ),
        health=3,
    )
    old_exit = MapExit(
        entity=Entity(
            entity_id="old_exit",
            position=pygame.Vector2(64.0, 320.0),
            size=pygame.Vector2(32.0, 80.0),
        ),
        destination_map_id="old-destination",
        destination_position=(0.0, 0.0),
    )
    destination_map = create_clearing_map(player)
    on_map_exit_reached = Mock()

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2()),
    )
    monkeypatch.setattr(
        gameplay_scene, "move_entity", Mock(return_value=pygame.Vector2())
    )
    monkeypatch.setattr(gameplay_scene, "draw_text", Mock())
    monkeypatch.setattr(pygame.draw, "rect", Mock())

    scene = _create_gameplay_scene(
        player=player,
        exits=(old_exit,),
        on_map_exit_reached=on_map_exit_reached,
    )

    scene.change_map(destination_map)
    scene.update(0.0)
    scene.draw(surface)

    on_map_exit_reached.assert_called_once_with(destination_map.exits[0])
    surface.fill.assert_called_once_with(destination_map.background_color)
