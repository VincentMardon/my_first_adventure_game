from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlayerDefeated:
    """Report that the player was defeated.

    Attributes:
        player_id: Stable identifier of the defeated player.
    """

    player_id: str
