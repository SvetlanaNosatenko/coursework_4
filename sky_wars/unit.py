from __future__ import annotations
import random
from abc import ABC
from typing import Optional, Type

from sky_wars.classes import UnitClass
from sky_wars.equipment import Weapon, Armor

REGENERATE_CONST = 3


class BaseUnit(ABC):
    def __init__(self, name, unit: Type[UnitClass], weapon: Weapon, armor: Armor):
        self.name = name
        self.unit = unit
        self._health = self.unit.max_health
        self._stamina = self.unit.max_stamina
        self.weapon = weapon
        self.armor = armor
        self.used_skill = False

    @property
    def health(self):
        return round(self._health, 1)

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def stamina(self):
        return round(self._stamina, 1)

    @stamina.setter
    def stamina(self, value):
        self._stamina = value

    @property
    def total_armor(self) -> float:
        if self.stamina - self.armor.stamina_per_turn >= 0:
            return round(self.armor.defence * self.unit.armor, 1)
        return 0

    def _hit(self, target: BaseUnit) -> Optional[float]:
        if self.stamina - self.weapon.stamina_per_hit < 0:
            return None

        unit_damage = self.weapon.damage() * self.unit.attack
        damage = unit_damage - target.total_armor
        if damage < 0:
            return 0
        self.stamina -= self.weapon.stamina_per_hit
        return round(damage, 1)

    def take_hit(self, damage: float):
        self.health -= damage
        self.stamina -= self.armor.stamina_per_turn
        if self.health < 0:
            self.health = 0

    def regenerate_stamina(self):
        delta_stamina = REGENERATE_CONST * self.unit.stamina
        if self.stamina + delta_stamina <= self.unit.stamina:
            self.stamina += delta_stamina
        else:
            self.stamina = self.unit.max_stamina

    def use_skill(self) -> Optional[float]:
        if not self.used_skill and self.stamina - self.unit.skill.stamina:
            self.used_skill = True
            return round(self.unit.skill.damage, 1)
        return None


class Enemy(BaseUnit):
    def hit(self, target: BaseUnit) -> Optional[float]:
        if random.randint(1, 100) < 10 and self.stamina >= self.unit.skill.stamina and not self.used_skill:
            self.use_skill()
        return self._hit(target)


class Player(BaseUnit):
    def hit(self, target: BaseUnit) -> Optional[float]:
        return self._hit(target)

