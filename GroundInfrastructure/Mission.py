from typing import List
import json

class Mission():
    """
    Represents a mission.
    A mission is serialisable into a JSON string.
    A mission is deserialisable from a JSON string.
    Contains fields:
    - operation_id
    """
    def __init__(self, operation_id):
        """
        Initialises a mission.
        :param operation_id: The operation id.
        """
        self.__operation_id = str(operation_id)

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
        return json.dumps({'operation_id': self.__operation_id})

    @staticmethod
    def from_json(json_string):
        """
        Deserialises a mission from a JSON string.
        :param json_string: The JSON string.
        :return: The mission.
        """
        mission_json = json.loads(json_string) if json_string is not None else None
        return Mission(mission_json['operation_id']) if mission_json is not None else None

    def __str__(self):
        """
        Returns a string representation of the mission.
        :return: The string representation.
        """
        return "Mission(operation_id={})".format(self.__operation_id)