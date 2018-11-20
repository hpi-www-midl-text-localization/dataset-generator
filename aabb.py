import numpy as np


class AABB:
    @classmethod
    def fromPositionAndSize(cls, position, width, height):
        aabb = AABB()
        aabb.position = position
        aabb.width = width
        aabb.height = height
        return aabb

    def intersects(self, aabb):
        if(not isinstance(aabb, AABB)):
            raise ValueError("Argument must be a of type AABB")
        selfHalfWidth = self.width / 2
        selfHalfHeight = self.height / 2
        aabbHalfWidth = aabb.width / 2
        aabbHalfHeight = aabb.height / 2
        return not (self.position[0] - selfHalfWidth > aabb.position[0] + aabbHalfWidth or
                    self.position[0] + selfHalfWidth < aabb.position[0] - aabbHalfWidth or
                    self.position[1] - selfHalfHeight > aabb.position[1] + aabbHalfHeight or
                    self.position[1] + selfHalfHeight < aabb.position[1] - aabbHalfHeight)

    def scale(self, ratio=0.4):
        return self.fromPositionAndSize(self.position, self.width * ratio, self.height * ratio)
