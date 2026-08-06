import pygame

from my_first_adventure_game.game.levels import create_demo_map


def test_demo_map_registers_player_and_walls_in_world() -> None:
    game_map = create_demo_map()

    assert game_map.world.entities == (
        game_map.player,
        *game_map.walls,
    )
    assert game_map.world.get(game_map.player.entity_id) is game_map.player

    for wall in game_map.walls:
        assert game_map.world.get(wall.entity_id) is wall


def test_demo_map_has_active_player_and_solid_walls() -> None:
    game_map = create_demo_map()

    assert game_map.player.active
    assert game_map.walls
    assert all(wall.active for wall in game_map.walls)


def test_demo_map_player_starts_outside_walls() -> None:
    game_map = create_demo_map()

    assert not any(
        game_map.player.bounds.overlaps(wall.bounds) for wall in game_map.walls
    )


def test_demo_map_uses_floating_point_entity_geometry() -> None:
    game_map = create_demo_map()

    assert isinstance(game_map.player.position, pygame.Vector2)
    assert isinstance(game_map.player.size, pygame.Vector2)
    assert all(
        isinstance(wall.position, pygame.Vector2)
        and isinstance(wall.size, pygame.Vector2)
        for wall in game_map.walls
    )


def test_demo_map_wall_bounds_are_distinct() -> None:
    game_map = create_demo_map()

    assert len({wall.bounds for wall in game_map.walls}) == len(game_map.walls)
