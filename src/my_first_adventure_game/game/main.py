import pygame

from my_first_adventure_game.engine.application import Application, WindowConfig
from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.graphics import Animation
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.engine.scenes import SceneManager
from my_first_adventure_game.game.events import ItemCollected
from my_first_adventure_game.game.input import DEFAULT_KEYBOARD_BINDINGS
from my_first_adventure_game.game.levels import create_demo_map
from my_first_adventure_game.game.scenes import GameplayScene, TitleScene
from my_first_adventure_game.game.scoring import (
    SessionScore,
    item_collection_points,
)

WINDOW_CONFIG = WindowConfig(title="My First Adventure Game", size=(1280, 720))
FRAMES_PER_SECOND = 60
PLAYER_FRAME_SIZE = (32, 32)
PLAYER_IDLE_COLORS = (
    (224, 196, 96),
    (240, 212, 112),
)
PLAYER_MOVEMENT_COLORS = (
    (240, 144, 72),
    (255, 184, 88),
)
PLAYER_IDLE_FRAME_DURATION = 0.4
PLAYER_MOVEMENT_FRAME_DURATION = 0.15
PLAYER_COLLECTION_COLORS = (
    (248, 248, 248),
    (112, 240, 160),
)
PLAYER_COLLECTION_FRAME_DURATION = 0.1


def main() -> None:
    """Compose the game services and start the application."""

    input_state = InputState(DEFAULT_KEYBOARD_BINDINGS)
    font_cache = FontCache(pygame)
    game_map = create_demo_map()
    session_score = SessionScore()
    player_idle_frames = tuple(
        pygame.Surface(PLAYER_FRAME_SIZE) for _ in PLAYER_IDLE_COLORS
    )
    player_movement_frames = tuple(
        pygame.Surface(PLAYER_FRAME_SIZE) for _ in PLAYER_MOVEMENT_COLORS
    )
    player_collection_frames = tuple(
        pygame.Surface(PLAYER_FRAME_SIZE) for _ in PLAYER_COLLECTION_COLORS
    )

    for frame, color in zip(
        player_idle_frames,
        PLAYER_IDLE_COLORS,
        strict=True,
    ):
        frame.fill(color)

    for frame, color in zip(
        player_movement_frames,
        PLAYER_MOVEMENT_COLORS,
        strict=True,
    ):
        frame.fill(color)

    for frame, color in zip(
        player_collection_frames, PLAYER_COLLECTION_COLORS, strict=True
    ):
        frame.fill(color)

    player_idle_animation = Animation(
        frames=player_idle_frames,
        frame_duration=PLAYER_IDLE_FRAME_DURATION,
    )
    player_movement_animation = Animation(
        frames=player_movement_frames,
        frame_duration=PLAYER_MOVEMENT_FRAME_DURATION,
    )
    player_collection_animation = Animation(
        frames=player_collection_frames,
        frame_duration=PLAYER_COLLECTION_FRAME_DURATION,
        loop=False,
    )

    def start_game() -> None:
        scene_manager.change_scene(gameplay_scene)

    initial_scene = TitleScene(
        font_cache,
        input_state,
        start_game,
    )
    scene_manager = SceneManager(initial_scene)

    def handle_item_collected(event: ItemCollected) -> None:
        session_score.add(item_collection_points(event))

    gameplay_scene = GameplayScene(
        input_state,
        font_cache,
        session_score,
        game_map.player,
        game_map.walls,
        game_map.collectibles,
        handle_item_collected,
        player_idle_animation,
        player_movement_animation,
        player_collection_animation,
    )
    application = Application(
        window_config=WINDOW_CONFIG,
        scene_manager=scene_manager,
        input_processor=input_state,
        frames_per_second=FRAMES_PER_SECOND,
    )

    application.run()
