import random


class Chamber(object):
    """A dungeon chamber"""

    def __init__(self, size, max_neighbours):
        self.size = size
        self.max_neighbours = max_neighbours

        self.neighbours = []
        self.twins = []

        self.has_been_generated = False

        self.weight = 0

    @property
    def is_full(self):
        return len(self.max_neighbours) >= self.size

    def randomize(self):
        random.shuffle(self.neighbours)


class BlockedChamber(Chamber):
    def __init__(self, size, max_neighbours):
        super(BlockedChamber, self).__init__(size, max_neighbours)
        self.is_blocked = True

        self.linked_chamber = None


class UnblockerChamber(Chamber):
    def __init__(self, size, max_neighbours):
        super(UnblockerChamber, self).__init__(size, max_neighbours)
        self.linked_chamber = None
