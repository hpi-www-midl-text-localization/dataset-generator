import pytest
from aabb import AABB


def test_intersects():
    aabb1 = AABB((0, 0), (20, 30))
    aabb2 = AABB((0, 0), (20, 30))
    assert(aabb1.intersects(aabb2))
    aabb2 = AABB((100, 100), (200, 200))
    assert(not aabb1.intersects(aabb2))
    aabb2 = AABB((-5, -5), (10, 10))
    assert(aabb1.intersects(aabb2))
    aabb2 = AABB((5, 5), (10, 10))
    assert(aabb1.intersects(aabb2))
    aabb2 = AABB((-5, 5), (10, 10))
    assert(aabb1.intersects(aabb2))
    aabb2 = AABB((5, -5), (10, 10))
    assert(aabb1.intersects(aabb2))
    with pytest.raises(ValueError):
        aabb1.intersects("Not a word")


def test_inside():
    aabb1 = AABB((0, 0), (50, 30))
    aabb2 = AABB((0, 0), (20, 30))
    assert(not aabb1.inside(aabb2))
    assert(aabb2.inside(aabb1))
    with pytest.raises(ValueError):
        aabb1.inside("Not a word")


def test_scale():
    scaled_aabb = AABB((0, 0), (20, 30)).scale(0.5)
    assert(scaled_aabb.bottom_right[0] == 15)
    assert(scaled_aabb.bottom_right[1] == 22.5)
    assert(scaled_aabb.top_left[0] == 5)
    assert(scaled_aabb.top_left[1] == 7.5)


def test_widht_height():
    aabb = AABB((0, 0), (50, 30))
    assert(aabb.width == 50)
    assert(aabb.height == 30)


if __name__ == "__main__":
    test_intersects()
    test_scale()
    test_inside()
