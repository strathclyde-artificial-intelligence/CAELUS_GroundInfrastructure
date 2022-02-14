import json
from .Hospital import Hospital
from .ChargingStation import ChargingStation
from .GroundInfrastructure import GroundInfrastructure

def ground_infrastructure_from_json(json_string):
    """
    Deserialises a ground infrastructure from a JSON string.
    :param json_string: The JSON string.
    :return: The ground infrastructure.
    """
    ground_infrastructure = json.loads(json_string)
    _type = ground_infrastructure['type']
    if _type == GroundInfrastructure.TYPE_HOSPITAL:
        return Hospital.from_json(json_string)
    elif _type == GroundInfrastructure.TYPE_CHARGING_STATION:
        return ChargingStation.from_json(json_string)
    else:
        raise Exception(f'Unknown ground infrastructure type: {_type}')