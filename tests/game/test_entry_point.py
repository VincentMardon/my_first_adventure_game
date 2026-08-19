import logging
from unittest.mock import Mock, call

from my_first_adventure_game.game import main as game_main
from my_first_adventure_game.game.events import (
    EnemyDefeated,
    ItemCollected,
    NPCTargetReached,
    ObstacleDestroyed,
    PlayerDefeated,
    WallTouched,
)
from my_first_adventure_game.game.profile import PlayerProfile
from my_first_adventure_game.game.progression import (
    GuideObjective,
    GuideObjectiveState,
)
from my_first_adventure_game.game.statistics import SessionStatistics


def test_main_builds_and_runs_application(monkeypatch) -> None:
    input_state = Mock()
    initial_scene = Mock()
    scene_manager = Mock()
    font_cache = Mock()
    game_map = Mock()
    game_map.map_id = "demo"
    game_map.exits = ()
    game_map.player.entity.entity_id = "player"
    clearing_map = Mock()
    clearing_map.map_id = "clearing"
    clearing_map.player = game_map.player
    clearing_collectible = Mock()
    clearing_collectible.active = False
    clearing_map.collectibles = (clearing_collectible,)
    clearing_wall = Mock()
    clearing_wall.entity_id = "clearing-wall-top"
    clearing_map.walls = (clearing_wall,)
    clearing_caretaker = Mock()
    clearing_caretaker.name = "Caretaker"
    clearing_caretaker.entity.entity_id = "npc-clearing-caretaker"
    initial_caretaker_target = Mock()
    clearing_caretaker.movement_target = initial_caretaker_target
    clearing_caretaker.movement_target_entity = None
    clearing_map.npcs = (clearing_caretaker,)
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
    session_score.value = 700
    session_statistics = Mock(spec=SessionStatistics)
    profile_path = Mock()
    player_profile = Mock(spec=PlayerProfile)
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
    profile_scene = Mock()

    create_input_state = Mock(return_value=input_state)
    create_title_scene = Mock(return_value=initial_scene)
    create_scene_manager = Mock(return_value=scene_manager)
    create_font_cache = Mock(return_value=font_cache)
    create_demo_map = Mock(return_value=game_map)
    create_clearing_map = Mock(return_value=clearing_map)
    create_session_score = Mock(return_value=session_score)
    create_session_statistics = Mock(return_value=session_statistics)
    score_item_collection = Mock(return_value=100)
    score_guide_objective_completion = Mock(return_value=500)
    resolve_profile_path = Mock(return_value=profile_path)
    load_player_profile = Mock(return_value=player_profile)
    persist_profile = Mock()
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
    create_profile_scene = Mock(return_value=profile_scene)

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
        "SessionStatistics",
        create_session_statistics,
    )
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
    monkeypatch.setattr(
        game_main,
        "get_profile_path",
        resolve_profile_path,
    )
    monkeypatch.setattr(
        game_main,
        "load_profile",
        load_player_profile,
    )
    monkeypatch.setattr(
        game_main,
        "save_profile",
        persist_profile,
    )
    monkeypatch.setattr(game_main, "GameplayScene", create_gameplay_scene)
    monkeypatch.setattr(game_main, "Application", create_application)
    monkeypatch.setattr(game_main.pygame, "Surface", create_surface)
    monkeypatch.setattr(game_main, "Animation", create_animation)
    monkeypatch.setattr(game_main, "DefeatScene", create_defeat_scene)
    monkeypatch.setattr(game_main, "VictoryScene", create_victory_scene)
    monkeypatch.setattr(game_main, "PauseScene", create_pause_scene)
    monkeypatch.setattr(game_main, "DialogueScene", create_dialogue_scene)
    monkeypatch.setattr(game_main, "ProfileScene", create_profile_scene)

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

    show_profile = create_title_scene.call_args.args[3]

    create_profile_scene.assert_called_once()
    profile_args = create_profile_scene.call_args.args

    assert profile_args[:3] == (
        font_cache,
        player_profile,
        input_state,
    )
    assert callable(profile_args[3])

    show_profile()

    scene_manager.change_scene.assert_called_once_with(profile_scene)
    scene_manager.change_scene.reset_mock()

    create_victory_scene.assert_not_called()
    create_session_statistics.assert_not_called()

    resolve_profile_path.assert_called_once_with()
    load_player_profile.assert_called_once_with(profile_path)
    player_profile.record_game_started.assert_not_called()
    persist_profile.assert_not_called()

    start_game()

    player_profile.record_game_started.assert_called_once_with()
    persist_profile.assert_called_once_with(
        profile_path,
        player_profile,
    )

    create_session_statistics.assert_called_once_with()

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

    assert defeat_args[:4] == (
        font_cache,
        session_score,
        session_statistics,
        input_state,
    )
    assert callable(defeat_args[4])

    return_to_title = defeat_args[4]

    create_victory_scene.assert_called_once()
    victory_args = create_victory_scene.call_args.args

    assert victory_args[:4] == (
        font_cache,
        session_score,
        session_statistics,
        input_state,
    )
    assert victory_args[4] is return_to_title

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
    gameplay_kwargs = create_gameplay_scene.call_args.kwargs

    assert gameplay_kwargs["input_state"] is input_state
    assert gameplay_kwargs["font_cache"] is font_cache
    assert gameplay_kwargs["session_score"] is session_score
    assert gameplay_kwargs["game_map"] is game_map
    assert callable(gameplay_kwargs["on_pause_requested"])
    assert callable(gameplay_kwargs["on_player_defeated"])
    assert callable(gameplay_kwargs["on_npc_interacted"])
    assert callable(gameplay_kwargs["on_npc_target_reached"])
    assert callable(gameplay_kwargs["on_enemy_defeated"])
    assert callable(gameplay_kwargs["on_item_collected"])
    assert callable(gameplay_kwargs["on_obstacle_destroyed"])
    assert callable(gameplay_kwargs["on_wall_touched"])
    assert gameplay_kwargs["player_idle_animation"] is player_idle_animation
    assert gameplay_kwargs["player_movement_animation"] is player_movement_animation
    assert gameplay_kwargs["player_collection_animation"] is player_collection_animation
    assert gameplay_kwargs["player_attack_animation"] is player_attack_animation

    guide_objective = gameplay_kwargs["guide_objective"]

    assert isinstance(guide_objective, GuideObjective)
    assert guide_objective.total_items == (
        len(game_map.collectibles) + len(clearing_map.collectibles)
    )
    assert callable(gameplay_kwargs["on_map_exit_reached"])

    request_pause = gameplay_kwargs["on_pause_requested"]

    handle_player_defeated = gameplay_kwargs["on_player_defeated"]

    handle_wall_touched = gameplay_kwargs["on_wall_touched"]

    handle_wall_touched(WallTouched(wall_id="wall-top"))

    assert clearing_caretaker.movement_target is initial_caretaker_target
    assert clearing_caretaker.movement_target_entity is None

    handle_wall_touched(WallTouched(wall_id="clearing-wall-top"))

    assert clearing_caretaker.movement_target is None
    assert clearing_caretaker.movement_target_entity is game_map.player.entity

    handle_npc_target_reached = gameplay_kwargs["on_npc_target_reached"]

    handle_npc_target_reached(
        NPCTargetReached(
            npc_id="npc-1",
            target_id="player",
        )
    )

    assert clearing_caretaker.movement_target_entity is game_map.player.entity
    create_dialogue_scene.assert_not_called()

    handle_npc_target_reached(
        NPCTargetReached(
            npc_id="npc-clearing-caretaker",
            target_id="player",
        )
    )

    assert clearing_caretaker.movement_target_entity is None
    create_dialogue_scene.assert_called_once()
    scene_manager.change_scene.assert_called_with(dialogue_scene)

    caretaker_arrival_dialogue_args = create_dialogue_scene.call_args.args

    assert caretaker_arrival_dialogue_args[:4] == (
        font_cache,
        input_state,
        clearing_caretaker.name,
        game_main.CARETAKER_WALL_TOUCHED_DIALOGUE_LINES,
    )

    return_to_dirty_wall = caretaker_arrival_dialogue_args[4]

    assert callable(return_to_dirty_wall)

    return_to_dirty_wall()

    assert clearing_caretaker.movement_target is None
    assert clearing_caretaker.movement_target_entity is clearing_wall

    handle_npc_target_reached(
        NPCTargetReached(
            npc_id="npc-clearing-caretaker",
            target_id="clearing-wall-top",
        )
    )

    assert clearing_caretaker.movement_target_entity is None
    assert create_dialogue_scene.call_count == 1
    scene_manager.change_scene.assert_called_with(gameplay_scene)

    create_dialogue_scene.reset_mock()

    resume_game = pause_args[2]

    request_pause()
    scene_manager.change_scene.assert_called_with(pause_scene)

    resume_game()
    scene_manager.change_scene.assert_called_with(gameplay_scene)

    handle_npc_interacted = gameplay_kwargs["on_npc_interacted"]

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
    assert guide_objective.state is GuideObjectiveState.NOT_STARTED
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

    handle_item_collected = gameplay_kwargs["on_item_collected"]
    event = ItemCollected(item_id="collectible-1")

    collectible.active = False
    handle_item_collected(event)

    assert guide_objective.collected_items == 1
    assert guide_objective.state is GuideObjectiveState.ACTIVE

    clearing_event = ItemCollected(item_id="collectible-clearing-1")
    clearing_collectible.active = False

    handle_item_collected(clearing_event)

    assert guide_objective.collected_items == 2
    assert guide_objective.state is GuideObjectiveState.READY_TO_COMPLETE
    assert session_statistics.record_item_collected.call_count == 2

    player_event = PlayerDefeated(player_id="player")
    handle_player_defeated(player_event)

    player_profile.record_game_finished.assert_called_once_with(
        score=700,
        statistics=session_statistics,
        victory=False,
    )
    assert persist_profile.call_args_list == [
        call(profile_path, player_profile),  # Session started
        call(profile_path, player_profile),  # Session finished
    ]

    return_to_title()

    handle_enemy_defeated = gameplay_kwargs["on_enemy_defeated"]
    first_enemy_event = EnemyDefeated(enemy_id="enemy-1")

    handle_enemy_defeated(first_enemy_event)

    assert call(victory_scene) not in scene_manager.change_scene.call_args_list

    second_enemy.entity.active = False
    second_enemy_event = EnemyDefeated(enemy_id="enemy-2")

    handle_enemy_defeated(second_enemy_event)

    assert call(victory_scene) not in (scene_manager.change_scene.call_args_list)

    assert guide_objective.state is GuideObjectiveState.READY_TO_COMPLETE

    assert session_statistics.record_enemy_defeated.call_count == 2

    handle_map_exit_reached = gameplay_kwargs["on_map_exit_reached"]
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

    assert player_profile.record_game_finished.call_count == 1

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

    handle_obstacle_destroyed = gameplay_kwargs["on_obstacle_destroyed"]
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
    session_statistics.record_obstacle_destroyed.assert_called_once_with()

    second_game_map = Mock()
    second_game_map.map_id = "demo"
    second_game_map.exits = ()
    second_clearing_map = Mock()
    second_clearing_map.map_id = "clearing"
    second_clearing_map.player = second_game_map.player
    second_clearing_collectible = Mock()
    second_clearing_collectible.active = False
    second_clearing_map.collectibles = (second_clearing_collectible,)
    second_clearing_wall = Mock()
    second_clearing_wall.entity_id = "clearing-wall-top"
    second_clearing_map.walls = (second_clearing_wall,)
    second_clearing_caretaker = Mock()
    second_clearing_caretaker.entity.entity_id = "npc-clearing-caretaker"
    second_clearing_caretaker.movement_target = Mock()
    second_clearing_caretaker.movement_target_entity = None
    second_clearing_map.npcs = (second_clearing_caretaker,)
    second_collectible = Mock()
    second_collectible.active = False
    second_enemy = Mock()
    second_enemy.entity.active = True
    second_game_map.enemies = (second_enemy,)
    second_game_map.collectibles = (second_collectible,)
    second_session_score = Mock()
    second_session_score.value = 400
    second_session_statistics = Mock(spec=SessionStatistics)
    second_gameplay_scene = Mock()
    second_defeat_scene = Mock()
    second_victory_scene = Mock()
    second_pause_scene = Mock()
    second_player_frames = tuple(Mock() for _ in range(8))
    second_player_animations = tuple(Mock() for _ in range(4))

    create_demo_map.return_value = second_game_map
    create_clearing_map.return_value = second_clearing_map
    create_session_score.return_value = second_session_score
    create_session_statistics.return_value = second_session_statistics
    create_gameplay_scene.return_value = second_gameplay_scene
    create_defeat_scene.return_value = second_defeat_scene
    create_victory_scene.return_value = second_victory_scene
    create_pause_scene.return_value = second_pause_scene
    create_surface.side_effect = second_player_frames
    create_animation.side_effect = second_player_animations

    start_game()

    assert player_profile.record_game_started.call_count == 2
    assert persist_profile.call_args_list == [
        call(profile_path, player_profile),  # First session started
        call(profile_path, player_profile),  # First session finished
        call(profile_path, player_profile),  # Second session started
    ]
    assert create_demo_map.call_count == 2
    assert create_clearing_map.call_count == 2
    assert create_session_score.call_count == 2
    assert create_session_statistics.call_count == 2
    assert create_gameplay_scene.call_count == 2
    assert create_defeat_scene.call_count == 2
    assert create_victory_scene.call_count == 2
    assert create_pause_scene.call_count == 2

    assert create_clearing_map.call_args_list == [
        call(game_map.player),
        call(second_game_map.player),
    ]

    second_gameplay_kwargs = create_gameplay_scene.call_args.kwargs

    assert second_gameplay_kwargs["input_state"] is input_state
    assert second_gameplay_kwargs["font_cache"] is font_cache
    assert second_gameplay_kwargs["session_score"] is second_session_score
    assert second_session_statistics is not session_statistics
    assert second_gameplay_kwargs["game_map"] is second_game_map
    assert second_gameplay_kwargs["on_pause_requested"] is not request_pause
    assert second_gameplay_kwargs["on_player_defeated"] is not handle_player_defeated
    assert (
        second_gameplay_kwargs["player_idle_animation"],
        second_gameplay_kwargs["player_movement_animation"],
        second_gameplay_kwargs["player_collection_animation"],
        second_gameplay_kwargs["player_attack_animation"],
    ) == second_player_animations

    second_guide_objective = second_gameplay_kwargs["guide_objective"]

    assert isinstance(second_guide_objective, GuideObjective)
    assert second_guide_objective is not guide_objective
    assert second_guide_objective.total_items == (
        len(second_game_map.collectibles) + len(second_clearing_map.collectibles)
    )
    assert callable(second_gameplay_kwargs["on_map_exit_reached"])
    assert second_gameplay_kwargs["on_map_exit_reached"] is not handle_map_exit_reached

    second_defeat_args = create_defeat_scene.call_args.args

    assert second_defeat_args[:4] == (
        font_cache,
        second_session_score,
        second_session_statistics,
        input_state,
    )
    assert second_defeat_args[4] is return_to_title

    second_victory_args = create_victory_scene.call_args.args

    assert second_victory_args[:4] == (
        font_cache,
        second_session_score,
        second_session_statistics,
        input_state,
    )
    assert second_victory_args[4] is second_defeat_args[4]
    assert second_victory_args[4] is return_to_title

    second_pause_args = create_pause_scene.call_args.args

    assert second_pause_args[:2] == (
        font_cache,
        input_state,
    )
    assert second_pause_args[2] is not resume_game

    second_guide_objective = second_guide_objective
    second_guide_objective.start()
    second_guide_objective.record_item_collected()
    second_guide_objective.record_item_collected()
    second_guide_objective.complete()

    second_handle_enemy_defeated = second_gameplay_kwargs["on_enemy_defeated"]
    second_enemy_event = EnemyDefeated(enemy_id="second-enemy")

    second_handle_enemy_defeated(second_enemy_event)

    assert call(second_victory_scene) not in (scene_manager.change_scene.call_args_list)

    second_enemy.entity.active = False
    second_handle_enemy_defeated(second_enemy_event)

    scene_manager.change_scene.assert_called_with(second_victory_scene)

    assert player_profile.record_game_finished.call_args_list == [
        call(
            score=700,
            statistics=session_statistics,
            victory=False,
        ),
        call(
            score=400,
            statistics=second_session_statistics,
            victory=True,
        ),
    ]
    assert persist_profile.call_args_list == [
        call(profile_path, player_profile),
        call(profile_path, player_profile),
        call(profile_path, player_profile),
        call(profile_path, player_profile),
    ]

    assert scene_manager.change_scene.call_args_list == [
        call(gameplay_scene),
        call(dialogue_scene),  # Caretaker arrival
        call(gameplay_scene),  # Caretaker returns to dirty
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

    second_handle_map_exit_reached = second_gameplay_kwargs["on_map_exit_reached"]
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


def test_save_player_profile_logs_storage_error(
    monkeypatch,
    caplog,
) -> None:
    profile_path = Mock()
    player_profile = Mock(spec=PlayerProfile)
    persist_profile = Mock(side_effect=OSError("disk full"))

    monkeypatch.setattr(
        game_main,
        "save_profile",
        persist_profile,
    )

    with caplog.at_level(
        logging.WARNING,
        logger=game_main.__name__,
    ):
        game_main._save_player_profile(
            profile_path,
            player_profile,
        )

    persist_profile.assert_called_once_with(
        profile_path,
        player_profile,
    )
    assert "Unable to save player profile" in caplog.text
