from PySmartSkies.Credentials import DIS_Credentials, CVMS_Credentials
from PySmartSkies.Session import Session
from PySmartSkies.DIS_API import DIS_API
from PySmartSkies.CVMS_API import CVMS_API
from .Vendor import Vendor
from .ChargingStation import ChargingStation
from .Hospital import Hospital

class SmartSkiesBridge():

    def __init__(self, dis_credentials: DIS_Credentials, cvms_credentials: CVMS_Credentials, auth = True):
        """
        Initialises the SmartSkiesBridge.
        :param credentials: The credentials.
        """
        self.__session = Session(cvms_credentials, dis_credentials)
        self.__cvms_api = CVMS_API(self.__session)
        self.__dis_api = DIS_API(self.__session)
        self.__authenticated = False
        if auth:
            self.authenticate()

    def authenticate(self):
        if not self.__authenticated:
            self.__dis_api.authenticate()
            self.__cvms_api.authenticate()
            self.__authenticated = True

    def get_all_available_drone_ids(self):
        """
        Use the get_requested_deliveries method from the DIS_API
        to get the available drones (3rd return value)
        """
        return list(map(lambda drone: drone.registration_number, self.__dis_api.get_requested_deliveries()[2]))
    
    def get_products_for_vendor(self, vendor: Vendor):
        """
        Use the get_products_for_vendor_id method from the DIS_API
        to get the products for a given vendor id
        """
        return self.__cvms_api.get_product_list_from_vendor(vendor.get_vendor_id())

    def get_hospitals(self):
        """
        Use the get_hospitals method from the CVMS_API
        to get the hospitals
        """
        return [Hospital.from_smartskies_vendor(v) for v in  self.__cvms_api.get_vendor_list()]

    def get_charging_stations(self):
        """
        Use the get_charging_stations method from the CVMS_API
        to get the charging stations
        """
        return [ChargingStation.from_smartskies_vendor(v) for v in  self.__cvms_api.get_vendor_list() if v.location_text == 'new infrastructure']
