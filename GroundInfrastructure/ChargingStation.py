from .GroundInfrastructure import GroundInfrastructure
from .Vendor import Vendor
import json
from PySmartSkies.Models.Vendor import Vendor as SmartSkiesVendor

class ChargingStation(GroundInfrastructure, Vendor):
    """
    A charging station.
    """

    @staticmethod
    def from_json(json_string) -> 'ChargingStation':
        """
        Creates a charging station from a json string.
        :param json_string: The json string.
        :return: The charging station.
        """
        charging_station = json.loads(json_string)
        return ChargingStation(charging_station['id'], charging_station['name'], [charging_station['lon'], charging_station['lat']], charging_station['max_storing_capacity'], charging_station['max_charging_capacity'])

    def to_json(self) -> str:
        """
        Returns the charging station as a json string.
        :return: The charging station as a json string.
        """
        return json.dumps({"id": self.get_id(), "name": self.get_name(), "lon": self.get_lonlat()[0], "lat": self.get_lonlat()[1], "max_storing_capacity": self.get_max_storing_capacity(), "max_charging_capacity": self.get_max_charging_capacity(), "type": self.get_type()})
        
    @staticmethod
    def from_smartskies_vendor(vendor: SmartSkiesVendor) -> 'ChargingStation':
        """
        Creates a charging station from a smart skies vendor.
        :param vendor: The smart skies vendor.
        :return: The charging station.
        """
        MAX_STORING_CAPACITY = 100
        MAX_CHARGING_CAPACITY = 100
        
        return ChargingStation(vendor.vendor_id, vendor.name, [vendor.location_long, vendor.location_lat], MAX_STORING_CAPACITY, MAX_CHARGING_CAPACITY)

    def __init__(self, id, name, lonlat, max_storing_capacity, max_charging_capacity):
        """
        Initialises a charging station.
        :param id: The id of the charging station.
        :param name: The name of the charging station.
        :param lonlat: The longitude and latitude of the charging station.
        :param max_storing_capacity: The storing capacity of the charging station.
        :param max_charging_capacity: The charging capacity of the charging station.
        """
        super().__init__(id, name, lonlat, type=GroundInfrastructure.TYPE_CHARGING_STATION)
        self.__max_storing_capacity = max_storing_capacity
        self.__max_charging_capacity = max_charging_capacity
        self.__currently_storing = []
        self.__currently_charging = []
        
    def get_max_storing_capacity(self) -> int:
        """
        Returns the storing capacity of the charging station.
        :return: The storing capacity.
        """
        return self.__max_storing_capacity
    
    def get_current_storing_capacity(self) -> int:
        """
        Returns the current storing capacity of the charging station.
        :return: The current storing capacity.
        """
        return self.__max_storing_capacity - len(self.__currently_storing)

    def get_current_charging_capacity(self) -> int:
        """
        Returns the current charging capacity of the charging station.
        :return: The current charging capacity.
        """
        return self.__max_charging_capacity - len(self.__currently_charging)

    def get_max_charging_capacity(self) -> int:
        """
        Returns the charging capacity of the charging station.
        :return: The charging capacity.
        """
        return self.__max_charging_capacity

    def __repr__(self) -> str:
        return f'<ChargingStation|id={self.get_id()},name={self.get_name()},lonlat={self.get_lonlat()}>'

    # Vendor methods

    def get_vendor_id(self) -> int:
        """
        Returns the id of the charging station.
        :return: The id.
        """
        return self.get_id()


    