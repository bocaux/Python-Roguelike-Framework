import random

from dungeon.chamber import Chamber, BlockedChamber, UnblockerChamber


class SimpleChamberRule(object):
    def __init__(self, size, max_neighbourgs, max_count):
        self.size = size
        self.max_neighbourg = max_neighbourgs
        self.max_count = max_count
        self.current_count = 0

    def generate(self, generator):
        chamber = self._generate()
        self.place(chamber, generator)
        self.current_count += 1

    def _generate(self):
        return Chamber(self.size, self.max_neighbourg)

    def place(self, chamber, generator):
        neighbour = random.choice(generator.chambers)
        neighbour.neighbours.append(chamber)

        chamber.neighbours.append(neighbour)
        chamber.weight = neighbour.weight + 1

    def reset(self):
        self.current_count = 0

    @property
    def is_completed(self):
        return self.current_count >= self.max_count


class BlockedChamberPairRule(SimpleChamberRule):
    def generate(self, generator):
        unblocker_chamber = UnblockerChamber(self.size, self.max_neighbourg)
        blocked_chamber = BlockedChamber(self.size, self.max_neighbourg)

        unblocker_chamber.linked_chamber = blocked_chamber
        blocked_chamber.linked_chamber = unblocker_chamber

        #  We need to place the unblocker chamber first to make sure that it is always reachable
        self.place(unblocker_chamber, generator)
        self.place(blocked_chamber, generator)
        self.current_count += 1
