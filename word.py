from aabb import AABB
import numpy as np


class Word:
    def __init__(self, content, font, color, top_left):
        self.content = content
        self.aabb = AABB()
        self.font = font
        self.color = color
        self.position = (top_left[0] + self.width/2, top_left[1] - self.height/2)

    @property
    def position(self):
        return self.aabb.position

    @position.setter
    def position(self, position):
        self.aabb.position = position

    @property
    def width(self):
        return self.aabb.width

    @property
    def height(self):
        return self.aabb.height

    @property
    def font(self):
        self._font

    @font.setter
    def font(self, font):
        self._font = font
        self.aabb.width, self.aabb.height = font.getsize(self.content)

    def overlaps(self, word):
        if(not isinstance(word, Word)):
            raise ValueError("Argument must be a of type Word")
        return self.aabb.intersects(word.aabb)

    def get_scaled_aabb(self, scale=0.4):
        return self.aabb.scale(scale)

    def draw(self, position, image_draw):
        top_left = self.aabb.top_left
        image_draw.text((top_left[0]+position[0], top_left[1]+position[1]), self.content, self.color, self.font)
