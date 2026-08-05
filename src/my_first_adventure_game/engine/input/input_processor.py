from typing import Protocol

import pygame


class InputProcessor(Protocol):
    def start_frame(self) -> None: ...

    def handle_event(self, event: pygame.event.Event) -> None: ...
