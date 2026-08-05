from unittest.mock import Mock

import pygame

from my_first_adventure_game.engine.graphics import draw_text


def test_draw_text_renders_and_centers_text_on_surface() -> None:
    surface = Mock(spec=pygame.Surface)
    font = Mock(spec=pygame.font.Font)
    rendered_text = Mock(spec=pygame.Surface)
    text_rect = pygame.Rect(100, 50, 200, 40)

    font.render.return_value = rendered_text
    rendered_text.get_rect.return_value = text_rect

    result = draw_text(
        surface,
        "Adventure",
        font,
        (240, 240, 240),
        center=(640, 120),
    )

    font.render.assert_called_once_with(
        "Adventure",
        True,
        (240, 240, 240),
    )
    rendered_text.get_rect.assert_called_once_with(center=(640, 120))
    surface.blit.assert_called_once_with(rendered_text, text_rect)
    assert result is text_rect
