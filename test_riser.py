import pytest
from build123d import Vector

from riser import print_pose, riser


def test_riser() -> None:
    part = riser()
    bb = part.bounding_box()
    assert part.is_valid
    assert len(part.solids()) == 1
    assert bb.size.X == pytest.approx(42.0, abs=0.01)
    assert bb.size.Y == pytest.approx(11.0, abs=0.01)
    assert bb.size.Z == pytest.approx(23.3, abs=0.01)
    assert bb.min.Z == pytest.approx(-6.0, abs=0.01)
    assert bb.max.Z == pytest.approx(17.3, abs=0.01)
    assert 2715 < part.volume < 2755
    assert not part.is_inside(Vector(17.5, 5.5, 5.0))
    assert part.is_inside(Vector(17.5, 0.6, 5.0))
    assert part.is_inside(Vector(17.5, 5.5, 0.6))
    assert not part.is_inside(Vector(17.5, 10.5, 5.0))
    assert part.is_inside(Vector(17.5, 10.5, 9.4))
    assert not part.is_inside(Vector(17.5, 5.5, 12.65))
    assert part.is_inside(Vector(17.5, 5.5, 16.3))
    assert part.is_inside(Vector(1.0, 5.5, 12.65))
    assert not part.is_inside(Vector(39.0, 5.5, 12.65))
    assert not part.is_inside(Vector(17.5, 0.5, 12.65))
    assert not part.is_inside(Vector(32.0, 5.5, 15.0))
    assert part.is_inside(Vector(41.0, 5.5, 14.3))
    assert not part.is_inside(Vector(41.0, 5.5, 13.0))
    assert part.is_inside(Vector(41.0, 5.5, 16.3))
    assert not part.is_inside(Vector(41.0, 5.5, 9.5))
    assert not part.is_inside(Vector(39.0, 5.5, 14.3))
    assert not part.is_inside(Vector(17.5, 5.5, 15.0))


def test_print_pose() -> None:
    posed = print_pose(riser())
    bb = posed.bounding_box()
    assert posed.is_valid
    assert bb.min.Z == pytest.approx(0.0, abs=0.01)
    assert (bb.min.X + bb.max.X) / 2 == pytest.approx(0.0, abs=0.01)
    assert (bb.min.Y + bb.max.Y) / 2 == pytest.approx(0.0, abs=0.01)
    assert bb.size.X == pytest.approx(42.0, abs=0.01)
    assert bb.size.Y == pytest.approx(23.3, abs=0.01)
    assert bb.size.Z == pytest.approx(11.0, abs=0.01)
    assert posed.is_inside(Vector(0.0, 7.15, 0.5))
    assert not posed.is_inside(Vector(0.0, 0.65, 10.5))
    assert posed.is_inside(Vector(0.0, -3.75, 10.5))
    assert posed.is_inside(Vector(0.0, -10.65, 5.5))
    assert not posed.is_inside(Vector(0.0, -7.0, 5.5))
    assert posed.is_inside(Vector(20.0, -8.65, 5.5))
    assert not posed.is_inside(Vector(20.0, -7.35, 5.5))
