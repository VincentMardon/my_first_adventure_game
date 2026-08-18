from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NPCTargetReached:
    """Report that an NPC reached its moving target.

    Attributes:
        npc_id: Stable identifier of the NPC.
        target_id: Stable identifier of the reached target.
    """

    npc_id: str
    target_id: str
