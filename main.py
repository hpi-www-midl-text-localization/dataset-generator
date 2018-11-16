from random import randrange, choice
import numpy as np
from PIL import Image, ImageFont, ImageDraw


def render_text_and_return_aabb(draw, xy, text, font=None, color=(255, 255, 255)):
    """Renders a text using ImageDraw.text() and returns its AABB.

    The resulting AABB is in the following format:
    (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
    The AABB's bottom_right coordinates may be outside of the actual
    ImageDraw's image's dimensions.
    """
    if font is None:
        font = ImageFont.truetype("fonts/open-sans/OpenSans-Regular.ttf", 12)

    width, height = font.getsize(text)
    draw.text(xy, text, font=font, fill=color)

    return (xy[0], xy[1], xy[0] + width, xy[1] + height)


def render_random_words_at_random_position_and_return_aabb(image,
                                                           word_list,
                                                           min_word_count=1,
                                                           max_word_count=3,
                                                           min_font_size=8,
                                                           max_font_size=24,
                                                           text_color=(255, 255, 255)):
    """Renders a random single-line text at a random position and
    allows to set minima and maxima for the text length and for the
    font size. Returns the AABB of the resulting text.

    For the AABB specifics, see render_text_and_return_aabb().
    """
    image_width, image_height = image.size
    x = randrange(image_width + 1)
    y = randrange(image_height + 1)

    word_count = randrange(min_word_count, max_word_count + 1)
    text = ' '.join([choice(word_list) for i in range(word_count)])

    font_size = randrange(min_font_size, max_font_size + 1, 2)  # use only even font sizes
    font = ImageFont.truetype("fonts/open-sans/OpenSans-Regular.ttf", font_size)

    draw = ImageDraw.Draw(image)

    return render_text_and_return_aabb(draw, (x, y), text, font=font, color=text_color)


image_width = 256
image_height = 256

image = Image.new("RGB", (image_width, image_height))

words = np.loadtxt('words.txt', dtype=np.dtype(str), delimiter="\n")

rand_color = (randrange(255), randrange(255), randrange(255))

top_left_x, top_left_y, bottom_right_x, bottom_right_y = render_random_words_at_random_position_and_return_aabb(image, words, text_color=rand_color)

print(top_left_x, top_left_y, bottom_right_x, bottom_right_y)

image.show()
