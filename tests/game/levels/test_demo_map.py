import pygame

from my_first_adventure_game.game.levels import create_demo_map


def test_demo_map_registers_all_entities_in_world() -> None:
    game_map = create_demo_map()

    assert game_map.world.entities == (
        game_map.player.entity,
        *game_map.walls,
        *(enemy.entity for enemy in game_map.enemies),
        *(npc.entity for npc in game_map.npcs),
        *game_map.collectibles,
    )
    assert (
        game_map.world.get(game_map.player.entity.entity_id) is game_map.player.entity
    )

    for entity in (*game_map.walls, *game_map.collectibles):
        assert game_map.world.get(entity.entity_id) is entity

    for enemy in game_map.enemies:
        assert game_map.world.get(enemy.entity.entity_id) is enemy.entity

    for npc in game_map.npcs:
        assert game_map.world.get(npc.entity.entity_id) is npc.entity


def test_demo_map_has_active_collectibles() -> None:
    game_map = create_demo_map()

    assert game_map.collectibles
    assert all(collectible.active for collectible in game_map.collectibles)


def test_demo_map_has_active_player_and_solid_walls() -> None:
    game_map = create_demo_map()

    assert game_map.player.entity.active
    assert game_map.player.health == 3
    assert game_map.walls
    assert all(wall.active for wall in game_map.walls)


def test_demo_map_player_starts_outside_walls() -> None:
    game_map = create_demo_map()

    assert not any(
        game_map.player.entity.bounds.overlaps(wall.bounds) for wall in game_map.walls
    )


def test_demo_map_collectibles_start_outside_player_and_walls() -> None:
    game_map = create_demo_map()

    for collectible in game_map.collectibles:
        assert not collectible.bounds.overlaps(game_map.player.entity.bounds)
        assert not any(
            collectible.bounds.overlaps(wall.bounds) for wall in game_map.walls
        )


def test_demo_map_uses_floating_point_entity_geometry() -> None:
    game_map = create_demo_map()

    assert isinstance(game_map.player.entity.position, pygame.Vector2)
    assert isinstance(game_map.player.entity.size, pygame.Vector2)
    assert all(
        isinstance(wall.position, pygame.Vector2)
        and isinstance(wall.size, pygame.Vector2)
        for wall in game_map.walls
    )
    assert all(
        isinstance(collectible.position, pygame.Vector2)
        and isinstance(collectible.size, pygame.Vector2)
        for collectible in game_map.collectibles
    )

    assert all(
        isinstance(enemy.entity.position, pygame.Vector2)
        and isinstance(enemy.entity.size, pygame.Vector2)
        for enemy in game_map.enemies
    )

    assert all(
        isinstance(npc.entity.position, pygame.Vector2)
        and isinstance(npc.entity.size, pygame.Vector2)
        for npc in game_map.npcs
    )


def test_demo_map_wall_bounds_are_distinct() -> None:
    game_map = create_demo_map()

    assert len({wall.bounds for wall in game_map.walls}) == len(game_map.walls)


def test_demo_map_has_active_destructible_obstacles() -> None:
    game_map = create_demo_map()

    assert game_map.destructible_obstacles
    assert all(obstacle.active for obstacle in game_map.destructible_obstacles)
    assert all(
        obstacle in game_map.walls for obstacle in game_map.destructible_obstacles
    )


def test_demo_map_has_active_enemies() -> None:
    game_map = create_demo_map()

    assert game_map.enemies
    assert all(enemy.entity.active for enemy in game_map.enemies)
    assert all(enemy.health == 2 for enemy in game_map.enemies)
    assert not any(enemy.entity in game_map.walls for enemy in game_map.enemies)


def test_demo_map_has_active_npcs_with_dialogue() -> None:
    game_map = create_demo_map()

    assert game_map.npcs
    assert all(npc.entity.active for npc in game_map.npcs)
    assert all(npc.dialogue_text.strip() for npc in game_map.npcs)
    assert not any(npc.entity in game_map.walls for npc in game_map.npcs)
