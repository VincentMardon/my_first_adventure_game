from unittest.mock import Mock, call

import pygame

from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.engine.world import Entity
from my_first_adventure_game.game.input import GameAction
from my_first_adventure_game.game.scenes import gameplay_scene
from my_first_adventure_game.game.scenes.gameplay_scene import (
    BACKGROUND_COLOR,
    PLAYER_COLOR,
    PLAYER_SPEED,
    WALL_COLOR,
    GameplayScene,
)


def test_update_moves_player_from_directional_actions(monkeypatch) -> None:
    input_state = Mock(spec=InputState)
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

    movement_axis = Mock(return_value=pygame.Vector2(0.6, 0.8))
    move_entity = Mock()

    monkeypatch.setattr(gameplay_scene, "movement_axis", movement_axis)
    monkeypatch.setattr(gameplay_scene, "move_entity", move_entity)

    scene = GameplayScene(
        input_state=input_state,
        player=player,
        walls=(wall,),
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


def test_draw_renders_background_walls_and_player(monkeypatch) -> None:
    surface = Mock(spec=pygame.Surface)
    input_state = Mock(spec=InputState)
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
    draw_rect = Mock()

    monkeypatch.setattr(pygame.draw, "rect", draw_rect)

    scene = GameplayScene(
        input_state=input_state,
        player=player,
        walls=(wall,),
    )

    scene.draw(surface)

    surface.fill.assert_called_once_with(BACKGROUND_COLOR)
    assert draw_rect.call_args_list == [
        call(
            surface,
            WALL_COLOR,
            pygame.Rect(160, 64, 32, 48),
        ),
        call(
            surface,
            PLAYER_COLOR,
            pygame.Rect(100, 80, 24, 24),
        ),
    ]
