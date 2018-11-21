from aabb import AABB
import numpy as np


class Word:
    def __init__(self, content, font, color, top_left):
        self.content = content
        self.aabb = AABB(top_left, top_left)
        self.font = font
        self.color = color

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
        return self._font

    @font.setter
    def font(self, font):
        self._font = font
        width, height = font.getsize(self.content)
        self.aabb.bottom_right = (self.aabb.top_left[0] + width, self.aabb.top_left[1] + height)

    def overlaps(self, value):
        if(isinstance(value, AABB)):
            return self.aabb.intersects(value)
        else:
            return self.aabb.intersects(value.aabb)

    def get_scaled_aabb(self, scale=0.4):
        return self.aabb.scale(scale)

    def draw(self, image_draw, debug=False):
        top_left = self.aabb.top_left
        if(debug):
            bottom_right = self.aabb.bottom_right
            image_draw.rectangle([bottom_right, top_left], outline=(128, 128, 128))
        image_draw.text(top_left, self.content, self.color, font=self.font)
