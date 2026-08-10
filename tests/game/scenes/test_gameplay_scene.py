from unittest.mock import Mock, call

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.graphics import Animation
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.engine.world import Entity
from my_first_adventure_game.game.events import (
    ItemCollected,
    ObstacleDestroyed,
)
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scenes import gameplay_scene
from my_first_adventure_game.game.scenes.gameplay_scene import (
    BACKGROUND_COLOR,
    COLLECTIBLE_COLOR,
    PLAYER_SPEED,
    SCORE_CENTER,
    SCORE_COLOR,
    SCORE_FONT_PATH,
    SCORE_FONT_SIZE,
    WALL_COLOR,
    GameplayScene,
)
from my_first_adventure_game.game.scoring import SessionScore


def test_update_moves_player_from_directional_actions(monkeypatch) -> None:
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    player = Entity(
        entity_id="player",
        position=pygame.Vector2(100.0, 80.0),
        size=pygame.Vector2(24.0, 24.0),
    )
    wall = Entity(
        entity_id="wall",
        position=pygame.Vector2(200.0, 80.0),
        size=pygame.Vector2(32.0, 32.0),
    )
    on_item_collected = Mock()
    on_obstacle_destroyed = Mock()

    movement_axis = Mock(return_value=pygame.Vector2(0.6, 0.8))
    move_entity = Mock()

    player_idle_animation = Mock(spec=Animation)
    player_movement_animation = Mock(spec=Animation)
    player_collection_animation = Mock(spec=Animation)
    player_collection_animation.finished = False

    monkeypatch.setattr(gameplay_scene, "movement_axis", movement_axis)
    monkeypatch.setattr(gameplay_scene, "move_entity", move_entity)

    scene = GameplayScene(
        input_state=input_state,
        font_cache=font_cache,
        session_score=session_score,
        player=player,
        walls=(wall,),
        collectibles=(),
        on_item_collected=on_item_collected,
        destructible_obstacles=(),
        on_obstacle_destroyed=on_obstacle_destroyed,
        player_idle_animation=player_idle_animation,
        player_movement_animation=player_movement_animation,
        player_collection_animation=player_collection_animation,
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
        player,
        pygame.Vector2(0.6, 0.8) * PLAYER_SPEED * 0.5,
        (wall.bounds,),
    )


def test_draw_renders_background_walls_active_collectibles_and_player(
    monkeypatch,
) -> None:
    surface = Mock(spec=pygame.Surface)
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    player = Entity(
        entity_id="player",
        position=pygame.Vector2(100.0, 80.0),
        size=pygame.Vector2(24.0, 24.0),
    )
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
    on_item_collected = Mock()
    on_obstacle_destroyed = Mock()
    score_font = Mock(spec=pygame.font.Font)
    session_score.value = 200
    font_cache.load.return_value = score_font
    draw_text = Mock()
    draw_rect = Mock()
    player_idle_animation = Mock(spec=Animation)
    player_movement_animation = Mock(spec=Animation)
    player_idle_frame = Mock(spec=pygame.Surface)
    player_idle_animation.current_frame = player_idle_frame
    player_collection_animation = Mock(spec=Animation)
    player_collection_animation.finished = False

    monkeypatch.setattr(gameplay_scene, "draw_text", draw_text)
    monkeypatch.setattr(pygame.draw, "rect", draw_rect)

    scene = GameplayScene(
        input_state=input_state,
        font_cache=font_cache,
        session_score=session_score,
        player=player,
        walls=(wall, inactive_wall),
        collectibles=(active_collectible, inactive_collectible),
        on_item_collected=on_item_collected,
        destructible_obstacles=(),
        on_obstacle_destroyed=on_obstacle_destroyed,
        player_idle_animation=player_idle_animation,
        player_movement_animation=player_movement_animation,
        player_collection_animation=player_collection_animation,
    )

    scene.draw(surface)

    font_cache.load.assert_called_once_with(
        SCORE_FONT_PATH,
        SCORE_FONT_SIZE,
    )
    draw_text.assert_called_once_with(
        surface,
        "Score: 200",
        score_font,
        SCORE_COLOR,
        center=SCORE_CENTER,
    )
    surface.fill.assert_called_once_with(BACKGROUND_COLOR)
    assert draw_rect.call_args_list == [
        call(
            surface,
            WALL_COLOR,
            pygame.Rect(160, 64, 32, 48),
        ),
        call(
            surface,
            COLLECTIBLE_COLOR,
            pygame.Rect(120, 96, 12, 12),
        ),
    ]
    surface.blit.assert_called_once_with(
        player_idle_frame,
        pygame.Rect(100, 80, 24, 24),
    )


