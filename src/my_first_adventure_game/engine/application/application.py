import pygame

from my_first_adventure_game.engine.application.window_config import WindowConfig
from my_first_adventure_game.engine.scenes import SceneManager


class Application:
    def __init__(
        self,
        window_config: WindowConfig,
        scene_manager: SceneManager,
        *,
        frames_per_second: int,
    ) -> None:
        self._window_config = window_config
        self._scene_manager = scene_manager
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

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    else:
                        self._scene_manager.handle_event(event)

                self._scene_manager.update(delta_time)
                self._scene_manager.draw(surface)
                pygame.display.flip()
        finally:
            pygame.quit()
