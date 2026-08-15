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
