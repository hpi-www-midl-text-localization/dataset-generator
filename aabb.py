import numpy as np


class AABB:

    def __init__(self, position=(0, 0), width=0, height=0):
        self.position = position
        self.width = width
        self.height = height

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
        return (self.position[0] - (self.width/2.0), self.position[1] - (self.height/2.0))

    @property
    def bottom_right(self):
        return (self.position[0] + (self.width/2.0), self.position[1] + (self.height/2.0))
