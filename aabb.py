import numpy as np


class AABB:

    def __init__(self, position=(0, 0), width=0, height=0):
        self._position = position
        self._width = width
        self._height = height
        self._invalidate()

    def intersects(self, aabb):
        if(not isinstance(aabb, AABB)):
            raise ValueError("Argument must be a of type AABB")
        self_half_width = self.width / 2
        self_half_height = self.height / 2
        aabb_half_width = aabb.width / 2
        aabb_half_height = aabb.height / 2
        return not (self.position[0] - self_half_width > aabb.position[0] + aabb_half_width or
                    self.position[0] + self_half_width < aabb.position[0] - aabb_half_width or
                    self.position[1] - self_half_height > aabb.position[1] + aabb_half_height or
                    self.position[1] + self_half_height < aabb.position[1] - aabb_half_height)

    def scale(self, ratio=0.4):
        return AABB(self.position, self.width * ratio, self.height * ratio)

    @property
    def top_left(self):
        if(self._top_left is None):
            self._top_left = (self.position[0] - (self.width/2.0), self.position[1] - (self.height/2.0))
        return self._top_left

    @property
    def bottom_right(self):
        if(self._bottom_right is None):
            self._bottom_right = (self.position[0] + (self.width/2.0), self.position[1] + (self.height/2.0))
        return self._bottom_right

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._invalidate()
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._invalidate()
        self._height = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._invalidate()
        self._position = value

    def _invalidate(self):
        self._bottom_right = None
        self._top_left = None
