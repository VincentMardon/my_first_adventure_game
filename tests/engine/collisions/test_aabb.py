import pytest

from my_first_adventure_game.engine.collisions import AABB


def test_aabb_exposes_its_edges() -> None:
    bounds = AABB(
        x=10.5,
        y=20.25,
        width=30.0,
        height=40.0,
    )

    assert bounds.left == 10.5
    assert bounds.right == 40.5
    assert bounds.top == 20.25
    assert bounds.bottom == 60.25


def test_overlaps_returns_true_for_intersecting_bounds() -> None:
    first = AABB(x=0.0, y=0.0, width=10.0, height=10.0)
    second = AABB(x=5.0, y=4.0, width=10.0, height=10.0)

    assert first.overlaps(second)
    assert second.overlaps(first)


@pytest.mark.parametrize(
    "second",
    [
        AABB(x=10.0, y=0.0, width=10.0, height=10.0),
        AABB(x=-10.0, y=0.0, width=10.0, height=10.0),
        AABB(x=0.0, y=10.0, width=10.0, height=10.0),
        AABB(x=0.0, y=-10.0, width=10.0, height=10.0),
    ],
)
def test_overlaps_returns_false_when_bounds_only_touch(
    second: AABB,
) -> None:
    first = AABB(x=0.0, y=0.0, width=10.0, height=10.0)

    assert not first.overlaps(second)


@pytest.mark.parametrize(
    ("width", "height"),
    [(-1.0, 10.0), (10.0, -1.0)],
)
def test_aabb_rejects_negative_dimensions(
    width: float,
    height: float,
) -> None:
    with pytest.raises(ValueError, match="dimensions"):
        AABB(x=0.0, y=0.0, width=width, height=height)


@pytest.mark.parametrize(
    "empty",
    [
        AABB(x=5.0, y=0.0, width=0.0, height=10.0),
        AABB(x=0.0, y=5.0, width=10.0, height=0.0),
    ],
)
def test_zero_area_bounds_do_not_overlap(empty: AABB) -> None:
    bounds = AABB(x=0.0, y=0.0, width=10.0, height=10.0)

    assert not empty.overlaps(bounds)
    assert not bounds.overlaps(empty)
