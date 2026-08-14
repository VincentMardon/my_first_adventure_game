import pygame

from my_first_adventure_game.engine.application import Application, WindowConfig
from my_first_adventure_game.engine.assets import FontCache
from my_first_adventure_game.engine.graphics import Animation
from my_first_adventure_game.engine.input import InputState
from my_first_adventure_game.engine.scenes import SceneManager
from my_first_adventure_game.game.entities import NPC
from my_first_adventure_game.game.events import (
    EnemyDefeated,
    ItemCollected,
    ObstacleDestroyed,
    PlayerDefeated,
)
from my_first_adventure_game.game.input import DEFAULT_KEYBOARD_BINDINGS
from my_first_adventure_game.game.levels import create_demo_map
from my_first_adventure_game.game.progression import (
    GuideObjective,
    GuideObjectiveState,
)
from my_first_adventure_game.game.scenes import (
    DefeatScene,
    DialogueScene,
    GameplayScene,
    PauseScene,
    TitleScene,
    VictoryScene,
)
from my_first_adventure_game.game.scoring import (
    SessionScore,
    guide_objective_completion_points,
    item_collection_points,
)

WINDOW_CONFIG = WindowConfig(title="My First Adventure Game", size=(1280, 720))
COLLECTION_ACTIVE_DIALOGUE_LINES = ("Find every item and return to me.",)
COLLECTION_COMPLETE_DIALOGUE_LINES = ("You found every item. Well done, traveler!",)
FRAMES_PER_SECOND = 60
PLAYER_FRAME_SIZE = (32, 32)
PLAYER_IDLE_COLORS = (
    (224, 196, 96),
    (240, 212, 112),
)
PLAYER_MOVEMENT_COLORS = (
    (240, 144, 72),
    (255, 184, 88),
)
PLAYER_IDLE_FRAME_DURATION = 0.4
PLAYER_MOVEMENT_FRAME_DURATION = 0.15
PLAYER_COLLECTION_COLORS = (
    (248, 248, 248),
    (112, 240, 160),
)
PLAYER_COLLECTION_FRAME_DURATION = 0.1
PLAYER_ATTACK_COLORS = (
    (248, 96, 96),
    (255, 176, 96),
)
PLAYER_ATTACK_FRAME_DURATION = 0.1


def main() -> None:
    """Compose the game services and start the application."""

    input_state = InputState(DEFAULT_KEYBOARD_BINDINGS)
    font_cache = FontCache(pygame)

    def start_game() -> None:
        game_map = create_demo_map()
        session_score = SessionScore()
        guide_objective = GuideObjective(
            total_items=len(game_map.collectibles),
        )
        player_idle_frames = tuple(
            pygame.Surface(PLAYER_FRAME_SIZE) for _ in PLAYER_IDLE_COLORS
        )
        player_movement_frames = tuple(
            pygame.Surface(PLAYER_FRAME_SIZE) for _ in PLAYER_MOVEMENT_COLORS
        )
        player_collection_frames = tuple(
            pygame.Surface(PLAYER_FRAME_SIZE) for _ in PLAYER_COLLECTION_COLORS
        )
        player_attack_frames = tuple(
            pygame.Surface(PLAYER_FRAME_SIZE) for _ in PLAYER_ATTACK_COLORS
        )

        for frame, color in zip(
            player_idle_frames,
            PLAYER_IDLE_COLORS,
            strict=True,
        ):
            frame.fill(color)

        for frame, color in zip(
            player_movement_frames,
            PLAYER_MOVEMENT_COLORS,
            strict=True,
        ):
            frame.fill(color)

        for frame, color in zip(
            player_collection_frames, PLAYER_COLLECTION_COLORS, strict=True
        ):
            frame.fill(color)

        for frame, color in zip(
            player_attack_frames,
            PLAYER_ATTACK_COLORS,
            strict=True,
        ):
            frame.fill(color)

        player_idle_animation = Animation(
            frames=player_idle_frames,
            frame_duration=PLAYER_IDLE_FRAME_DURATION,
        )
        player_movement_animation = Animation(
            frames=player_movement_frames,
            frame_duration=PLAYER_MOVEMENT_FRAME_DURATION,
        )
        player_collection_animation = Animation(
            frames=player_collection_frames,
            frame_duration=PLAYER_COLLECTION_FRAME_DURATION,
            loop=False,
        )

        player_attack_animation = Animation(
            frames=player_attack_frames,
            frame_duration=PLAYER_ATTACK_FRAME_DURATION,
            loop=False,
        )

        def return_to_title() -> None:
            scene_manager.change_scene(initial_scene)

        defeat_scene = DefeatScene(
            font_cache,
            session_score,
            input_state,
            return_to_title,
        )

        victory_scene = VictoryScene(
            font_cache,
            session_score,
            input_state,
            return_to_title,
        )

        def request_pause() -> None:
            scene_manager.change_scene(pause_scene)

        def resume_game() -> None:
            scene_manager.change_scene(gameplay_scene)

        def handle_npc_interacted(npc: NPC) -> None:
            if guide_objective.state is GuideObjectiveState.NOT_STARTED:
                for collectible in game_map.collectibles:
                    collectible.active = True

                dialogue_lines = npc.dialogue_lines
                guide_objective.start()
            elif guide_objective.state is GuideObjectiveState.ACTIVE:
                dialogue_lines = COLLECTION_ACTIVE_DIALOGUE_LINES
            elif guide_objective.state is GuideObjectiveState.READY_TO_COMPLETE:
                guide_objective.complete()
                session_score.add(guide_objective_completion_points())
                dialogue_lines = COLLECTION_COMPLETE_DIALOGUE_LINES
            else:
                dialogue_lines = COLLECTION_COMPLETE_DIALOGUE_LINES

            dialogue_scene = DialogueScene(
                font_cache,
                input_state,
                npc.name,
                dialogue_lines,
                resume_game,
            )
            scene_manager.change_scene(dialogue_scene)

        pause_scene = PauseScene(
            font_cache,
            input_state,
            resume_game,
        )

        def handle_player_defeated(
            _event: PlayerDefeated,
        ) -> None:
            scene_manager.change_scene(defeat_scene)

        def handle_enemy_defeated(
            _event: EnemyDefeated,
        ) -> None:
            if all(not enemy.entity.active for enemy in game_map.enemies):
                scene_manager.change_scene(victory_scene)

        def handle_item_collected(event: ItemCollected) -> None:
            session_score.add(item_collection_points(event))
            guide_objective.record_item_collected()

        def handle_obstacle_destroyed(
            _event: ObstacleDestroyed,
        ) -> None:
            pass

        gameplay_scene = GameplayScene(
            input_state,
            font_cache,
            session_score,
            game_map.player,
            request_pause,
            handle_player_defeated,
            game_map.walls,
            game_map.enemies,
            game_map.npcs,
            handle_npc_interacted,
            handle_enemy_defeated,
            game_map.collectibles,
            handle_item_collected,
            game_map.destructible_obstacles,
            handle_obstacle_destroyed,
            player_idle_animation,
            player_movement_animation,
            player_collection_animation,
            player_attack_animation,
            guide_objective,
        )

        scene_manager.change_scene(gameplay_scene)

    initial_scene = TitleScene(
        font_cache,
        input_state,
        start_game,
    )
    scene_manager = SceneManager(initial_scene)

    application = Application(
        window_config=WINDOW_CONFIG,
        scene_manager=scene_manager,
        input_processor=input_state,
        frames_per_second=FRAMES_PER_SECOND,
    )

    application.run()
