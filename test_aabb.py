import pytest
from aabb import AABB


def test_constructor():
    aabb = AABB((0, 0), (10, 10))

    # AABBs with an empty area are allowed
    aabb = AABB((0, 0), (0, 0))
    aabb = AABB((0, 0), (10, 0))

    # AABBs with floats as their co-ordinates are allowed
    aabb = AABB((0.1, 0.1), (0.9, 0.9))

    # AABBs which have their bottom_right above and/or to the left of their top_left are not allowed
    with pytest.raises(ValueError):
        aabb = AABB((10, 10), (0, 0))

    # AABBs should only be constructed with integers or floats as the top_left and bottom_right co-ordinate components
    with pytest.raises(TypeError):
        aabb = AABB((0, '0'), "10.6, 10")


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

    # Edge case: two AABBs that share exactly one edge should not be considered intersecting
    aabb2 = AABB((20, 0), (40, 30))
    assert(not aabb1.intersects(aabb2))

    # Edge case: two AABBs that share exactly one point should not be considered intersecting
    aabb2 = AABB((20, 30), (40, 60))
    assert(not aabb1.intersects(aabb2))

    with pytest.raises(TypeError):
        aabb1.intersects("Not a word")


def test_inside():
    aabb1 = AABB((0, 0), (50, 30))
    aabb2 = AABB((0, 0), (20, 30))
    assert(not aabb1.inside(aabb2))
    assert(aabb2.inside(aabb1))

    # Edge case: AABBs should be considered "inside" AABBs of the exact same dimensions (and vice-versa)
    aabb2 = aabb1
    assert (aabb1.inside(aabb2))
    assert (aabb2.inside(aabb1))

    with pytest.raises(TypeError):
        aabb1.inside("Not a word")


def test_scale():
    scaled_aabb = AABB((0, 0), (20, 30)).scale(0.5)
    assert(scaled_aabb.bottom_right[0] == 15)
    assert(scaled_aabb.bottom_right[1] == 22.5)
    assert(scaled_aabb.top_left[0] == 5)
    assert(scaled_aabb.top_left[1] == 7.5)

    scaled_aabb = AABB((-10, -10), (10, 10)).scale(2)
    assert (scaled_aabb.bottom_right[0] == 20)
    assert (scaled_aabb.bottom_right[1] == 20)
    assert (scaled_aabb.top_left[0] == -20)
    assert (scaled_aabb.top_left[1] == -20)

    # Edge case: Scaling an AABB by factor 1.0 should not change its dimensions
    identically_scaled_aabb = AABB((0, 0), (20, 30)).scale(1.0)
    assert (identically_scaled_aabb.bottom_right[0] == 20)
    assert (identically_scaled_aabb.bottom_right[1] == 30)
    assert (identically_scaled_aabb.top_left[0] == 0)
    assert (identically_scaled_aabb.top_left[1] == 0)

    with pytest.raises(TypeError):
        AABB((0, 0), (10, 10)).scale('up')

def test_widht_height():
    aabb = AABB((0, 0), (50, 30))
    assert(aabb.width == 50)
    assert(aabb.height == 30)

    aabb = AABB((0, 0), (10, 0))
    assert (aabb.width == 10)
    assert (aabb.height == 0)

    aabb = AABB((0, 0), (0.1, 0.1))
    assert (aabb.width == 0.1)
    assert (aabb.height == 0.1)


if __name__ == "__main__":
    test_constructor()
    test_intersects()
    test_scale()
    test_inside()
