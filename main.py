from random import randrange, choice, seed
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import click


def render_line_and_return_aabb(image, xy, words_in_line, font=None, color=(255, 255, 255)):
    """Renders a text using ImageDraw.text() and returns its AABB.

    The resulting AABB is in the following format:
    (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
    The AABB's bottom_right coordinates may be outside of the actual
    ImageDraw's image's dimensions.
    """
    if font is None:
        font = ImageFont.truetype("fonts/open-sans/OpenSans-Regular.ttf", 12)

    draw = ImageDraw.Draw(image)

    top_left = xy
    space_size = font.getsize(" ")[0]
    bounding_boxes = []

    for word in words_in_line:
        width, height = font.getsize(word)
        bottom_right = (min(top_left[0] + width, image.width), min(top_left[1] + height, image.height))
        bounding_boxes.append((top_left[0], top_left[1], bottom_right[0], bottom_right[1]))

        draw.text(top_left, word + " ", font=font, fill=color)
        top_left = (top_left[0] + width + space_size, top_left[1])

        if top_left[0] >= image.width:
            break

    return bounding_boxes


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
    text = [choice(word_list) for _ in range(word_count)]

    font_size = randrange(min_font_size, max_font_size + 1, 2)  # use only even font sizes
    font = ImageFont.truetype("fonts/open-sans/OpenSans-Regular.ttf", font_size)

    return render_line_and_return_aabb(image, (x, y), text, font=font, color=text_color)


@click.command()
@click.option("--width", "-w", default=256, help="Width of generated output images.")
@click.option("--height", "-h", default=256, help="Height of generated output images.")
@click.option("--words", "--wordsfile", default='words.txt', help="Path to list of words to be used for generation.", type=click.Path(exists=True))
@click.option("--seed", "-s", "userseed", type=click.INT, help="Seed for generating random numbers.")
def main(width, height, wordsfile, userseed):
    """Image generator for text localization. Generates images with words and their corresponding AABB's."""
    if userseed is not None:
        seed(userseed)

    image = Image.new("RGB", (width, height))

    words = np.loadtxt(wordsfile, dtype=np.dtype(str), delimiter="\n")

    rand_color = (randrange(255), randrange(255), randrange(255))

    bboxes = render_random_words_at_random_position_and_return_aabb(image, words, text_color=rand_color)

    for bbox in bboxes:
        print(bbox)

    image.show()


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    main()