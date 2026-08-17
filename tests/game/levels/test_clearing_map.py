import pygame

from my_first_adventure_game.game.levels import (
    create_clearing_map,
    create_demo_map,
)


def test_clearing_map_reuses_player_with_stable_identifier() -> None:
    player = create_demo_map().player

    game_map = create_clearing_map(player)

    assert game_map.map_id == "clearing"
    assert game_map.player is player
    assert game_map.world.get(player.entity.entity_id) is player.entity


def test_clearing_map_has_registered_exit_to_demo() -> None:
    player = create_demo_map().player

    game_map = create_clearing_map(player)

    assert len(game_map.exits) == 1

    map_exit = game_map.exits[0]

    assert map_exit.destination_map_id == "demo"
    assert map_exit.destination_position == (1120.0, 320.0)
    assert game_map.world.get(map_exit.entity.entity_id) is map_exit.entity


def test_clearing_map_registers_boundary_walls_around_exit() -> None:
    player = create_demo_map().player

    game_map = create_clearing_map(player)

    assert tuple(
        (
            wall.entity_id,
            (wall.position.x, wall.position.y),
            (wall.size.x, wall.size.y),
        )
        for wall in game_map.walls
    ) == (
        ("clearing-wall-top", (64.0, 64.0), (1152.0, 32.0)),
        ("clearing-wall-bottom", (64.0, 624.0), (1152.0, 32.0)),
        ("clearing-wall-left-top", (64.0, 96.0), (32.0, 224.0)),
        ("clearing-wall-left-bottom", (64.0, 400.0), (32.0, 224.0)),
        ("clearing-wall-right", (1184.0, 96.0), (32.0, 528.0)),
    )

    assert all(game_map.world.get(wall.entity_id) is wall for wall in game_map.walls)
    assert all(
        not wall.bounds.overlaps(game_map.exits[0].entity.bounds)
        for wall in game_map.walls
    )
    assert all(
        not wall.bounds.overlaps(player.entity.bounds) for wall in game_map.walls
    )


def test_clearing_map_has_registered_caretaker() -> None:
    player = create_demo_map().player

    game_map = create_clearing_map(player)

    assert len(game_map.npcs) == 1

    caretaker = game_map.npcs[0]

    assert caretaker.name == "Caretaker"
    assert caretaker.entity.entity_id == "npc-clearing-caretaker"
    assert caretaker.entity.position == (640.0, 320.0)
    assert caretaker.entity.size == (24.0, 32.0)
    assert caretaker.movement_target == pygame.Vector2(800.0, 480.0)
    assert caretaker.movement_speed == 80.0
    assert caretaker.entity.active
    assert caretaker.dialogue_lines == (
        "I just finished cleaning these walls.",
        "Please try not to leave any mysterious stains.",
    )
    assert game_map.world.get(caretaker.entity.entity_id) is caretaker.entity
    assert all(
        not caretaker.entity.bounds.overlaps(wall.bounds) for wall in game_map.walls
    )
    assert not caretaker.entity.bounds.overlaps(player.entity.bounds)
    assert not caretaker.entity.bounds.overlaps(game_map.exits[0].entity.bounds)


def test_clearing_map_has_registered_hidden_collectible() -> None:
    player = create_demo_map().player

    game_map = create_clearing_map(player)

    assert len(game_map.collectibles) == 1

    collectible = game_map.collectibles[0]

    assert collectible.entity_id == "collectible-clearing-1"
    assert collectible.position == (960.0, 480.0)
    assert collectible.size == (16.0, 16.0)
    assert not collectible.active
    assert game_map.world.get(collectible.entity_id) is collectible
    assert all(not collectible.bounds.overlaps(wall.bounds) for wall in game_map.walls)
    assert all(
        not collectible.bounds.overlaps(npc.entity.bounds) for npc in game_map.npcs
    )
    assert not collectible.bounds.overlaps(player.entity.bounds)
    assert not collectible.bounds.overlaps(game_map.exits[0].entity.bounds)


def test_clearing_map_has_distinct_background_color() -> None:
    player = create_demo_map().player

    game_map = create_clearing_map(player)

    assert game_map.background_color == (28, 26, 40)
