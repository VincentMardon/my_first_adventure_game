from dataclasses import dataclass

from my_first_adventure_game.game.statistics import SessionStatistics


@dataclass(slots=True)
class PlayerProfile:
    """Store statistics accumulated across game sessions.

    Attributes:
        games_started: Number of game sessions started.
        games_finished: Number of sessions ending in victory or defeat.
        victories: Number of sessions ending in victory.
        best_score: Highest final session score.
        total_score: Score accumulated across finished sessions.
        items_collected: Items collected across finished sessions.
        obstacles_destroyed: Obstacles destroyed across finished sessions.
        enemies_defeated: Enemies defeated across finished sessions.
        wall_stains_cleaned: Wall stains cleaned across finished sessions.
    """

    games_started: int = 0
    games_finished: int = 0
    victories: int = 0
    best_score: int = 0
    total_score: int = 0
    items_collected: int = 0
    obstacles_destroyed: int = 0
    enemies_defeated: int = 0
    wall_stains_cleaned: int = 0

    def record_game_started(self) -> None:
        """Record the start of one game session."""
        self.games_started += 1

    def record_game_finished(
        self,
        score: int,
        statistics: SessionStatistics,
        *,
        victory: bool,
    ) -> None:
        """Accumulate the result of one finished game session."""
        self.games_finished += 1

        if victory:
            self.victories += 1

        self.best_score = max(self.best_score, score)
        self.total_score += score
        self.items_collected += statistics.items_collected
        self.obstacles_destroyed += statistics.obstacles_destroyed
        self.enemies_defeated += statistics.enemies_defeated
        self.wall_stains_cleaned += statistics.wall_stains_cleaned
