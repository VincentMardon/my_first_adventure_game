from unittest.mock import Mock, call

import pygame

from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.engine.world import Entity
from my_first_adventure_game.game.events import ItemCollected
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scenes import gameplay_scene
from my_first_adventure_game.game.scenes.gameplay_scene import (
    BACKGROUND_COLOR,
    COLLECTIBLE_COLOR,
    PLAYER_COLOR,
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

    movement_axis = Mock(return_value=pygame.Vector2(0.6, 0.8))
    move_entity = Mock()

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
    )

    scene.update(0.5)

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
    score_font = Mock(spec=pygame.font.Font)
    session_score.value = 200
    font_cache.load.return_value = score_font
    draw_text = Mock()
    draw_rect = Mock()

    monkeypatch.setattr(gameplay_scene, "draw_text", draw_text)
    monkeypatch.setattr(pygame.draw, "rect", draw_rect)

    scene = GameplayScene(
        input_state=input_state,
        font_cache=font_cache,
        session_score=session_score,
        player=player,
        walls=(wall,),
        collectibles=(active_collectible, inactive_collectible),
        on_item_collected=on_item_collected,
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
        call(
            surface,
            PLAYER_COLOR,
            pygame.Rect(100, 80, 24, 24),
        ),
    ]


def test_update_deactivates_overlapping_collectible_and_reports_event_once(
    monkeypatch,
) -> None:
    input_state = Mock(spec=InputState)
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
    )

    scene.update(0.016)
    scene.update(0.016)

    on_item_collected.assert_called_once_with(
        ItemCollected(item_id=overlapping.entity_id)
    )
    assert not overlapping.active
    assert distant.active
