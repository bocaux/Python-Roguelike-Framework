class CharacterClass(object):
    def __init__(self, uid, name, level_tree, experience_penalty=0):
        self.uid = uid
        self.name = name
        self.level_tree = level_tree
        self.experience_penalty = experience_penalty


class CharacterClassInstance(object):
    def __init__(self, template, experience_pool):
        self.template = template
        self.experience_pool = experience_pool

    @property
    def name(self):
        return self.template.name

    @property
    def level_tree(self):
        return self.template.level_tree
