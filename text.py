from PIL import Image, ImageDraw
from word import Word
from random import randint, randrange
from PIL import ImageFont
from aabb import AABB
from itertools import chain


class Text:
    def __init__(self):
        self.lines = []

    def __iter__(self):
        for line in self.lines:
            for word in line:
                yield word

    def generate_words(self, words, font, font_size, color, line_max_count=3):
        line_count = randint(1, line_max_count)
        lines = [[] for _ in range(line_count)]
        for word in words:
            lines[randrange(line_count)].append(word)

        font = ImageFont.truetype(font, font_size)
        white_space_width, white_space_height = font.getsize(" ")
        pos_y = 0
        for line in lines:
            word_line = []
            pos_x = 0
            max_height = white_space_height
            for raw_word in line:
                word = Word(raw_word, font, color, (pos_x, pos_y))
                pos_x += word.width + white_space_width
                max_height = max(max_height, word.height)
                word_line.append(word)
            self.lines.append(word_line)
            pos_y += max_height + 1
        self.calculate_aabb()

    def calculate_aabb(self):
        top_left = None
        bottom_right = None
        for word in self:
            if(top_left is None):
                top_left = word.aabb.top_left
            else:
                top_left = (min(top_left[0], word.aabb.top_left[0]), min(top_left[1], word.aabb.top_left[1]))
            if(bottom_right is None):
                bottom_right = word.aabb.bottom_right
            else:
                bottom_right = (max(bottom_right[0], word.aabb.bottom_right[0]), max(bottom_right[1], word.aabb.bottom_right[1]))
        width = bottom_right[0]-top_left[0]
        height = bottom_right[1]-top_left[1]
        self.aabb = AABB((top_left[0]+(width/2), top_left[1]+(height/2)), width, height)

    def draw(self, position, image_draw, debug=False):
        if(debug):
            top_left = self.aabb.top_left
            top_left = (top_left[0]+position[0], top_left[1]+position[1])
            bottom_right = self.aabb.bottom_right
            bottom_right = (position[0]+bottom_right[0], position[1]+bottom_right[1])
            image_draw.rectangle([bottom_right, top_left], outline=(0, 0, 255))
        for word in self:
            word.draw(position, image_draw, debug)


if __name__ == "__main__":
    text = Text()
    text.generate_words(["test", "Hello", "World", "This", "nice"], "fonts/Roboto/Roboto-Regular.ttf", 20, (255, 0, 0))
    image = Image.new("RGB", (400, 400))
    draw = ImageDraw.Draw(image)
    text.draw((100, 100), draw, True)
    image.save("test.png")
