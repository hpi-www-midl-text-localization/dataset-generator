from aabb import AABB
import numpy as np
from PIL import ImageFont, ImageDraw2


class Word:
    def __init__(self, content, font, color, top_left):
        if not isinstance(font, ImageFont.FreeTypeFont):
            raise TypeError('"font" argument has to be of type PIL.ImageFont.FreeTypeFont')

        self.content = content
        self.aabb = AABB(top_left, top_left)
        self.font = font
        self.color = color

    @property
    def position(self):
        return self.aabb.position

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
        if not isinstance(font, ImageFont.FreeTypeFont):
            raise TypeError('"font" argument has to be of type PIL.ImageFont.FreeTypeFont')

        self._font = font
        width, height = font.getsize(self.content)
        self.aabb.bottom_right = (self.aabb.top_left[0] + width, self.aabb.top_left[1] + height)

    def overlaps(self, value):
        try:
            if(isinstance(value, AABB)):
                return self.aabb.intersects(value)
            elif isinstance(getattr(value, 'aabb'), AABB):
                return self.aabb.intersects(value.aabb)
            else:
                raise TypeError('"value" argument has to be of type AABB or contain an "aabb" property of type AABB')
        except AttributeError:
            raise TypeError('"value" argument has to be of type AABB or contain an "aabb" property of type AABB')

    def get_scaled_aabb(self, scale):
        return self.aabb.scale(scale)

    def draw(self, image_draw, debug=False):
        top_left = self.aabb.top_left
        if(debug):
            bottom_right = self.aabb.bottom_right
            image_draw.rectangle([top_left, bottom_right], outline=(128, 128, 128))
        image_draw.text(top_left, self.content, self.color, font=self.font)
