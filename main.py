import os
from random import randrange, randint, choice, seed
import numpy as np
from PIL import Image, ImageDraw
import click
from aabb import AABB
from text import Text
from pathlib import Path


def grab_random_font():
    ff = [font.as_posix() for font in Path('fonts').glob('**/*.ttf')]
    return choice(ff)


def generate_text(
        word_list,
        top_left,
        min_word_count,
        max_word_count,
        min_font_size=8,
        max_font_size=24,
        text_color=(255, 255, 255)):
    """ Generate Text at the given top_left position and some random words from word_list.
        Chooses parameters randomly between min and max arguments.
    """
    word_count = randint(min_word_count, max_word_count)
    words = [choice(word_list) for _ in range(word_count)]

    font_size = randrange(min_font_size, max_font_size + 1, 2)  # use only even font sizes
    text = Text(top_left)
    text.generate_words(words, grab_random_font(), font_size, text_color)
    return text


def is_text_overlapping_with_text_or_image_boundaries(text, texts, image_aabb):
    if not text.aabb.scale(0.6).inside(image_aabb):
        return True
    for other_text in texts:
        if other_text.overlaps(text):
            return True
    return False


def create_images_with_text_and_bounding_box(
        n,
        word_list,
        width,
        height,
        min_text_count,
        max_text_count,
        min_word_count,
        max_word_count,
        debug=False):
    """Creates n images with text on them. The images will have the
    dimensions width x height. Returns generated images and the
    bounding boxes of the text on them.
    """
    images = []
    bounding_boxes = []

    for _ in range(0, n):
        image_color = (randrange(255), randrange(255), randrange(255))
        rl_image_color = relative_luminance(image_color)

        image = Image.new("RGB", (width, height), color=image_color)
        image_aabb = AABB((0, 0), (width, height))
        text_count = randint(min_text_count, max_text_count)
        texts = []
        current_boxes = []

        for i in range(text_count):
            rand_color = (randrange(255), randrange(255), randrange(255))
            rl_text_color = relative_luminance(rand_color)
            contrast_ratio = (max(rl_text_color, rl_image_color) + 0.05) / (min(rl_text_color, rl_image_color) + 0.05)

            while contrast_ratio <= 4.5:
                rand_color = (randrange(255), randrange(255), randrange(255))
                rl_text_color = relative_luminance(rand_color)
                contrast_ratio = (max(rl_text_color, rl_image_color) + 0.05) / (min(rl_text_color, rl_image_color) + 0.05)

            text = None
            tries = 0
            while True:
                tries += 1
                x = randrange(width + 1)
                y = randrange(height + 1)
                text = generate_text(
                    word_list, (x, y), min_word_count=min_word_count, max_word_count=max_word_count, text_color=rand_color)
                if not is_text_overlapping_with_text_or_image_boundaries(text, texts, image_aabb):
                    break
                if tries > 100:
                    raise Exception("Too many tries of placing a text with given parameters. Please try other parameters or a different seeding.")
            texts.append(text)
        for text in texts:
            current_boxes.extend(text.get_word_aabbs())
            text.draw(ImageDraw.Draw(image), debug=debug)
        images.append(image)
        bounding_boxes.append(current_boxes)

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


def relative_luminance(color):
    R = color[0]/255
    G = color[1]/255
    B = color[2]/255
    k = []

    for element in [R, G, B]:
        if element <= 0.03928:
            k.append(element / 12.92)
        else:
            k.append(((element + 0.055) / 1.055)**2.4)

    return 0.2126 * k[0] + 0.7152 * k[1] + 0.0722 * k[2]


@click.command()
@click.option("--width", "-w", default=256, help="Width of generated output images.")
@click.option("--height", "-h", default=256, help="Height of generated output images.")
@click.option("--count", "-c", default=10, help="Number of images to be generated.")
@click.option("--wordsfile", default='words.txt', help="Path to list of words to be used for generation.", type=click.Path(exists=True))
@click.option("--min_textcount", "-min_tc", default=1, help="Minimum number of texts in one image.")
@click.option("--max_textcount", "-max_tc", default=2, help="Maximum number of texts in one image.")
@click.option("--min_wordcount", "-min_wc", default=1, help="Minimum number of words per text.")
@click.option("--max_wordcount", "-max_wc", default=3, help="Maximum number of words per text.")
@click.option("--min_wordlength", "-min_wl", default=1, help="Minimum length of the words.")
@click.option("--max_wordlength", "-max_wl", default=50, help="Maximum length of the words.")
@click.option("--seed", "-s", "userseed", type=click.INT, help="Seed for generating random numbers.")
@click.option("--debug", "-d", "debug", is_flag=True, help="Generates debugging AABBs.")
def main(width, height, count, wordsfile, min_textcount, max_textcount, min_wordcount, max_wordcount, min_wordlength, max_wordlength, userseed, debug):
    """Image generator for text localization. Generates images with words and their corresponding AABB's."""
    if userseed is not None:
        seed(userseed)
    words = np.loadtxt(wordsfile, dtype=np.dtype(str), delimiter="\n")
    correct_length_words = list(filter(lambda x: max_wordlength >= len(x) >= min_wordlength, words))

    images, bounding_boxes = create_images_with_text_and_bounding_box(
        count, correct_length_words, width, height, min_text_count=min_textcount, max_text_count=max_textcount,
        min_word_count=min_wordcount, max_word_count=max_wordcount, debug=debug)

    save_image_dataset(images)
    np.save("bounding_boxes.npy", bounding_boxes)


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    main()
