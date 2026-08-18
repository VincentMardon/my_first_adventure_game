from my_first_adventure_game.game.events.enemy_defeated import EnemyDefeated
from my_first_adventure_game.game.events.item_collected import ItemCollected
from my_first_adventure_game.game.events.npc_target_reached import NPCTargetReached
from my_first_adventure_game.game.events.obstacle_destroyed import ObstacleDestroyed
from my_first_adventure_game.game.events.player_defeated import PlayerDefeated
from my_first_adventure_game.game.events.wall_touched import WallTouched

__all__ = [
    "EnemyDefeated",
    "ItemCollected",
    "NPCTargetReached",
    "ObstacleDestroyed",
    "PlayerDefeated",
    "WallTouched",
]
