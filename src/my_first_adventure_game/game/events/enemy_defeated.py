from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EnemyDefeated:
    """Report that the player defeated an enemy.

    Attributes:
        enemy_id: stable identifier of the defeated enemy.
    """

    enemy_id: str
