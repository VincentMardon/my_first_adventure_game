from enum import Enum, auto

from my_first_adventure_game.engine.collisions import AABB
from my_first_adventure_game.game.entities.caretaker_movement import (
    caretaker_sidestep_target,
)
from my_first_adventure_game.game.entities.npc import NPC
from my_first_adventure_game.game.entities.player import Player
from my_first_adventure_game.game.entities.wall_stain import WallStain

CARETAKER_SIDESTEP_TARGET_ID = "caretaker-sidestep"


class CaretakerPhase(Enum):
    """Idebtify the current phase of the Caretaker wall task."""

    IDLE = auto()
    RETURNING_TO_STAIN = auto()
    SIDESTEPPING = auto()


class CaretakerBehavior:
    """Recalculate Caretaker movement targets for the current wall task.

    Attributes:
        phase: Current phase of the wall task.
    """

    __slots__ = ("_caretaker", "_player", "_stain", "phase")

    def __init__(
        self,
        caretaker: NPC,
        player: Player,
    ) -> None:
        self._caretaker = caretaker
        self._player = player
        self._stain: WallStain | None = None
        self.phase = CaretakerPhase.IDLE

    def return_to_stain(self, stain: WallStain) -> None:
        """Start returning toward a wall stain."""
        self._stain = stain
        self.phase = CaretakerPhase.RETURNING_TO_STAIN

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

        if approach_bounds.overlaps(self._player.entity.bounds):
            self.phase = CaretakerPhase.SIDESTEPPING
            movement_target = caretaker_sidestep_target(
                self._stain,
                self._caretaker.entity.bounds,
                self._player.entity.bounds,
            )
            movement_target_id = CARETAKER_SIDESTEP_TARGET_ID
        else:
            self.phase = CaretakerPhase.RETURNING_TO_STAIN
            movement_target = approach_position
            movement_target_id = self._stain.wall_id

        self._caretaker.movement_target = movement_target
        self._caretaker.movement_target_id = movement_target_id
        self._caretaker.movement_target_entity = None

    def complete_task(self) -> None:
        """Finish the current wall task and clear Caretaker movement."""
        self._stain = None
        self.phase = CaretakerPhase.IDLE
        self._caretaker.movement_target = None
        self._caretaker.movement_target_id = None
        self._caretaker.movement_target_entity = None
