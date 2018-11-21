from PIL import Image, ImageDraw
from word import Word
from random import randint, randrange
from PIL import ImageFont


class Text:
    def __init__(self):
        self.lines = []

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
            pos_y += max_height

    def draw(self, position, image_draw):
        for line in self.lines:
            for word in line:
                word.draw(position, image_draw)


if __name__ == "__main__":
    text = Text()
    text.generate_words(["test", "Hello", "World", "This", "nice"], "fonts/open-sans/OpenSans-Regular.ttf", 10, (255, 0, 0))
    image = Image.new("RGB", (400, 400))
    draw = ImageDraw.Draw(image)
    text.draw((100, 100), draw)
    image.save("test.png")
