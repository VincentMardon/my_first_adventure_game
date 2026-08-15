import pygame

from my_first_adventure_game.engine.world import Entity, World
from my_first_adventure_game.game.entities import NPC, Player
from my_first_adventure_game.game.levels.game_map import GameMap
from my_first_adventure_game.game.levels.map_exit import MapExit


def create_clearing_map(player: Player) -> GameMap:
    """Create the clearing map with the current session player."""
    world = World()
    exits = (
        MapExit(
            entity=Entity(
                entity_id="exit-to-demo",
                position=pygame.Vector2(64.0, 320.0),
                size=pygame.Vector2(32.0, 80.0),
            ),
            destination_map_id="demo",
            destination_position=(1120.0, 320.0),
        ),
    )
    walls = (
        Entity(
            entity_id="clearing-wall-top",
            position=pygame.Vector2(64.0, 64.0),
            size=pygame.Vector2(1152.0, 32.0),
        ),
        Entity(
            entity_id="clearing-wall-bottom",
            position=pygame.Vector2(64.0, 624.0),
            size=pygame.Vector2(1152.0, 32.0),
        ),
        Entity(
            entity_id="clearing-wall-left-top",
            position=pygame.Vector2(64.0, 96.0),
            size=pygame.Vector2(32.0, 224.0),
        ),
        Entity(
            entity_id="clearing-wall-left-bottom",
            position=pygame.Vector2(64.0, 400.0),
            size=pygame.Vector2(32.0, 224.0),
        ),
        Entity(
            entity_id="clearing-wall-right",
            position=pygame.Vector2(1184.0, 96.0),
            size=pygame.Vector2(32.0, 528.0),
        ),
    )
    npcs = (
        NPC(
            name="Caretaker",
            entity=Entity(
                entity_id="npc-clearing-caretaker",
                position=pygame.Vector2(640.0, 320.0),
                size=pygame.Vector2(24.0, 32.0),
            ),
            dialogue_lines=(
                "I just finished cleaning these walls.",
                "Please try not to leave any mysterious stains.",
            ),
        ),
    )
    collectibles = (
        Entity(
            entity_id="collectible-clearing-1",
            position=pygame.Vector2(960.0, 480.0),
            size=pygame.Vector2(16.0, 16.0),
            active=False,
        ),
    )

    for entity in (
        player.entity,
        *walls,
        *(npc.entity for npc in npcs),
        *collectibles,
        *(map_exit.entity for map_exit in exits),
    ):
        world.add(entity)

    return GameMap(
        map_id="clearing",
        background_color=(28, 26, 40),
        world=world,
        player=player,
        walls=walls,
        enemies=(),
        npcs=npcs,
        destructible_obstacles=(),
        collectibles=collectibles,
        exits=exits,
    )
