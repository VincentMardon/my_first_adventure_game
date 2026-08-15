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
