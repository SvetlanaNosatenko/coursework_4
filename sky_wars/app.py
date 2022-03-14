from functools import wraps
from typing import Dict

from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

from sky_wars.arena import Arena
from sky_wars.classes import hero_classes
from sky_wars.equipment import EquipmentData
from sky_wars.get_data import _data_equipment
from sky_wars.unit import Player, BaseUnit, Enemy

app = Flask(__name__)
app.url_map.strict_slashes = False

EQUIPMENT: EquipmentData = _data_equipment()
heroes: Dict[str, BaseUnit] = dict()

arena = Arena()


def game_processing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if arena.game_is_on:
            return func(*args, **kwargs)
        if arena.results:
            return render_template('fight.html', heroes=heroes, result=arena.results)
        return redirect(url_for("index"))
    return wrapper


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/choose-hero/', methods=["GET", "POST"])
def choose_hero():
    if request.method == 'GET':
        return render_template('hero_choosing.html',
                               header="Выберите героя",
                               classes=hero_classes.values(),
                               result=_data_equipment(),
                               next_button="Выбрать врага")
    elif request.method == 'POST':
        heroes["player"] = Player(unit=hero_classes[request.form['unit_class']],
                                  weapon=EQUIPMENT.get_weapon(request.form['weapon']),
                                  armor=EQUIPMENT.get_armor(request.form['armor']),
                                  name=request.form["name"])

    return redirect(url_for('choose_enemy'), 301)


@app.route('/choose-enemy/', methods=["GET", "POST"])
def choose_enemy():
    if request.method == 'GET':
        return render_template('hero_choosing.html',
                               header="Выберите врага",
                               classes=hero_classes.values(),
                               result=_data_equipment(),
                               next_button="Начать бой")
    elif request.method == 'POST':
        heroes["enemy"] = Enemy(unit=hero_classes[request.form['unit_class']],
                                weapon=EQUIPMENT.get_weapon(request.form['weapon']),
                                armor=EQUIPMENT.get_armor(request.form['armor']),
                                name=request.form["name"])
    return redirect(url_for('start_game'))


@app.route('/fight/')
def start_game():
    if "player" in heroes and "enemy" in heroes:
        arena.game_run(**heroes)
        return render_template('fight.html', heroes=heroes, result="Бой начался!")
    return redirect(url_for('index'))


@app.route('/fight/hit')
@game_processing
def hit():
    return render_template('fight.html', heroes=heroes, result=arena.player_hit())


@app.route('/fight/use-skill')
@game_processing
def use_skill():
    return render_template('fight.html', heroes=heroes, result=arena.use_skill())


@app.route('/fight/pass-turn')
@game_processing
def pass_turn():
    return render_template('fight.html', heroes=heroes, result=arena.next_step())


@app.route('/fight/end-fight')
def end_fight():
    return redirect(url_for('index'))


if __name__ == '__main__':
     app.run(debug=True)
