import numpy as np


class AABB:

    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def intersects(self, aabb):
        if(not isinstance(aabb, AABB)):
            raise ValueError("Argument must be a of type AABB")
        x1 = min(self.bottom_right[0], aabb.bottom_right[0])
        y1 = min(self.bottom_right[1], aabb.bottom_right[1])

        x2 = max(self.top_left[0], aabb.top_left[0])
        y2 = max(self.top_left[1], aabb.top_left[1])
        return (x1 > x2 and y1 > y2)

    def inside(self, aabb):
        if(not isinstance(aabb, AABB)):
            raise ValueError("Argument must be a of type AABB")
        return (self.top_left[0] >= aabb.top_left[0] and self.top_left[1] >= aabb.top_left[1] and
                self.bottom_right[0] <= aabb.bottom_right[0] and self.bottom_right[1] <= aabb.bottom_right[1])

    def scale(self, ratio=0.4):
        diagonal = ((self.bottom_right[0]-self.top_left[0])/2.0, (self.bottom_right[1]-self.top_left[1])/2.0)
        position = (self.top_left[0] + diagonal[0], self.top_left[1] + diagonal[1])
        new_diagonal = (diagonal[0]*ratio, diagonal[1] * ratio)
        new_top_left = (position[0] - new_diagonal[0], position[1] - new_diagonal[1])
        new_bottom_right = (position[0] + new_diagonal[0], position[1] + new_diagonal[1])
        return AABB(new_top_left, new_bottom_right)

    @property
    def height(self):
        return self.bottom_right[1] - self.top_left[1]

    @property
    def width(self):
        return self.bottom_right[0] - self.top_left[0]
