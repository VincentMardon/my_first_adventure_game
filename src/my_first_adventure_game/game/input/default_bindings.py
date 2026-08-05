import pygame

from my_first_adventure_game.engine.input import KeyboardBindings
from my_first_adventure_game.game.input.actions import GameAction

DEFAULT_KEYBOARD_BINDINGS = KeyboardBindings(
    {
        GameAction.MOVE_LEFT: (pygame.K_LEFT,),
        GameAction.MOVE_RIGHT: (pygame.K_RIGHT,),
        GameAction.MOVE_UP: (pygame.K_UP,),
        GameAction.MOVE_DOWN: (pygame.K_DOWN,),
    }
)
