import pytest
from main import *
from PIL import Image

def test_testenv():
    assert(True)

def test_calculate_word_aabb():
    font = ImageFont.truetype("fonts/open-sans/OpenSans-Regular.ttf", 12)
    image = Image.new("RGB", (100, 100))
    assert(calculate_word_aabb("test", (0,0),font,image),((0, 0, 21, 13), 21))
