import pytest
from text import Text
from functools import reduce


def test_generate_words():
    text = Text((0, 0))
    assert(not text.lines)
    words = ["test", "Hello", "World", "This", "nice"]
    text.generate_words(words, "fonts/open-sans/OpenSans-Regular.ttf", 10, (255, 0, 0))
    assert(text.lines)
    assert(reduce((lambda x, y: x + y), map(len, text.lines)) == len(words))
    for word1 in text:
        for word2 in text:
            if (word1 is not word2):
                assert(not word1.overlaps(word2))
            else:
                assert(word1.overlaps(word2))
