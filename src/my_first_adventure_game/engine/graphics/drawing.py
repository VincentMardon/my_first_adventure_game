import pygame


def draw_text(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
    *,
    center: tuple[int, int],
) -> pygame.Rect:
    """Render centered text and return its destination rectangle."""
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=center)
    surface.blit(rendered_text, text_rect)

    return text_rect
