import json
from .Hospital import Hospital
from .ChargingStation import ChargingStation
from .GroundInfrastructure import GroundInfrastructure

def ground_infrastructure_from_json(json_object):
    """
    Deserialises a ground infrastructure from a JSON object or equivalent dict.
    :param json_object: The JSON object or equivalent dict.
    :return: The ground infrastructure.
    """
    ground_infrastructure = json_object
    _type = ground_infrastructure['type']
    if _type == GroundInfrastructure.TYPE_CHARGING_STATION:
        return ChargingStation.from_json(json_object)
    elif _type == GroundInfrastructure.TYPE_HOSPITAL:
        return Hospital.from_json(json_object)
    else:
        raise Exception(f'Unknown ground infrastructure type: {_type}')