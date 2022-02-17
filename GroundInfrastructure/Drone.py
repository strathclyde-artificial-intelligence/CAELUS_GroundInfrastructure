from .Mission import Mission
from typing import Optional
import json

class Drone():
    
    TYPE_QUADROTOR = 'QUADROTOR'
    TYPE_EVTOL_FW = 'EVTOL_FW'

    AVAILABLE = 'AVAILABLE'
    RESERVED = 'RESERVED'
    MISSION = 'MISSION'
    MAINTEINANCE = 'MAINTEINANCE'

    """
    Represents a drone.
    The sqlite schema for a drone is as follows:
    
    CREATE TABLE IF NOT EXISTS Drones (
        id INTEGER PRIMARY KEY,
        type TEXT NOT NULL,
        state TEXT NOT NULL,
        reservation_token TEXT,
        mission_id INTEGER,
        mission_json TEXT
    )

    A drone can have various states:
    - AVAILABLE
    - RESERVED
    - MISSION
    - MAINTEINANCE

    * Drones can be serialised into a SQLite row.
    * Drones can be deserialised from a SQLite row.
    * Drones can be printed.
    """
    
    @staticmethod
    def from_sqlite(sqlite_row):
        """
        Deserialises a drone from a SQLite row.

        :param sqlite_row: The SQLite row.
        :return: The drone.
        """
        mission_json = sqlite_row[5] if len(sqlite_row) > 5 else None
        mission = Mission.from_json(mission_json) if mission_json is not None else None
        drone = Drone(sqlite_row[0], sqlite_row[1], sqlite_row[6], state=sqlite_row[2])
        drone.__reservation_token = sqlite_row[3]
        drone.__mission = mission
        return drone
        
    def to_sqlite(self):
        """
        Serialises the drone into a SQLite row.

        :return: The drone as a SQLite row.
        """
        mission_json = json.loads(self.__mission.to_json()) if self.__mission is not None else None
        return (
            self.__drone_id,
            self.__type,
            self.__state,
            self.get_reservation_token(),
            mission_json['operation_id'] if mission_json is not None and 'operation_id' in mission_json else None,
            json.dumps(mission_json) if mission_json is not None else None,
            self.__config_name)

    def __init__(self, drone_id, type, config_name, state = AVAILABLE):
        """
        Initialises a drone.

        :param drone_id: The drone's ID.
        :param state: The drone's state.
        """
        self.__drone_id = str(drone_id)
        self.__type = type
        self.__state = state
        self.__mission: Mission = None
        self.__reservation_token = None
        self.__config_name = config_name

    def get_reservation_token(self):
        """
        Returns the reservation token.

        :return: The reservation token.
        """
        return self.__reservation_token

    def get_drone_id(self):
        """
        Returns the drone's ID.

        :return: The drone's ID.
        """
        return self.__drone_id

    def get_state(self):
        """
        Returns the drone's state.

        :return: The drone's state.
        """
        return self.__state

    def reserve(self, reservation_token):
        """
        Reserves the drone.

        :param reservation_token: The reservation token.
        """
        self.__state = Drone.RESERVED
        self.__reservation_token = reservation_token
    
    def get_mission(self):
        """
        Returns the drone's mission.

        :return: The drone's mission.
        """
        return self.__mission
        
    def assign_mission(self, mission, reservation_token):
        """
        Assigns the drone to a mission.

        :param mission: The mission.
        :param reservation_token: The reservation token.
        """
        reservation_token = str(reservation_token)
        if self.__reservation_token == reservation_token:
            self.__mission = mission
            self.__state = Drone.MISSION
        else:
            raise Exception('Invalid reservation token.')
    
    def release_drone(self, reservation_token):
        """
        Releases the drone from reserved state.

        :param reservation_token: The reservation token.
        """
        reservation_token = str(reservation_token)
        if self.__reservation_token == reservation_token:
            self.__state = Drone.AVAILABLE
            self.__reservation_token = None
            self.__remove_mission_details()
        else:
            raise Exception('Invalid reservation token.')

    def __remove_mission_details(self):
        """
        Removes the mission details from the drone.
        """
        self.__mission = None

    def put_drone_in_mainteinance(self):
        """
        Drone must not be in reserved state
        Drone must not be in mainteinance state
        """
        if self.__state == Drone.RESERVED:
            raise Exception('Drone is reserved.')
        elif self.__state == Drone.MAINTEINANCE:
            raise Exception('Drone is already in mainteinance.')
        else:
            self.__state = Drone.MAINTEINANCE
            self.__remove_mission_details()
            self.__reservation_token = None

    def return_drone_from_mainteinance(self):
        """
        Returns the drone from mainteinance.
        """
        self.__state = Drone.AVAILABLE
        self.__reservation_token = None
        self.__remove_mission_details()

    def __str__(self):
        """
        Returns a string representation of the drone.

        :return: The drone as a string.
        """
        return 'Drone: ' + str(self.__drone_id) + ' ' + str(self.__state)
    
    def get_type(self):
        """
        Returns the drone's type.

        :return: The drone's type.
        """
        return self.__type

    def get_config_name(self):
        """
        Returns the drone's config name.

        :return: The drone's config name.
        """
        return self.__config_name
