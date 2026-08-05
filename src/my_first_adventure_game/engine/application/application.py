import pygame

from my_first_adventure_game.engine.application.window_config import WindowConfig
from my_first_adventure_game.engine.input import InputProcessor
from my_first_adventure_game.engine.scenes import SceneManager


class Application:
    def __init__(
        self,
        window_config: WindowConfig,
        scene_manager: SceneManager,
        input_processor: InputProcessor,
        *,
        frames_per_second: int,
    ) -> None:
        self._window_config = window_config
        self._scene_manager = scene_manager
        self._input_processor = input_processor
        self._frames_per_second = frames_per_second

    def run(self) -> None:
        pygame.init()

        try:
            surface = pygame.display.set_mode(self._window_config.size)
            pygame.display.set_caption(self._window_config.title)
            clock = pygame.time.Clock()
            running = True

            while running:
                delta_time = clock.tick(self._frames_per_second) / 1000
                self._input_processor.start_frame()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    else:
                        self._input_processor.handle_event(event)
                        self._scene_manager.handle_event(event)

                self._scene_manager.update(delta_time)
                self._scene_manager.draw(surface)
                pygame.display.flip()
        finally:
            pygame.quit()
