from aabb import AABB


class Word:
    def __init__(self, content, font, position):
        self.content = content
        self.font = font
        self.position = position
        self.width, self.height = self.font.getsize(self.content)
        self._aabb = AABB.fromPositionAndSize(self.position, self.width, self.height)

    def getAABB(self):
        return self._aabb

    def overlaps(self, word):
        if(not isinstance(word, Word)):
            raise ValueError("Argument must be a of type Word")
        return self.getAABB().intersects(word.getAABB())
