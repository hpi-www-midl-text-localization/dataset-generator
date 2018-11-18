import pytest
from main import calculate_word_aabb
from PIL import Image, ImageFont

def test_testenv():
    assert True

@pytest.fixture(scope="session")
def font():
    return ImageFont.truetype("../fonts/open-sans/OpenSans-Regular.ttf", 12)

def test_calculate_word_aabb(font):
    image = Image.new("RGB", (100, 100))
    assert calculate_word_aabb("test", (0,0),font,image) == ((0, 0, 21, 13), 21)
