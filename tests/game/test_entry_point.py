from unittest.mock import Mock, call

from my_first_adventure_game.game import main as game_main
from my_first_adventure_game.game.events import (
    EnemyDefeated,
    ItemCollected,
    ObstacleDestroyed,
    PlayerDefeated,
)


def test_main_builds_and_runs_application(monkeypatch) -> None:
    input_state = Mock()
    initial_scene = Mock()
    scene_manager = Mock()
    font_cache = Mock()
    game_map = Mock()
    session_score = Mock()
    gameplay_scene = Mock()
    application = Mock()
    first_player_frame = Mock()
    second_player_frame = Mock()
    player_idle_animation = Mock()
    player_movement_animation = Mock()
    third_player_frame = Mock()
    fourth_player_frame = Mock()
    fifth_player_frame = Mock()
    sixth_player_frame = Mock()
    player_collection_animation = Mock()
    seventh_player_frame = Mock()
    eighth_player_frame = Mock()
    player_attack_animation = Mock()

    create_input_state = Mock(return_value=input_state)
    create_title_scene = Mock(return_value=initial_scene)
    create_scene_manager = Mock(return_value=scene_manager)
    create_font_cache = Mock(return_value=font_cache)
    create_demo_map = Mock(return_value=game_map)
    create_session_score = Mock(return_value=session_score)
    score_item_collection = Mock(return_value=100)
    create_gameplay_scene = Mock(return_value=gameplay_scene)
    create_application = Mock(return_value=application)
    create_surface = Mock(
        side_effect=(
            first_player_frame,
            second_player_frame,
            third_player_frame,
            fourth_player_frame,
            fifth_player_frame,
            sixth_player_frame,
            seventh_player_frame,
            eighth_player_frame,
        ),
    )
    create_animation = Mock(
        side_effect=(
            player_idle_animation,
            player_movement_animation,
            player_collection_animation,
            player_attack_animation,
        )
    )

    monkeypatch.setattr(game_main, "TitleScene", create_title_scene)
    monkeypatch.setattr(game_main, "SceneManager", create_scene_manager)
    monkeypatch.setattr(game_main, "InputState", create_input_state)
    monkeypatch.setattr(game_main, "FontCache", create_font_cache)
    monkeypatch.setattr(game_main, "create_demo_map", create_demo_map)
    monkeypatch.setattr(game_main, "SessionScore", create_session_score)
    monkeypatch.setattr(
        game_main,
        "item_collection_points",
        score_item_collection,
    )
    monkeypatch.setattr(game_main, "GameplayScene", create_gameplay_scene)
    monkeypatch.setattr(game_main, "Application", create_application)
    monkeypatch.setattr(game_main.pygame, "Surface", create_surface)
    monkeypatch.setattr(game_main, "Animation", create_animation)

    game_main.main()

    create_input_state.assert_called_once_with(game_main.DEFAULT_KEYBOARD_BINDINGS)
    create_font_cache.assert_called_once_with(game_main.pygame)
    create_demo_map.assert_called_once_with()
    create_session_score.assert_called_once_with()
    assert create_surface.call_args_list == [
        call(game_main.PLAYER_FRAME_SIZE),
        call(game_main.PLAYER_FRAME_SIZE),
        call(game_main.PLAYER_FRAME_SIZE),
        call(game_main.PLAYER_FRAME_SIZE),
        call(game_main.PLAYER_FRAME_SIZE),
        call(game_main.PLAYER_FRAME_SIZE),
        call(game_main.PLAYER_FRAME_SIZE),
        call(game_main.PLAYER_FRAME_SIZE),
    ]
    first_player_frame.fill.assert_called_once_with(
        game_main.PLAYER_IDLE_COLORS[0],
    )
    second_player_frame.fill.assert_called_once_with(
        game_main.PLAYER_IDLE_COLORS[1],
    )
    third_player_frame.fill.assert_called_once_with(
        game_main.PLAYER_MOVEMENT_COLORS[0],
    )
    fourth_player_frame.fill.assert_called_once_with(
        game_main.PLAYER_MOVEMENT_COLORS[1],
    )
    fifth_player_frame.fill.assert_called_once_with(
        game_main.PLAYER_COLLECTION_COLORS[0],
    )
    sixth_player_frame.fill.assert_called_once_with(
        game_main.PLAYER_COLLECTION_COLORS[1],
    )
    seventh_player_frame.fill.assert_called_once_with(
        game_main.PLAYER_ATTACK_COLORS[0],
    )
    eighth_player_frame.fill.assert_called_once_with(
        game_main.PLAYER_ATTACK_COLORS[1],
    )
    assert create_animation.call_args_list == [
        call(
            frames=(first_player_frame, second_player_frame),
            frame_duration=game_main.PLAYER_IDLE_FRAME_DURATION,
        ),
        call(
            frames=(third_player_frame, fourth_player_frame),
            frame_duration=game_main.PLAYER_MOVEMENT_FRAME_DURATION,
        ),
        call(
            frames=(fifth_player_frame, sixth_player_frame),
            frame_duration=game_main.PLAYER_COLLECTION_FRAME_DURATION,
            loop=False,
        ),
        call(
            frames=(seventh_player_frame, eighth_player_frame),
            frame_duration=game_main.PLAYER_ATTACK_FRAME_DURATION,
            loop=False,
        ),
    ]
    create_gameplay_scene.assert_called_once()
    gameplay_args = create_gameplay_scene.call_args.args

    assert gameplay_args[:4] == (
        input_state,
        font_cache,
        session_score,
        game_map.player,
    )
    assert callable(gameplay_args[4])
    assert gameplay_args[5] is game_map.walls
    assert gameplay_args[6] is game_map.enemies
    assert callable(gameplay_args[7])
    assert gameplay_args[8] is game_map.collectibles
    assert callable(gameplay_args[9])
    assert gameplay_args[10] is game_map.destructible_obstacles
    assert callable(gameplay_args[11])
    assert gameplay_args[12] is player_idle_animation
    assert gameplay_args[13] is player_movement_animation
    assert gameplay_args[14] is player_collection_animation
    assert gameplay_args[15] is player_attack_animation

    handle_player_defeated = gameplay_args[4]
    player_event = PlayerDefeated(player_id="player")

    assert handle_player_defeated(player_event) is None

    handle_enemy_defeated = gameplay_args[7]
    enemy_event = EnemyDefeated(enemy_id="enemy-1")

    assert handle_enemy_defeated(enemy_event) is None

    handle_item_collected = gameplay_args[9]
    event = ItemCollected(item_id="collectible-1")

    handle_item_collected(event)

    handle_obstacle_destroyed = gameplay_args[11]
    obstacle_event = ObstacleDestroyed(obstacle_id="destructible-1")

    assert handle_obstacle_destroyed(obstacle_event) is None

    score_item_collection.assert_called_once_with(event)
    session_score.add.assert_called_once_with(100)

    create_title_scene.assert_called_once()
    assert create_title_scene.call_args.args[:2] == (
        font_cache,
        input_state,
    )
    start_game = create_title_scene.call_args.args[2]

    start_game()

    scene_manager.change_scene.assert_called_once_with(gameplay_scene)

    create_scene_manager.assert_called_once_with(initial_scene)
    create_application.assert_called_once_with(
        window_config=game_main.WINDOW_CONFIG,
        scene_manager=scene_manager,
        input_processor=input_state,
        frames_per_second=game_main.FRAMES_PER_SECOND,
    )
    application.run.assert_called_once_with()
