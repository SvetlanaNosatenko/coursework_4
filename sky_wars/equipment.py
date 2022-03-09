import random
from dataclasses import dataclass
from typing import List


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    def damage(self) -> float:
        damage = round(random.uniform(self.min_damage, self.max_damage), 1)
        return damage


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]

    def get_weapon(self, weapon_name: str) -> Weapon:
        for weapon in self.weapons:
            if weapon.name == weapon_name:
                return weapon
        print("Такого оружия нет")

    def get_armor(self, armor_name: str) -> Armor:
        for armor in self.armors:
            if armor.name == armor_name:
                return armor
        print("Такой брони нет")

    def get_weapon_names(self) -> List[str]:
        return [item.name for item in self.weapons]

    def get_armor_names(self) -> List[str]:
        return [item.name for item in self.armors]
