from abc import ABC


class Skill(ABC):
    def __init__(self, name, damage, stamina):
        self.name = name
        self.damage = damage
        self.stamina = stamina


skill_kick = Skill(name="Свирепый пинок", damage=12, stamina=6)
skill_sting = Skill(name="Мощный укол", damage=15, stamina=5)





