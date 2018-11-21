import pytest
from PIL import ImageFont
from word import Word


@pytest.fixture(scope="session")
def font():
    return ImageFont.truetype("fonts/open-sans/OpenSans-Regular.ttf", 12)


def test_overlaps(font):
    word1 = Word("test", font, (255, 255, 255), (0, 0))
    word2 = Word("test", font, (255, 255, 255), (0, 0))
    assert(word1.overlaps(word2))
    word2 = Word("test", font, (255, 255, 255), (0, 2 * word1.height))
    assert(not word1.overlaps(word2))


if __name__ == "__main__":
    test_overlaps(ImageFont.truetype("fonts/open-sans/OpenSans-Regular.ttf", 12))
