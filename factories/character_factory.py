from characters.character import Character
from characters.classes import CharacterClassInstance
from characters.race import RaceInstance
from components.stats import CharacterStats
from components.display import Display
from components.experience_pool import ExperiencePool
from components.inventory import Inventory


class CharacterFactory(object):
    """
    At first this will only instantiate templates but eventually it should be able
    to pump out variations of a template ex: Adjusted to match player level.
    """
    def __init__(self, character_templates, factory_service, race_templates, class_templates):
        self.character_templates = character_templates
        self.template_instance_count = {}
        self.factory_service = factory_service
        self.race_templates = race_templates
        self.class_templates = class_templates

    def build(self, uid):
        """
        Builds a characters instance from a template using the uid.
        :param uid: uid of the template to instantiate.
        :return: Built instance from template.
        """

        character_template = self.character_templates[uid]
        if character_template:
            return self._create_instance_of_template(character_template)
        else:
            raise Exception("Could not find template for UID " + uid)

    def create(self, name, class_uid, race_uid, stats, body_uid):
        """
        Creates a new character based on arguments
        :return:
        """
        uid = "player"
        race_experience_pool = ExperiencePool()
        class_experience_pool = ExperiencePool()
        race_experience_pool.add_child_pool(class_experience_pool)
        new_instance = Character(
            uid=uid,
            name=name,
            character_class=CharacterClassInstance(
                template=self.get_class_template_by_uid(class_uid),
                experience_pool=class_experience_pool
            ),
            character_race=RaceInstance(
                template=self.get_race_template_by_uid(race_uid),
                experience_pool=race_experience_pool
            ),
            stats=stats,
            display=Display((255, 255, 255), (0, 0, 0), "@"),
            body=self.factory_service.build_body_instance_by_uid(body_uid),
            main_experience_pool=race_experience_pool,
            inventory=Inventory()
        )

        return new_instance

    def _create_instance_of_template(self, character_template):
        instance_id = 0
        if character_template.uid in self.template_instance_count:
            instance_id = self.template_instance_count[character_template.uid]
            self.template_instance_count[character_template.uid] += 1
        else:
            self.template_instance_count[character_template.uid] = 1

        instance_uid = character_template.uid + "_" + str(instance_id)
        race_experience_pool = ExperiencePool()
        class_experience_pool = ExperiencePool()
        race_experience_pool.add_child_pool(class_experience_pool)
        new_instance = Character(
            uid=instance_uid,
            name=character_template.name,
            character_class=CharacterClassInstance(
                template=self.get_class_template_by_uid(character_template.class_uid),
                experience_pool=class_experience_pool
            ),
            character_race=RaceInstance(
                template=self.get_race_template_by_uid(character_template.race_uid),
                experience_pool=race_experience_pool
            ),
            stats=CharacterStats(**character_template.base_stats.__dict__),
            display=Display(**character_template.display.__dict__),
            body=self.factory_service.build_body_instance_by_uid(character_template.body_uid),
            main_experience_pool=race_experience_pool,
            inventory=Inventory()
        )

        return new_instance

    def get_class_template_by_uid(self, uid):
        if uid in self.class_templates:
            return self.class_templates[uid]

    def get_race_template_by_uid(self, uid):
        if uid in self.race_templates:
            return self.race_templates[uid]
