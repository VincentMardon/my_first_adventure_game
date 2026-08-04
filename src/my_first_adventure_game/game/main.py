import pygame

WINDOW_SIZE = (1280, 720)
WINDOW_TITLE = "My First Adventure Game"
BACKGROUND_COLOR = (24, 28, 36)
FRAMES_PER_SECOND = 60


def main() -> None:
    pygame.init()

    try:
        screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)
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