def test_update_deactivates_overlapping_collectible_and_reports_event_once(
    monkeypatch,
) -> None:
    input_state = Mock(spec=InputState)
    input_state.is_pressed.return_value = False
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    player = Entity(
        entity_id="player",
        position=pygame.Vector2(100.0, 80.0),
        size=pygame.Vector2(24.0, 24.0),
    )
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
    on_obstacle_destroyed = Mock()
    player_idle_animation = Mock(spec=Animation)
    player_movement_animation = Mock(spec=Animation)
    player_collection_animation = Mock(spec=Animation)
    player_collection_animation.finished = False

    monkeypatch.setattr(
        gameplay_scene,
        "movement_axis",
        Mock(return_value=pygame.Vector2()),
    )
    monkeypatch.setattr(gameplay_scene, "move_entity", Mock())

    scene = GameplayScene(
        input_state=input_state,
        font_cache=font_cache,
        session_score=session_score,
        player=player,
        walls=(),
        collectibles=(overlapping, distant),
        on_item_collected=on_item_collected,
        destructible_obstacles=(),
        on_obstacle_destroyed=on_obstacle_destroyed,
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
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    player = Entity(
        entity_id="player",
        position=pygame.Vector2(100.0, 80.0),
        size=pygame.Vector2(24.0, 24.0),
    )
    on_item_collected = Mock()
    on_obstacle_destroyed = Mock()
    player_idle_animation = Mock(spec=Animation)
    player_movement_animation = Mock(spec=Animation)
    player_collection_animation = Mock(spec=Animation)
    player_collection_animation.finished = False

    movement_axis = Mock(
        side_effect=(
            pygame.Vector2(1.0, 0.0),
            pygame.Vector2(),
        )
    )

    monkeypatch.setattr(gameplay_scene, "movement_axis", movement_axis)
    monkeypatch.setattr(gameplay_scene, "move_entity", Mock())

    scene = GameplayScene(
        input_state=input_state,
        font_cache=font_cache,
        session_score=session_score,
        player=player,
        walls=(),
        collectibles=(),
        on_item_collected=on_item_collected,
        destructible_obstacles=(),
        on_obstacle_destroyed=on_obstacle_destroyed,
        player_idle_animation=player_idle_animation,
        player_movement_animation=player_movement_animation,
        player_collection_animation=player_collection_animation,
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
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    player = Entity(
        entity_id="player",
        position=pygame.Vector2(100.0, 80.0),
        size=pygame.Vector2(24.0, 24.0),
    )
    collectible = Entity(
        entity_id="collectible",
        position=pygame.Vector2(108.0, 88.0),
        size=pygame.Vector2(8.0, 8.0),
    )
    on_item_collected = Mock()
    on_obstacle_destroyed = Mock()
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
    monkeypatch.setattr(gameplay_scene, "move_entity", Mock())

    scene = GameplayScene(
        input_state=input_state,
        font_cache=font_cache,
        session_score=session_score,
        player=player,
        walls=(),
        collectibles=(collectible,),
        on_item_collected=on_item_collected,
        destructible_obstacles=(),
        on_obstacle_destroyed=on_obstacle_destroyed,
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
    input_state.is_pressed.side_effect = (True, False)
    font_cache = Mock(spec=FontCache)
    session_score = Mock(spec=SessionScore)
    player = Entity(
        entity_id="player",
        position=pygame.Vector2(100.0, 80.0),
        size=pygame.Vector2(24.0, 24.0),
    )
    move_entity = Mock()
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
    on_item_collected = Mock()
    on_obstacle_destroyed = Mock()
    player_idle_animation = Mock(spec=Animation)
    player_movement_animation = Mock(spec=Animation)
    player_collection_animation = Mock(spec=Animation)
    player_collection_animation.finished = False

    monkeypatch.setattr(
        gameplay_scene, "movement_axis", Mock(return_value=pygame.Vector2())
    )
    monkeypatch.setattr(gameplay_scene, "move_entity", move_entity)

    scene = GameplayScene(
        input_state=input_state,
        font_cache=font_cache,
        session_score=session_score,
        player=player,
        walls=(nearby_obstacle, distant_obstacle),
        collectibles=(),
        destructible_obstacles=(
            nearby_obstacle,
            distant_obstacle,
        ),
        on_item_collected=on_item_collected,
        on_obstacle_destroyed=on_obstacle_destroyed,
        player_idle_animation=player_idle_animation,
        player_movement_animation=player_movement_animation,
        player_collection_animation=player_collection_animation,
    )

    scene.update(0.016)
    scene.update(0.016)

    assert input_state.is_pressed.call_args_list == [
        call(GameAction.ATTACK),
        call(GameAction.ATTACK),
    ]
    assert move_entity.call_args_list == [
        call(
            player,
            pygame.Vector2(),
            (nearby_obstacle.bounds, distant_obstacle.bounds),
        ),
        call(
            player,
            pygame.Vector2(),
            (distant_obstacle.bounds,),
        ),
    ]
    on_obstacle_destroyed.assert_called_once_with(
        ObstacleDestroyed(obstacle_id=nearby_obstacle.entity_id)
    )
    assert not nearby_obstacle.active
    assert distant_obstacle.active
