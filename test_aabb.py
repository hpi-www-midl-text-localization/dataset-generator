import pytest
from aabb import AABB


def test_intersects():
    aabb1 = AABB((0, 0), 20, 30)
    aabb2 = AABB((0, 0), 20, 30)
    assert(aabb1.intersects(aabb2))
    aabb2 = AABB((100, 100), 10, 10)
    assert(not aabb1.intersects(aabb2))
    aabb2 = AABB((-5, -5), 10, 10)
    assert(aabb1.intersects(aabb2))
    aabb2 = AABB((5, 5), 10, 10)
    assert(aabb1.intersects(aabb2))
    aabb2 = AABB((-5, 5), 10, 10)
    assert(aabb1.intersects(aabb2))
    aabb2 = AABB((5, -5), 10, 10)
    assert(aabb1.intersects(aabb2))


def test_scale():
    scaled_aabb = AABB((0, 0), 20, 30).scale(0.5)
    assert(scaled_aabb.width == 10)
    assert(scaled_aabb.height == 15)
