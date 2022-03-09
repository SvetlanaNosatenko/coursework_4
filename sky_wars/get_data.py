import json
from typing import Union

import marshmallow
import marshmallow_dataclass

from sky_wars.equipment import EquipmentData


def get_json() -> Union[dict, list]:
    with open('equipment.json', 'r', encoding="utf-8") as f:
        data_equipment = json.load(f)
    return data_equipment


def _data_equipment() -> EquipmentData:
    try:
        EquipmentSchema = marshmallow_dataclass.class_schema(EquipmentData)
        return EquipmentSchema().load(data=get_json())
    except marshmallow.exceptions.ValidationError:
        raise ValueError
