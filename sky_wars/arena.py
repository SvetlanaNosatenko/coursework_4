from typing import Optional
from sky_wars.unit import BaseUnit


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=SingletonMeta):
    def __init__(self):
        self.results = ""
        self.player = None
        self.enemy = None
        self.game_is_on = False

    def game_run(self, player: BaseUnit, enemy: BaseUnit):
        self.player = player
        self.enemy = enemy
        self.game_is_on = True

    def next_step(self) -> str:
        if self.check_health():
            return self.check_health()

        if not self.game_is_on:
            return self.results

        dealt_damage = self.enemy.hit(self.player)
        if dealt_damage is not None:
            self.player.take_hit(dealt_damage)
            results = f"{self.enemy.name} нанес вам {dealt_damage} урона"
        else:
            results = f"У {self.enemy.name} недостаточно выносливости для удара"
        self.stamina_regenerate()
        return results

    def check_health(self) -> Optional[str]:
        if self.player._health <= 0 and self.enemy._health <= 0:
            return self.game_over(results="Игра окончена. Ничья")
        if self.player._health <= 0:
            return self.game_over(results="Игра окончена. Вы проиграли")
        if self.enemy._health <= 0:
            return self.game_over(results="Игра окончена. Победа!")

    def game_over(self, results: str) -> str:
        self.game_is_on = False
        self.results = results
        return results

    def stamina_regenerate(self):
        self.player.regenerate_stamina()
        self.enemy.regenerate_stamina()

    def player_hit(self) -> str:
        dealt_damage = self.player.hit(self.enemy)
        if dealt_damage is not None:
            self.enemy.take_hit(dealt_damage)
            return f"<p>Вы нанесли врагу {dealt_damage} урона</p><p>{self.next_step()}</p>"
        return f"<p>Недостаточно выносливости для удара</p><p>{self.next_step()}</p>"

    def use_skill(self) -> str:
        dealt_damage = self.player.use_skill()
        if dealt_damage is not None:
            self.enemy.take_hit(dealt_damage)
            return f"<p>Вы воспользовались умением и нанесли врагу {dealt_damage} " \
                   f"урона</p><p>{self.next_step()}</p>"
        return f"<p>Недостаточно выносливости для использования умений</p><p>{self.next_step()}</p>"


