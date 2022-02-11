from PySmartSkies.Credentials import DIS_Credentials
from PySmartSkies.Session import Session
from PySmartSkies.DIS_API import DIS_API

class SmartSkiesBridge():

    def __init__(self, credentials: DIS_Credentials):
        """
        Initialises the SmartSkiesBridge.
        :param credentials: The credentials.
        """
        self.__credentials = credentials
        self.__session = Session(None, self.__credentials)
        self.__dis_api = DIS_API(self.__session)
        self.__dis_api.authenticate()

    def get_all_available_drone_ids(self):
        """
        Use the get_requested_deliveries method from the DIS_API
        to get the available drones (3rd return value)
        """
        return list(map(lambda drone: drone.registration_number, self.__dis_api.get_requested_deliveries()[2]))

