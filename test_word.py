import pytest
from PIL import ImageFont
from word import Word
from aabb import AABB


@pytest.fixture(scope="session")
def font():
    return ImageFont.truetype("fonts/open-sans/OpenSans-Regular.ttf", 12)


def test_constructor(font):
    word = Word("test", font, (255, 255, 255), (0, 0))

    # Words with an empty content are allowed
    word = Word("", font, (255, 255, 255), (0, 0))

    # Words without an appropriate font are not allowed
    with pytest.raises(TypeError):
        word = Word("test", "OpenSans", (255, 255, 255), (0, 0))

    # Words with different types of colors are allowed
    # See ImageDraw.text() --> ImageDraw._getink()
    word = Word("test", font, 'red', (0, 0))
    word = Word("test", font, '#ff0000', (0, 0))

    # Words without an appropriate co-ordinate tupel for top_left are not allowed
    with pytest.raises(TypeError):
        word = word = Word("test", font, (255, 255, 255), (0, '0'))
    with pytest.raises(TypeError):
        word = word = Word("test", font, (255, 255, 255), None)

def test_overlaps(font):
    word1 = Word("test", font, (255, 255, 255), (0, 0))
    word2 = Word("test", font, (255, 255, 255), (0, 0))
    assert(word1.overlaps(word2))
    word2 = Word("test", font, (255, 255, 255), (0, 2 * word1.height))
    assert(not word1.overlaps(word2))

    assert(word1.overlaps(AABB((0, 0), (1, 1))))

    with pytest.raises(TypeError):
        word1.overlaps(None)

    with pytest.raises(TypeError):
        word1.overlaps()

    with pytest.raises(TypeError):
        word1.overlaps(((0, 0), (0, 1)))


if __name__ == "__main__":
    test_constructor(font())
    test_overlaps(font())
