import pygame


class Animation:
    """Advance a looping sequence of image frames over time.

    Args:
        frames: Non-empty sequence of image surfaces.
        frame_duration: Positive display duration of each frame in seconds.
    """

    def __init__(
        self,
        frames: tuple[pygame.Surface, ...],
        frame_duration: float,
    ) -> None:
        if not frames:
            raise ValueError("frames must not be empty")

        if frame_duration <= 0.0:
            raise ValueError("frame duration must be positive")

        self._frames = frames
        self._frame_duration = frame_duration
        self._frame_index = 0
        self._elapsed_time = 0.0

    @property
    def current_frame(self) -> pygame.Surface:
        """Return the frame currently selected for rendering."""
        return self._frames[self._frame_index]

    def update(self, delta_time: float) -> None:
        """Advance the animation by an elapsed duration in seconds."""
        self._elapsed_time += delta_time

        elapsed_frames = int(self._elapsed_time / self._frame_duration)

        if elapsed_frames == 0:
            return

        self._frame_index = (self._frame_index + elapsed_frames) % len(self._frames)
        self._elapsed_time -= elapsed_frames * self._frame_duration

    def reset(self) -> None:
        """Return the animation to its initial frame and timing state."""
        self._frame_index = 0
        self._elapsed_time = 0.0
