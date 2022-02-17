from GroundInfrastructure.GroundInfrastructureHelpers import ground_infrastructure_from_json
from .GroundInfrastructure import GroundInfrastructure
from typing import List, Any, Dict
import json

class Mission():
    """
    Represents a mission.
    A mission is serialisable into a JSON string.
    A mission is deserialisable from a JSON string.
    Contains fields:
    - operation_id
    """
    def __init__(self, operation_id, origin: GroundInfrastructure, destination: GroundInfrastructure, payload: Dict[str, Any]):
        """
        Initialises a mission.
        :param operation_id: The operation id.
        :param origin: The origin.
        :param destination: The destination.
        """
        self.__operation_id = str(operation_id)
        self.__origin = origin
        self.__destination = destination
        self.__payload = payload

    def get_origin(self):
        """
        Returns the mission's origin.
        :return: The mission's origin.
        """
        return self.__origin

    def get_payload(self):
        """
        Returns the mission's payload.
        :return: The mission's payload.
        """
        return self.__payload

    def get_destination(self):
        """
        Returns the mission's destination.
        :return: The mission's destination.
        """
        return self.__destination

    def get_operation_id(self):
        """
        Returns the operation id.
        :return: The operation id.
        """
        return self.__operation_id

    def to_json(self):
        """
        Serialises the mission into a JSON string.
        :return: The mission as a JSON string.
        """
        return json.dumps({
            'operation_id': self.__operation_id,
            'origin': self.__origin.to_json(),
            'destination': self.__destination.to_json(),
            'payload': self.__payload
        })

    @staticmethod
    def from_json(json_string):
        """
        Deserialises a mission from a JSON string.
        :param json_string: The JSON string.
        :return: The mission.
        """
        mission = json.loads(json_string)
        return Mission(mission['operation_id'], ground_infrastructure_from_json(mission['origin']), ground_infrastructure_from_json(mission['destination']), mission['payload'])

    def __str__(self):
        """
        Returns a string representation of the mission.
        :return: The string representation.
        """
        return "Mission(operation_id={})".format(self.__operation_id)