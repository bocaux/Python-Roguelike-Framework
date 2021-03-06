class Equipment(object):
    """
    This component attaches itself to anything with a body.
    It represents equipment worn or wielded
    """
    def __init__(self, host):
        self.host = host
        self.host_body = host.body
        self.worn_equipment_map = {}
        self.wielded_equipment_map = {}

    def wear(self, item):
        # Wearing requires the bodypart to be compatible with the item
        if item.stats.size == self.host.stats.size:
            for compatible_bodypart_uid in item.wearable_bodyparts_uid:
                host_body_part = self.host_body.get_body_part(compatible_bodypart_uid)
                if host_body_part:
                    if host_body_part in self.worn_equipment_map:
                        if item.worn_layer not in [item.worn_layer for item in self.worn_equipment_map[host_body_part]]:
                            self.worn_equipment_map[host_body_part].append(item)
                            return True
                    else:
                        self.worn_equipment_map[host_body_part] = [item]
                        return True
        return False

    def wield(self, item):
        # Wielding requires bodyparts with GRASP
        grasp_able_body_parts = self.host_body.get_grasp_able_body_parts()
        # Wielding with one hand gets priority
        two_hands_wielders = []
        for grasp_able_body_part in grasp_able_body_parts:
            if grasp_able_body_part in self.wielded_equipment_map:
                continue

            # 10 is the normal relative_size for a hand
            relative_size_modifier = grasp_able_body_part.relative_size - 10
            relative_size_modifier = round(relative_size_modifier / 10) if relative_size_modifier else 0
            relative_size = self.host.stats.size + relative_size_modifier
            item_size = int(item.stats.size)
            if relative_size >= item_size >= relative_size - 2:
                # Can be wielded in one "hands"
                self.wielded_equipment_map[grasp_able_body_part] = item
                return True
            elif relative_size < item_size <= relative_size + 2:
                # Can be wielded in two "hands"
                two_hands_wielders.append(grasp_able_body_part)

        if len(two_hands_wielders) >= 2:
            first_wield = two_hands_wielders[0]
            second_wield = two_hands_wielders[1]
            self.wielded_equipment_map[first_wield] = item
            self.wielded_equipment_map[second_wield] = item
            return True

        return False

    def get_worn_items(self):
        return [item for item_list in self.worn_equipment_map.values() for item in item_list]

    def get_wielded_items(self):
        return [item for item in self.wielded_equipment_map.values()]
