from random import randrange, choice
import string
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

    return xy[0], xy[1], xy[0] + width, xy[1] + height


def render_random_text_at_random_position_and_return_aabb(image,
                                                          min_text_length=2,
                                                          max_text_length=10,
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

    text_length = randrange(min_text_length, max_text_length + 1)
    characters = string.ascii_letters + string.digits
    text = ''.join([choice(characters) for _ in range(text_length)])

    font_size = randrange(min_font_size, max_font_size + 1, 2)  # use only even font sizes
    font = ImageFont.truetype("fonts/open-sans/OpenSans-Regular.ttf", font_size)

    draw = ImageDraw.Draw(image)

    return render_text_and_return_aabb(draw, (x, y), text, font=font, color=text_color)


def create_images_with_text_and_bounding_box(n, width, height):
    """Creates n images with text on them. The images will have the
    dimensions width x height. Returns generated images and the
    bounding boxes of the text on them.
    """
    images = []
    bounding_boxes = []

    for _ in range(0, n):
        image = Image.new("RGB", (width, height))

        rand_color = (randrange(255), randrange(255), randrange(255))

        bounding_boxes.append(render_random_text_at_random_position_and_return_aabb(image, text_color=rand_color))
        images.append(image)

    return images, bounding_boxes


image_width = 256
image_height = 256

images, bounding_boxes = create_images_with_text_and_bounding_box(10, image_width, image_height)

