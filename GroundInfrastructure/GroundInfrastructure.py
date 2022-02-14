from typing import Tuple
import json

class GroundInfrastructure():
    
    TYPE_GENERIC = 0
    TYPE_DRONE_BASE = 1
    TYPE_AIRPORT = 2
    TYPE_CHARGING_STATION = 3
    TYPE_HOSPITAL = 4

    def to_json(self):
        """
        Serialises the ground infrastructure into a JSON string.
        :return: The ground infrastructure as a JSON string.
        """
        return json.dumps({'id': self.__id, 'name': self.__name, 'lon': self.__lonlat[0], 'lat': self.__lonlat[1], 'type': self.__type})

    def __init__(self, id, name, lonlat: Tuple[float], type=TYPE_GENERIC):
        """
        Initialises a ground infrastructure.
        :param id: The ID.
        :param name: The name.
        :param type: The type.
        """
        self.__id = id
        self.__name = name
        self.__type = type
        self.__lonlat = lonlat

    def get_id(self):
        """
        Returns the ID.
        :return: The ID.
        """
        return self.__id
    
    def get_name(self):
        """
        Returns the name.
        :return: The name.
        """
        return self.__name
    
    def get_type(self):
        """
        Returns the type.
        :return: The type.
        """
        return self.__type

    def get_lonlat(self):
        """
        Returns the longitude and latitude.
        :return: The longitude and latitude.
        """
        return self.__lonlat
