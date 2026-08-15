from unittest.mock import Mock, call

from my_first_adventure_game.game import main as game_main
from my_first_adventure_game.game.events import (
    EnemyDefeated,
    ItemCollected,
    ObstacleDestroyed,
    PlayerDefeated,
)
from my_first_adventure_game.game.progression import (
    GuideObjective,
    GuideObjectiveState,
)


def test_main_builds_and_runs_application(monkeypatch) -> None:
    input_state = Mock()
    initial_scene = Mock()
    scene_manager = Mock()
    font_cache = Mock()
    game_map = Mock()
    game_map.map_id = "demo"
    game_map.exits = ()
    clearing_map = Mock()
    clearing_map.map_id = "clearing"
    clearing_map.player = game_map.player
    clearing_collectible = Mock()
    clearing_collectible.active = False
    clearing_map.collectibles = (clearing_collectible,)
    first_enemy = Mock()
    first_enemy.entity.active = False
    second_enemy = Mock()
    second_enemy.entity.active = True
    game_map.enemies = (first_enemy, second_enemy)
    npc = Mock()
    npc.entity.entity_id = "npc-1"
    npc.name = "Guide"
    npc.dialogue_lines = (
        "Welcome, traveler!",
        "The road ahead is dangerous.",
    )
    collectible = Mock()
    collectible.active = False
    game_map.collectibles = (collectible,)
    game_map.npcs = (npc,)
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
    defeat_scene = Mock()
    victory_scene = Mock()
    pause_scene = Mock()
    dialogue_scene = Mock()

    create_input_state = Mock(return_value=input_state)
    create_title_scene = Mock(return_value=initial_scene)
    create_scene_manager = Mock(return_value=scene_manager)
    create_font_cache = Mock(return_value=font_cache)
    create_demo_map = Mock(return_value=game_map)
    create_clearing_map = Mock(return_value=clearing_map)
    create_session_score = Mock(return_value=session_score)
    score_item_collection = Mock(return_value=100)
    score_guide_objective_completion = Mock(return_value=500)
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
    create_defeat_scene = Mock(return_value=defeat_scene)
    create_victory_scene = Mock(return_value=victory_scene)
    create_pause_scene = Mock(return_value=pause_scene)
    create_dialogue_scene = Mock(return_value=dialogue_scene)

    monkeypatch.setattr(game_main, "TitleScene", create_title_scene)
    monkeypatch.setattr(game_main, "SceneManager", create_scene_manager)
    monkeypatch.setattr(game_main, "InputState", create_input_state)
    monkeypatch.setattr(game_main, "FontCache", create_font_cache)
    monkeypatch.setattr(game_main, "create_demo_map", create_demo_map)
    monkeypatch.setattr(
        game_main,
        "create_clearing_map",
        create_clearing_map,
    )
    monkeypatch.setattr(game_main, "SessionScore", create_session_score)
    monkeypatch.setattr(
        game_main,
        "item_collection_points",
        score_item_collection,
    )
    monkeypatch.setattr(
        game_main,
        "guide_objective_completion_points",
        score_guide_objective_completion,
    )
    monkeypatch.setattr(game_main, "GameplayScene", create_gameplay_scene)
    monkeypatch.setattr(game_main, "Application", create_application)
    monkeypatch.setattr(game_main.pygame, "Surface", create_surface)
    monkeypatch.setattr(game_main, "Animation", create_animation)
    monkeypatch.setattr(game_main, "DefeatScene", create_defeat_scene)
    monkeypatch.setattr(game_main, "VictoryScene", create_victory_scene)
    monkeypatch.setattr(game_main, "PauseScene", create_pause_scene)
    monkeypatch.setattr(game_main, "DialogueScene", create_dialogue_scene)

    game_main.main()

    create_input_state.assert_called_once_with(game_main.DEFAULT_KEYBOARD_BINDINGS)
    create_font_cache.assert_called_once_with(game_main.pygame)
    create_demo_map.assert_not_called()
    create_clearing_map.assert_not_called()
    create_session_score.assert_not_called()
    create_gameplay_scene.assert_not_called()
    create_defeat_scene.assert_not_called()
    create_surface.assert_not_called()
    create_animation.assert_not_called()

    create_title_scene.assert_called_once()
    assert create_title_scene.call_args.args[:2] == (
        font_cache,
        input_state,
    )
    start_game = create_title_scene.call_args.args[2]

    create_victory_scene.assert_not_called()

    start_game()

    create_pause_scene.assert_called_once()
    pause_args = create_pause_scene.call_args.args

    assert pause_args[:2] == (
        font_cache,
        input_state,
    )
    assert callable(pause_args[2])

    create_demo_map.assert_called_once_with()
    create_clearing_map.assert_called_once_with(game_map.player)
    create_session_score.assert_called_once_with()
    create_defeat_scene.assert_called_once()

    defeat_args = create_defeat_scene.call_args.args

    assert defeat_args[:3] == (
        font_cache,
        session_score,
        input_state,
    )
    assert callable(defeat_args[3])

    return_to_title = defeat_args[3]

    create_victory_scene.assert_called_once()
    victory_args = create_victory_scene.call_args.args

    assert victory_args[:3] == (
        font_cache,
        session_score,
        input_state,
    )
    assert victory_args[3] is return_to_title

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
    assert callable(gameplay_args[5])
    assert gameplay_args[6] is game_map.walls
    assert gameplay_args[7] is game_map.enemies
    assert gameplay_args[8] is game_map.npcs
    assert callable(gameplay_args[9])
    assert callable(gameplay_args[10])
    assert gameplay_args[11] is game_map.collectibles
    assert callable(gameplay_args[12])
    assert gameplay_args[13] is game_map.destructible_obstacles
    assert callable(gameplay_args[14])
    assert gameplay_args[15] is player_idle_animation
    assert gameplay_args[16] is player_movement_animation
    assert gameplay_args[17] is player_collection_animation
    assert gameplay_args[18] is player_attack_animation
    assert isinstance(gameplay_args[19], GuideObjective)
    assert gameplay_args[19].total_items == (
        len(game_map.collectibles) + len(clearing_map.collectibles)
    )
    assert gameplay_args[20] is game_map.exits
    assert callable(gameplay_args[21])

    request_pause = gameplay_args[4]
    handle_player_defeated = gameplay_args[5]
    resume_game = pause_args[2]

    request_pause()
    scene_manager.change_scene.assert_called_with(pause_scene)

    resume_game()
    scene_manager.change_scene.assert_called_with(gameplay_scene)

    handle_npc_interacted = gameplay_args[9]

    caretaker = Mock()
    caretaker.name = "Caretaker"
    caretaker.entity.entity_id = "npc-clearing-caretaker"
    caretaker.dialogue_lines = (
        "I just finished cleaning these walls.",
        "Please try not to leave any mysterious stains.",
    )

    handle_npc_interacted(caretaker)

    create_dialogue_scene.assert_called_once()
    caretaker_dialogue_args = create_dialogue_scene.call_args.args

    assert caretaker_dialogue_args[:4] == (
        font_cache,
        input_state,
        caretaker.name,
        caretaker.dialogue_lines,
    )
    assert gameplay_args[19].state is GuideObjectiveState.NOT_STARTED
    assert not collectible.active
    assert not clearing_collectible.active

    create_dialogue_scene.reset_mock()

    handle_npc_interacted(npc)

    create_dialogue_scene.assert_called_once()
    dialogue_args = create_dialogue_scene.call_args.args

    assert dialogue_args[:4] == (
        font_cache,
        input_state,
        npc.name,
        npc.dialogue_lines,
    )
    assert callable(dialogue_args[4])
    scene_manager.change_scene.assert_called_with(dialogue_scene)

    close_dialogue = dialogue_args[4]
    close_dialogue()

    assert collectible.active
    assert clearing_collectible.active

    scene_manager.change_scene.assert_called_with(gameplay_scene)

    handle_npc_interacted(npc)

    assert create_dialogue_scene.call_count == 2
    active_dialogue_args = create_dialogue_scene.call_args.args

    assert active_dialogue_args[:4] == (
        font_cache,
        input_state,
        npc.name,
        game_main.COLLECTION_ACTIVE_DIALOGUE_LINES,
    )

    active_dialogue_args[4]()

    scene_manager.change_scene.assert_called_with(gameplay_scene)

    handle_item_collected = gameplay_args[12]
    event = ItemCollected(item_id="collectible-1")

    collectible.active = False
    handle_item_collected(event)

    assert gameplay_args[19].collected_items == 1
    assert gameplay_args[19].state is GuideObjectiveState.ACTIVE

    clearing_event = ItemCollected(item_id="collectible-clearing-1")
    clearing_collectible.active = False

    handle_item_collected(clearing_event)

    assert gameplay_args[19].collected_items == 2
    assert gameplay_args[19].state is GuideObjectiveState.READY_TO_COMPLETE

    player_event = PlayerDefeated(player_id="player")
    handle_player_defeated(player_event)

    return_to_title()

    handle_enemy_defeated = gameplay_args[10]
    first_enemy_event = EnemyDefeated(enemy_id="enemy-1")

    handle_enemy_defeated(first_enemy_event)

    assert call(victory_scene) not in scene_manager.change_scene.call_args_list

    second_enemy.entity.active = False
    second_enemy_event = EnemyDefeated(enemy_id="enemy-2")

    handle_enemy_defeated(second_enemy_event)

    assert call(victory_scene) not in (scene_manager.change_scene.call_args_list)

    assert gameplay_args[19].state is GuideObjectiveState.READY_TO_COMPLETE

    handle_map_exit_reached = gameplay_args[21]
    map_exit = Mock()
    map_exit.destination_map_id = "clearing"
    map_exit.destination_position = (128.0, 320.0)

    handle_map_exit_reached(map_exit)

    game_map.player.entity.position.update.assert_called_once_with(
        map_exit.destination_position
    )
    gameplay_scene.change_map.assert_called_once_with(clearing_map)

    return_exit = Mock()
    return_exit.destination_map_id = "demo"
    return_exit.destination_position = (1120.0, 320.0)

    handle_map_exit_reached(return_exit)

    assert game_map.player.entity.position.update.call_args_list == [
        call(map_exit.destination_position),
        call(return_exit.destination_position),
    ]
    assert gameplay_scene.change_map.call_args_list == [
        call(clearing_map),
        call(game_map),
    ]

    handle_npc_interacted(npc)

    assert create_dialogue_scene.call_count == 3
    completed_dialogue_args = create_dialogue_scene.call_args.args

    assert completed_dialogue_args[:4] == (
        font_cache,
        input_state,
        npc.name,
        game_main.COLLECTION_COMPLETE_DIALOGUE_LINES,
    )
    assert callable(completed_dialogue_args[4])
    scene_manager.change_scene.assert_called_with(dialogue_scene)

    completed_dialogue_args[4]()

    scene_manager.change_scene.assert_called_with(victory_scene)

    handle_npc_interacted(npc)

    assert create_dialogue_scene.call_count == 4
    completed_again_dialogue_args = create_dialogue_scene.call_args.args

    assert completed_again_dialogue_args[:4] == (
        font_cache,
        input_state,
        npc.name,
        game_main.COLLECTION_COMPLETE_DIALOGUE_LINES,
    )

    completed_again_dialogue_args[4]()

    handle_obstacle_destroyed = gameplay_args[14]
    obstacle_event = ObstacleDestroyed(obstacle_id="destructible-1")

    assert handle_obstacle_destroyed(obstacle_event) is None

    assert score_item_collection.call_args_list == [
        call(event),
        call(clearing_event),
    ]
    score_guide_objective_completion.assert_called_once_with()
    assert session_score.add.call_args_list == [
        call(100),
        call(100),
        call(500),
    ]

    second_game_map = Mock()
    second_game_map.map_id = "demo"
    second_game_map.exits = ()
    second_clearing_map = Mock()
    second_clearing_map.map_id = "clearing"
    second_clearing_map.player = second_game_map.player
    second_clearing_collectible = Mock()
    second_clearing_collectible.active = False
    second_clearing_map.collectibles = (second_clearing_collectible,)
    second_collectible = Mock()
    second_collectible.active = False
    second_enemy = Mock()
    second_enemy.entity.active = True
    second_game_map.enemies = (second_enemy,)
    second_game_map.collectibles = (second_collectible,)
    second_session_score = Mock()
    second_gameplay_scene = Mock()
    second_defeat_scene = Mock()
    second_victory_scene = Mock()
    second_pause_scene = Mock()
    second_player_frames = tuple(Mock() for _ in range(8))
    second_player_animations = tuple(Mock() for _ in range(4))

    create_demo_map.return_value = second_game_map
    create_clearing_map.return_value = second_clearing_map
    create_session_score.return_value = second_session_score
    create_gameplay_scene.return_value = second_gameplay_scene
    create_defeat_scene.return_value = second_defeat_scene
    create_victory_scene.return_value = second_victory_scene
    create_pause_scene.return_value = second_pause_scene
    create_surface.side_effect = second_player_frames
    create_animation.side_effect = second_player_animations

    start_game()

    assert create_demo_map.call_count == 2
    assert create_clearing_map.call_count == 2
    assert create_session_score.call_count == 2
    assert create_gameplay_scene.call_count == 2
    assert create_defeat_scene.call_count == 2
    assert create_victory_scene.call_count == 2
    assert create_pause_scene.call_count == 2

    assert create_clearing_map.call_args_list == [
        call(game_map.player),
        call(second_game_map.player),
    ]

    second_gameplay_args = create_gameplay_scene.call_args.args

    assert second_gameplay_args[:4] == (
        input_state,
        font_cache,
        second_session_score,
        second_game_map.player,
    )
    assert second_gameplay_args[4] is not request_pause
    assert second_gameplay_args[5] is not handle_player_defeated
    assert second_gameplay_args[6] is second_game_map.walls
    assert second_gameplay_args[7] is second_game_map.enemies
    assert second_gameplay_args[8] is second_game_map.npcs
    assert second_gameplay_args[11] is second_game_map.collectibles
    assert second_gameplay_args[13] is second_game_map.destructible_obstacles
    assert second_gameplay_args[15:19] == second_player_animations
    assert isinstance(second_gameplay_args[19], GuideObjective)
    assert second_gameplay_args[19] is not gameplay_args[19]
    assert second_gameplay_args[19].total_items == (
        len(second_game_map.collectibles) + len(second_clearing_map.collectibles)
    )
    assert second_gameplay_args[20] is second_game_map.exits
    assert callable(second_gameplay_args[21])
    assert second_gameplay_args[21] is not handle_map_exit_reached

    second_defeat_args = create_defeat_scene.call_args.args

    assert second_defeat_args[:3] == (
        font_cache,
        second_session_score,
        input_state,
    )
    assert second_defeat_args[3] is not return_to_title

    second_victory_args = create_victory_scene.call_args.args

    assert second_victory_args[:3] == (
        font_cache,
        second_session_score,
        input_state,
    )
    assert second_victory_args[3] is second_defeat_args[3]
    assert second_victory_args[3] is not return_to_title

    second_pause_args = create_pause_scene.call_args.args

    assert second_pause_args[:2] == (
        font_cache,
        input_state,
    )
    assert second_pause_args[2] is not resume_game

    second_guide_objective = second_gameplay_args[19]
    second_guide_objective.start()
    second_guide_objective.record_item_collected()
    second_guide_objective.record_item_collected()
    second_guide_objective.complete()

    second_handle_enemy_defeated = second_gameplay_args[10]
    second_enemy_event = EnemyDefeated(enemy_id="second-enemy")

    second_handle_enemy_defeated(second_enemy_event)

    assert call(second_victory_scene) not in (scene_manager.change_scene.call_args_list)

    second_enemy.entity.active = False
    second_handle_enemy_defeated(second_enemy_event)

    scene_manager.change_scene.assert_called_with(second_victory_scene)

    assert scene_manager.change_scene.call_args_list == [
        call(gameplay_scene),
        call(pause_scene),
        call(gameplay_scene),
        call(dialogue_scene),  # Caretaker
        call(dialogue_scene),  # Guide introduction
        call(gameplay_scene),
        call(dialogue_scene),  # Guide reminder
        call(gameplay_scene),
        call(defeat_scene),
        call(initial_scene),
        call(dialogue_scene),  # Guide completion
        call(victory_scene),
        call(dialogue_scene),  # Guide after completion
        call(gameplay_scene),
        call(second_gameplay_scene),
        call(second_victory_scene),
    ]

    second_handle_map_exit_reached = second_gameplay_args[21]
    second_map_exit = Mock()
    second_map_exit.destination_map_id = "clearing"
    second_map_exit.destination.position = (128.0, 320.0)

    second_handle_map_exit_reached(second_map_exit)

    second_game_map.player.entity.position.update.assert_called_once_with(
        second_map_exit.destination_position
    )
    second_gameplay_scene.change_map.assert_called_once_with(second_clearing_map)

    create_scene_manager.assert_called_once_with(initial_scene)
    create_application.assert_called_once_with(
        window_config=game_main.WINDOW_CONFIG,
        scene_manager=scene_manager,
        input_processor=input_state,
        frames_per_second=game_main.FRAMES_PER_SECOND,
    )
    application.run.assert_called_once_with()
