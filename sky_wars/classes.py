from dataclasses import dataclass
from skills import Skill, skill_kick, skill_sting


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


class Warrior(UnitClass):
    name = 'Воин'
    max_health: float = 60.0
    max_stamina: float = 30.0
    attack: float = 0.8
    stamina: float = 0.9
    armor: float = 1.2
    skill: Skill = skill_kick


class Thief(UnitClass):
    name = 'Вор'
    max_health: float = 50.0
    max_stamina: float = 25.0
    attack: float = 1.5
    stamina: float = 1.2
    armor: float = 1.0
    skill: Skill = skill_sting


hero_classes = {Warrior.name: Warrior, Thief.name: Thief}

