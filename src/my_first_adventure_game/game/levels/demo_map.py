import pygame

from my_first_adventure_game.engine.world import Entity, World
from my_first_adventure_game.game.entities import NPC, Enemy, Player
from my_first_adventure_game.game.levels.game_map import GameMap


def create_demo_map() -> GameMap:
    """Create the first Python-authored gameplay map."""
    player = Player(
        entity=Entity(
            entity_id="player",
            position=pygame.Vector2(128.0, 128.0),
            size=pygame.Vector2(32.0, 32.0),
        ),
        health=3,
    )
    destructible_obstacles = (
        Entity(
            entity_id="destructible-1",
            position=pygame.Vector2(800.0, 320.0),
            size=pygame.Vector2(32.0, 64.0),
        ),
    )
    walls = (
        Entity(
            entity_id="wall-top",
            position=pygame.Vector2(64.0, 64.0),
            size=pygame.Vector2(1152.0, 32.0),
        ),
        Entity(
            entity_id="wall-bottom",
            position=pygame.Vector2(64.0, 624.0),
            size=pygame.Vector2(1152.0, 32.0),
        ),
        Entity(
            entity_id="wall-left",
            position=pygame.Vector2(64.0, 96.0),
            size=pygame.Vector2(32.0, 528.0),
        ),
        Entity(
            entity_id="wall-right",
            position=pygame.Vector2(1184.0, 96.0),
            size=pygame.Vector2(32.0, 528.0),
        ),
        Entity(
            entity_id="wall-center",
            position=pygame.Vector2(400.0, 224.0),
            size=pygame.Vector2(32.0, 256.0),
        ),
        *destructible_obstacles,
    )
    enemies = (
        Enemy(
            entity=Entity(
                entity_id="enemy-1",
                position=pygame.Vector2(960.0, 480.0),
                size=pygame.Vector2(32.0, 32.0),
            ),
            health=2,
        ),
    )
    npcs = (
        NPC(
            name="Guide",
            entity=Entity(
                entity_id="npc-1",
                position=pygame.Vector2(576.0, 160.0),
                size=pygame.Vector2(24.0, 32.0),
            ),
            dialogue_lines=(
                "Welcome, traveler!",
                (
                    "The road ahead is dangerous, so keep your weapon ready "
                    "and watch every shadow along the way."
                ),
            ),
        ),
    )
    collectibles = (
        Entity(
            entity_id="collectible-1",
            position=pygame.Vector2(256.0, 160.0),
            size=pygame.Vector2(16.0, 16.0),
            active=False,
        ),
        Entity(
            entity_id="collectible-2",
            position=pygame.Vector2(640.0, 360.0),
            size=pygame.Vector2(16.0, 16.0),
            active=False,
        ),
    )

    world = World()

    for entity in (
        player.entity,
        *walls,
        *(enemy.entity for enemy in enemies),
        *(npc.entity for npc in npcs),
        *collectibles,
    ):
        world.add(entity)

    return GameMap(
        world=world,
        player=player,
        walls=walls,
        enemies=enemies,
        npcs=npcs,
        destructible_obstacles=destructible_obstacles,
        collectibles=collectibles,
    )
