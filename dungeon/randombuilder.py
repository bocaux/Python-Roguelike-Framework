import random

from dungeon.chamber import Chamber


class RandomDungeonGenerator(object):
    """
    Generates a dungeon. This does not generate the map but the concept of the map. The resulting
    objects will be converted to a map.
    """
    def __init__(self):
        self.rules = []
        self.chambers = []

    def add_root_chamber(self, size, max_neighbours):
        self.chambers.append(Chamber(size, max_neighbours))

    def add_rule(self, rule):
        self.rules.append(rule)

    def generate(self):
        rules = self.rules[:]
        while rules:
            rule = random.choice()
            rule.generate(self)
            if rule.is_completed:
                rules.remove(rule)
        return self.chambers

    def reset(self):
        for rule in self.rules:
            rule.reset()
        self.chambers = self.chambers[:1]
