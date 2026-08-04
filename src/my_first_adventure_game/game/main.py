import pygame

from my_first_adventure_game.engine.application import WindowConfig

WINDOW_CONFIG = WindowConfig(title="My First Adventure Game", size=(1280, 720))
BACKGROUND_COLOR = (24, 28, 36)
FRAMES_PER_SECOND = 60


def main() -> None:
    pygame.init()

    try:
        screen = pygame.display.set_mode(WINDOW_CONFIG.size)
        pygame.display.set_caption(WINDOW_CONFIG.title)
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(BACKGROUND_COLOR)
            pygame.display.flip()
            clock.tick(FRAMES_PER_SECOND)
    finally:
        pygame.quit()
