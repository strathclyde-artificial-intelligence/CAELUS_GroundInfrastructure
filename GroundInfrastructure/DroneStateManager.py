from typing import List, Tuple
from uuid import uuid4
from .Drone import Drone
from .Exceptions import WrongStateTransition, InvalidToken
from .DBAdapter import DBAdapter

class DroneStateManager():
    @staticmethod
    def from_sqlite(adapter: DBAdapter):
        """
        Creates a DroneStateManager from a DBAdapter.

        :param adapter: The DBAdapter.
        :return: The DroneStateManager.
        """
        manager = DroneStateManager(adapter)
        for drone in adapter.get_drones():
            manager.add_drone(Drone.from_sqlite(drone))
        return manager

    def __init__(self, db_adapter: DBAdapter):
        self.__drones: List[Drone] = []
        self.__db_adapter = db_adapter
        self.__log = []

    def get_drone_ids(self):
        """
        Returns all drones.

        :return: All drones.
        """
        return [drone.get_drone_id() for drone in self.__drones]

    def get_log(self):
        """
        Returns the log of drone state transitions.

        :return: The log of drone state transitions.
        """
        return self.__log

    def add_drone(self, drone):
        """
        Adds a drone to the list of drones.
        Sync with the DB.
        :param drone: The drone to add.
        """
        self.__drones.append(drone)
        self.__db_adapter.add_or_edit_drone(drone)

    def remove_drone(self, drone_id):
        """
        Removes a drone from the list of drones.
        Sync with the DB.
        :param drone: The drone to remove.
        """
        self.__drones.remove(self.get_drone_by_id(drone_id))
        self.__db_adapter.remove_drone_if_exists(drone_id)

    def refetch_drones_from_db(self):
        """
        Refetches all drones from the DB.
        """
        self.__drones = [Drone.from_sqlite(drone) for drone in self.__db_adapter.get_drones()]

    def get_available_drone_ids(self):
        """
        Returns all available drones.

        :return: All available drones.
        """
        return [drone.get_drone_id() for drone in self.__drones if drone.get_state() == Drone.AVAILABLE]

    def get_reserved_drone_ids(self):
        """
        Returns all reserved drones.

        :return: All reserved drones.
        """
        return [drone.get_drone_id() for drone in self.__drones if drone.get_state() == Drone.RESERVED]

    def get_maintenance_drone_ids(self):
        """
        Returns all maintenance drones.

        :return: All maintenance drones.
        """
        return [drone for drone in self.__drones if drone.get_state() == Drone.MAINTEINANCE]

    def get_drone_by_id(self, drone_id):
        """
        Returns a drone
        If not present raises an exception

        :param drone_id: The drone's ID.
        :return: The drone.
        """
        for drone in self.__drones:
            if drone.get_drone_id() == drone_id:
                return drone
        raise Exception("Drone with ID {} not found".format(drone_id))

    def __log_drone_state_change(self, drone_id, new_state):
        """
        Logs a drone state change.

        :param drone_id: The drone's ID.
        :param new_state: The new state.
        """
        self.__log.append((drone_id, new_state))

    def reserve_available_drone(self, drone_id = None) -> Tuple[str, str]:
        """
        Returns an available drone_id and the reservation token (uuid4).
        Sync changes with the database.
        If no drones are available, returns None.
        """
        if drone_id is None:
            drone_id = self.get_available_drone_ids()[0]
        drone = self.get_drone_by_id(drone_id)
        reservation_token = str(uuid4())
        drone.reserve(reservation_token)
        self.__log_drone_state_change(drone.get_drone_id(), Drone.RESERVED)
        self.__db_adapter.add_or_edit_drone(drone)
        return drone_id, drone.get_reservation_token()
    
    def assign_mission(self, drone_id, reservation_token, mission):
        """
        Assigns a mission to a drone.
        Only works if the drone is in RESERVED state.
        Changes its state accordingly.
        Sync changes with the database.
        """
        drone = self.get_drone_by_id(drone_id)
        if drone.get_reservation_token() != reservation_token:
            raise InvalidToken("Invalid reservation token")
        if drone.get_state() != Drone.RESERVED:
            raise WrongStateTransition("Drone is not in RESERVED state")
        drone.assign_mission(mission, reservation_token)
        self.__log_drone_state_change(drone.get_drone_id(), Drone.MISSION)
        self.__db_adapter.add_or_edit_drone(drone)

    def release_drone(self, drone_id, reservation_token):
        """
        Release a drone from reserved state (RESERVED -> AVAILABLE, MISSION -> AVAILABLE).
        Sync changes with the database.
        Changes its state accordingly.
        """
        # Check if drone is not in mainteinance, if not log a warning and return
        drone = self.get_drone_by_id(drone_id)

        # Do not allow transition if drone is in maintenance
        if drone.get_state() == Drone.MAINTEINANCE:
            raise WrongStateTransition("Drone is in maintenance")

        # Check if reservation token is valid
        if drone.get_reservation_token() != reservation_token:
            print("Reservation token {} is invalid".format(reservation_token))
            # Raise a state transition exception
            raise InvalidToken("Reservation token {} is invalid".format(reservation_token))

        # Change state
        drone.release_drone(reservation_token)
        self.__log_drone_state_change(drone.get_drone_id(), Drone.AVAILABLE)
        self.__db_adapter.add_or_edit_drone(drone)
        
    def put_drone_in_mainteinance(self, drone_id):
        """
        Puts a drone in mainteinance.
        Sync changes with the database.
        Changes its state accordingly.
        """
        # Check if drone is not in mainteinance, if not log a warning and return
        drone = self.get_drone_by_id(drone_id)
        if drone.get_state() != Drone.AVAILABLE:
            print("Drone {} is not available".format(drone_id))
            # Raise a state transition exception
            raise WrongStateTransition("Drone {} is not available".format(drone_id))

        # Change state
        drone.put_drone_in_mainteinance()
        self.__log_drone_state_change(drone.get_drone_id(), Drone.MAINTEINANCE)
        self.__db_adapter.add_or_edit_drone(drone)

    def take_drone_out_of_mainteinance(self, drone_id):
        """
        Takes a drone out of mainteinance.
        Sync changes with the database.
        Changes its state accordingly.
        """
        # Check if drone is not in mainteinance, if not log a warning and return
        drone = self.get_drone_by_id(drone_id)
        if drone.get_state() != Drone.MAINTEINANCE:
            print("Drone {} is not in mainteinance".format(drone_id))
            # Raise a state transition exception
            raise WrongStateTransition("Drone {} is not in mainteinance".format(drone_id))

        # Change state
        drone.set_state(Drone.AVAILABLE)
        self.__log_drone_state_change(drone.get_drone_id(), Drone.AVAILABLE)
        self.__db_adapter.add_or_edit_drone(drone)


    def pretty_print_state_changes(self):
        """
        Pretty prints the log of drone state changes.
        """
        for drone_id, new_state in self.__log:
            print("Drone {} changed state from {} to {}".format(drone_id, Drone.get_state_name(new_state), Drone.get_state_name(self.get_drone_by_id(drone_id).get_state())))
    
