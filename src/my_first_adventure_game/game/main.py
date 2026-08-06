import pygame

from my_first_adventure_game.engine.application import Application, WindowConfig
from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.engine.scenes import SceneManager
from my_first_adventure_game.game.events import ItemCollected
from my_first_adventure_game.game.input import DEFAULT_KEYBOARD_BINDINGS
from my_first_adventure_game.game.levels import create_demo_map
from my_first_adventure_game.game.scenes import GameplayScene, TitleScene

WINDOW_CONFIG = WindowConfig(title="My First Adventure Game", size=(1280, 720))
FRAMES_PER_SECOND = 60


def main() -> None:
    """Compose the game services and start the application."""

    input_state = InputState(DEFAULT_KEYBOARD_BINDINGS)
    font_cache = FontCache(pygame)
    game_map = create_demo_map()

    def start_game() -> None:
        scene_manager.change_scene(gameplay_scene)

    initial_scene = TitleScene(
        font_cache,
        input_state,
        start_game,
    )
    scene_manager = SceneManager(initial_scene)

    def handle_item_collected(_event: ItemCollected) -> None:
        return None

    gameplay_scene = GameplayScene(
        input_state,
        game_map.player,
        game_map.walls,
        game_map.collectibles,
        handle_item_collected,
    )
    application = Application(
        window_config=WINDOW_CONFIG,
        scene_manager=scene_manager,
        input_processor=input_state,
        frames_per_second=FRAMES_PER_SECOND,
    )

    application.run()
