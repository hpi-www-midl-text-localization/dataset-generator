from random import randrange, choice
import os
import numpy as np
from PIL import Image, ImageFont, ImageDraw


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


def create_images_with_text_and_bounding_box(n, word_list, width, height):
    """Creates n images with text on them. The images will have the
    dimensions width x height. Returns generated images and the
    bounding boxes of the text on them.
    """
    images = []
    bounding_boxes = []

    for _ in range(0, n):
        image = Image.new("RGB", (width, height))

        rand_color = (randrange(255), randrange(255), randrange(255))
        bounding_boxes.append(render_random_words_at_random_position_and_return_aabb(image, word_list, text_color=rand_color))
        images.append(image)

    return images, bounding_boxes


def save_image_dataset(images):
    """Saves the images and creates a text file that stores their
    locations. This allows the images to be loaded as a Chainer ImageDataset.
    """
    if not os.path.exists("./images"):
        os.makedirs("./images")

    image_paths = [f"./images/image_{i}.png" for i in range(0, len(images))]
    np.savetxt("image_locations.txt", image_paths, fmt="%s")

    for i in range(0, len(images)):
        images[i].save(image_paths[i])


image_width = 256
image_height = 256
image_count = 10
words = np.loadtxt('words.txt', dtype=np.dtype(str), delimiter="\n")

images, bounding_boxes = create_images_with_text_and_bounding_box(image_count, words, image_width, image_height)


save_image_dataset(images)
np.save("bounding_boxes.npy", bounding_boxes)
