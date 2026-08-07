from my_first_adventure_game.game.scoring import SessionScore


def test_session_score_starts_at_zero() -> None:
    score = SessionScore()

    assert score.value == 0


def test_add_accumulates_points() -> None:
    score = SessionScore()

    score.add(100)
    score.add(50)

    assert score.value == 150
