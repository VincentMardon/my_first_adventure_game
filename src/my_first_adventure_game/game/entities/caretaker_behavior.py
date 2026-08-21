from collections.abc import Iterable
from enum import Enum, auto

import pygame

from my_first_adventure_game.engine.collisions import AABB
from my_first_adventure_game.engine.world import move_entity
from my_first_adventure_game.game.entities.caretaker_movement import (
    CaretakerSide,
    caretaker_nearest_side,
    caretaker_push_movement,
    caretaker_rounding_target,
    caretaker_sidestep_target,
)
from my_first_adventure_game.game.entities.npc import NPC
from my_first_adventure_game.game.entities.player import Player
from my_first_adventure_game.game.entities.wall_stain import WallStain

CARETAKER_ROUNDING_TARGET_ID = "caretaker-rounding"
CARETAKER_SIDESTEP_TARGET_ID = "caretaker-sidestep"


class CaretakerPhase(Enum):
    """Identify the current phase of the Caretaker wall task."""

    IDLE = auto()
    RETURNING_TO_STAIN = auto()
    ROUNDING_PLAYER = auto()
    SIDESTEPPING = auto()
    PUSHING_PLAYER = auto()


class CaretakerBehavior:
    """Recalculate Caretaker movement targets for the current wall task.

    Attributes:
        phase: Current phase of the wall task.
    """

    __slots__ = ("_caretaker", "_player", "_side", "_stain", "phase")

    def __init__(
        self,
        caretaker: NPC,
        player: Player,
    ) -> None:
        self._caretaker = caretaker
        self._player = player
        self._side: CaretakerSide | None = None
        self._stain: WallStain | None = None
        self.phase = CaretakerPhase.IDLE

    def _is_on_player_side(self) -> bool:
        """Return whether the Caretaker is beyond the chosen player side."""
        if self._stain is None or self._side is None:
            return False

        caretaker_bounds = self._caretaker.entity.bounds
        player_bounds = self._player.entity.bounds

        if self._stain.surface_normal[0] == 0.0:
            if self._side is CaretakerSide.NEGATIVE:
                return caretaker_bounds.right <= player_bounds.left

            return caretaker_bounds.left >= player_bounds.right

        if self._side is CaretakerSide.NEGATIVE:
            return caretaker_bounds.bottom <= player_bounds.top

        return caretaker_bounds.top >= player_bounds.bottom

    def return_to_stain(self, stain: WallStain) -> None:
        """Start returning toward a wall stain."""
        self._side = None
        self._stain = stain
        self.phase = CaretakerPhase.RETURNING_TO_STAIN

    def update(
        self,
        delta_time: float,
        solid_bounds: Iterable[AABB],
    ) -> None:
        """Update the current wall-task movement from live spatial state."""
        if self.phase is CaretakerPhase.PUSHING_PLAYER:
            self.push_player(delta_time, solid_bounds)

            if self._stain is None:
                return

            caretaker_size = self._caretaker.entity.size
            approach_position = self._stain.approach_position(caretaker_size)
            approach_bounds = AABB(
                x=approach_position.x,
                y=approach_position.y,
                width=caretaker_size.x,
                height=caretaker_size.y,
            )

            if not approach_bounds.overlaps(self._player.entity.bounds):
                self.update_target()

            return

        self.update_target()

    def update_target(self) -> None:
        """Recalculate the movement target from current spatial state."""
        if self._stain is None:
            return

        caretaker_size = self._caretaker.entity.size
        approach_position = self._stain.approach_position(caretaker_size)
        approach_bounds = AABB(
            x=approach_position.x,
            y=approach_position.y,
            width=caretaker_size.x,
            height=caretaker_size.y,
        )

        if self._side is None:
            self._side = caretaker_nearest_side(
                self._stain,
                self._caretaker.entity.bounds,
                self._player.entity.bounds,
            )

        if approach_bounds.overlaps(self._player.entity.bounds):
            sidestep_target = caretaker_sidestep_target(
                self._stain,
                self._caretaker.entity.bounds,
                self._player.entity.bounds,
                side=self._side,
            )

            if self.phase is CaretakerPhase.SIDESTEPPING or self._is_on_player_side():
                self.phase = CaretakerPhase.SIDESTEPPING
                movement_target = sidestep_target
                movement_target_id = CARETAKER_SIDESTEP_TARGET_ID
            else:
                self.phase = CaretakerPhase.ROUNDING_PLAYER
                movement_target = caretaker_rounding_target(
                    self._stain,
                    self._caretaker.entity.bounds,
                    self._player.entity.bounds,
                    side=self._side,
                )
                movement_target_id = CARETAKER_ROUNDING_TARGET_ID
        else:
            self._side = None
            self.phase = CaretakerPhase.RETURNING_TO_STAIN
            movement_target = approach_position
            movement_target_id = self._stain.wall_id

        self._caretaker.movement_target = movement_target
        self._caretaker.movement_target_id = movement_target_id
        self._caretaker.movement_target_entity = None

    def align_with_player(self) -> None:
        """Move from the outer corner toward the player's side at the wall."""
        if self._stain is None:
            return

        self.phase = CaretakerPhase.SIDESTEPPING
        self._caretaker.movement_target = caretaker_sidestep_target(
            self._stain,
            self._caretaker.entity.bounds,
            self._player.entity.bounds,
            side=self._side,
        )
        self._caretaker.movement_target_id = CARETAKER_SIDESTEP_TARGET_ID
        self._caretaker.movement_target_entity = None

    def start_pushing(self) -> None:
        """Start pushing the player without applying immediate movement."""
        if self._stain is None:
            return

        self.phase = CaretakerPhase.PUSHING_PLAYER
        self._caretaker.movement_target = None
        self._caretaker.movement_target_id = None
        self._caretaker.movement_target_entity = None

    def push_player(
        self,
        delta_time: float,
        solid_bounds: Iterable[AABB],
    ) -> pygame.Vector2:
        """Push the player and Caretaker together during an active push."""
        if self._stain is None or self.phase is not CaretakerPhase.PUSHING_PLAYER:
            return pygame.Vector2()

        requested_movement = caretaker_push_movement(
            self._stain,
            self._caretaker.entity.bounds,
            self._player.entity.bounds,
        )
        requested_movement.scale_to_length(self._caretaker.movement_speed * delta_time)

        applied_movement = move_entity(
            self._player.entity,
            requested_movement,
            solid_bounds,
        )
        self._caretaker.entity.position += applied_movement

        return applied_movement

    def complete_task(self) -> None:
        """Finish the current wall task and clear Caretaker movement."""
        self._stain = None
        self.phase = CaretakerPhase.IDLE
        self._caretaker.movement_target = None
        self._caretaker.movement_target_id = None
        self._caretaker.movement_target_entity = None
        self._side = None
