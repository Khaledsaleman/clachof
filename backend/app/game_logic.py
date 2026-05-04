import random
from . import models
import datetime

def calculate_battle_result(attacker: models.User, defender: models.User):
    attacker_power = sum(u.level * u.count for u in attacker.units)
    defender_power = sum(b.level * 2 for b in defender.buildings if b.type in ["cannon", "archer_tower"])
    attacker_roll = attacker_power * random.uniform(0.8, 1.2)
    defender_roll = defender_power * random.uniform(0.8, 1.2)
    was_win = attacker_roll > defender_roll
    gold_looted = 0
    if was_win:
        gold_looted = defender.gold * 0.2
        defender.gold -= gold_looted
        attacker.gold += gold_looted
    for unit in attacker.units:
        unit.count = int(unit.count * 0.9)
    return {
        "was_win": was_win,
        "gold_looted": gold_looted,
        "attacker_power": attacker_power,
        "defender_power": defender_power,
        "units_remaining": {u.type: u.count for u in attacker.units}
    }

def regenerate_energy(user: models.User):
    now = datetime.datetime.now(datetime.timezone.utc)
    if user.last_energy_regen:
        last_regen = user.last_energy_regen
        if last_regen.tzinfo is None:
             last_regen = last_regen.replace(tzinfo=datetime.timezone.utc)
        diff = now - last_regen
        minutes = diff.total_seconds() / 60
        energy_to_add = int(minutes / 5)
        if energy_to_add > 0:
            user.energy = min(user.max_energy, user.energy + energy_to_add)
            user.last_energy_regen = now
    else:
        user.last_energy_regen = now
