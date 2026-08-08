from unittest.mock import Mock

import pygame
import pytest

from my_first_adventure_game.engine.graphics import Animation


def test_animation_starts_on_first_frame() -> None:
    first_frame = Mock(spec=pygame.Surface)
    second_frame = Mock(spec=pygame.Surface)

    animation = Animation(
        frames=(first_frame, second_frame),
        frame_duration=0.1,
    )

    assert animation.current_frame is first_frame


def test_animation_advances_after_frame_duration() -> None:
    first_frame = Mock(spec=pygame.Surface)
    second_frame = Mock(spec=pygame.Surface)

    animation = Animation(
        frames=(first_frame, second_frame),
        frame_duration=0.1,
    )

    animation.update(0.1)

    assert animation.current_frame is second_frame


def test_animation_preserves_partial_elapsed_time() -> None:
    first_frame = Mock(spec=pygame.Surface)
    second_frame = Mock(spec=pygame.Surface)

    animation = Animation(
        frames=(first_frame, second_frame),
        frame_duration=0.1,
    )

    animation.update(0.06)
    animation.update(0.04)

    assert animation.current_frame is second_frame


def test_animation_loops_after_last_frame() -> None:
    first_frame = Mock(spec=pygame.Surface)
    second_frame = Mock(spec=pygame.Surface)

    animation = Animation(
        frames=(first_frame, second_frame),
        frame_duration=0.1,
    )

    animation.update(0.2)

    assert animation.current_frame is first_frame


def test_animation_reset_returns_to_first_frame() -> None:
    first_frame = Mock(spec=pygame.Surface)
    second_frame = Mock(spec=pygame.Surface)

    animation = Animation(
        frames=(first_frame, second_frame),
        frame_duration=0.1,
    )

    animation.update(0.1)

    animation.reset()

    assert animation.current_frame is first_frame


def test_animation_rejects_empty_frames() -> None:
    with pytest.raises(ValueError, match="frames must not be empty"):
        Animation(
            frames=(),
            frame_duration=0.1,
        )


@pytest.mark.parametrize("frame_duration", [0.0, -0.1])
def test_animation_rejects_non_positive_frame_duration(
    frame_duration: float,
) -> None:
    frame = Mock(spec=pygame.Surface)

    with pytest.raises(ValueError, match="frame duration must be positive"):
        Animation(
            frames=(frame,),
            frame_duration=frame_duration,
        )
