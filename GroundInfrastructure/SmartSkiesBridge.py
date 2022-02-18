import datetime
import time
from uuid import uuid4
import json
import geopy.distance

from typing import List
from PySmartSkies.Credentials import DIS_Credentials, CVMS_Credentials
from PySmartSkies.Session import Session
from PySmartSkies.DIS_API import DIS_API
from PySmartSkies.CVMS_API import CVMS_API
from PySmartSkies.Models.Product import Product as SmartSkiesProduct
from PySmartSkies.Models.Drone import Drone as SmartSkiesDrone
from PySmartSkies.Models.Operation import Operation as SmartSkiesOperation

from .Mission import Mission
from .Drone import Drone
from .Vendor import Vendor
from .ChargingStation import ChargingStation
from .Hospital import Hospital
from .GroundInfrastructure import GroundInfrastructure

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

    def find_ground_infrastructure_by_location(self, lonlat: List[float]) -> GroundInfrastructure:
        """
        Use the get_charging_stations method from the CVMS_API
        to get the charging stations
        """
        hospitals_and_charging_stations = self.get_hospitals() + self.get_charging_stations()
        hospitals_and_charging_stations = sorted(hospitals_and_charging_stations, key=lambda h: geopy.distance.distance(h.get_lonlat(), lonlat).m)
        return hospitals_and_charging_stations[0]
        
    def get_products_for_vendor(self, vendor: Vendor) -> List[SmartSkiesProduct]:
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
        return [ChargingStation.from_smartskies_vendor(v) for v in self.__cvms_api.get_vendor_list() if hasattr(v, 'location_text') and v.location_text == 'new infrastructure']

    def generate_mission(self,
        seller: GroundInfrastructure,
        drone: Drone,
        products: List[SmartSkiesProduct],
        mission_starts_at_unix: str = str(time.time()),
        group_id: str = str(uuid4())) -> Mission:

        # Place an order for the products
        orders = self.__cvms_api.place_order(seller.to_smartskies_vendor(), products)
        self.__cvms_api.checkout_orders(orders)
        deliveries, _, smartskies_drones, control_areas = self.__dis_api.get_requested_deliveries()
        
        if len(deliveries) == 0:
            raise Exception('Smartskies failed in creating delivery. Hospitals may be too far apart!')

        chosen_drone = [d for d in smartskies_drones if d.registration_number == drone.get_drone_id()]
        if len(chosen_drone) == 0:
            raise Exception('Failed in creating delivery. Smartskies has no drone with id {} found'.format(drone.get_drone_id()))
        chosen_drone = chosen_drone[0]
        
        # round to nearest second 
        effective_time_begin = datetime.datetime.fromtimestamp(int(mission_starts_at_unix.split('.')[0]))
        effective_time_begin += datetime.timedelta(minutes=1)

        payload_mass = sum(map(lambda product: product.per_item_weight, products))
        drone_config_file = drone.get_config_name()
        group_id = group_id if group_id is not None and group_id != "" else str(uuid4())

        ops = self.__dis_api.create_operation(deliveries[-1], chosen_drone, control_areas[-1], effective_time_begin.isoformat())
        op_details = self.__dis_api.get_operation_details_with_delivery_id(deliveries[-1].id)
        op: SmartSkiesOperation = ops[0]
        wps = op.get_waypoints()
    
        # Takeoff location must be rounded up / increased slightly
        # To prevent collision of the drone with the bottom of the
        # takeoff volume
        initial_lon_lat_alt_corrected = list(op.get_takeoff_location())
        initial_lon_lat_alt_corrected[-1] += 0.5
        # --------

        payload = {
            'waypoints': wps,
            "operation_id": op_details.operation_id,
            "control_area_id": control_areas[-1].control_area_id,
            "operation_reference_number": ops[-1].reference_number,
            "drone_id": chosen_drone.drone_id,
            "drone_registration_number": chosen_drone.registration_number,
            "dis_auth_token": self.__dis_api._session.get_dis_token(),
            "dis_refresh_token": self.__dis_api._session.get_dis_refresh_token(),
            "cvms_auth_token": self.__dis_api._session.get_cvms_token(),
            "delivery_id": deliveries[-1].id,
            "thermal_model_timestep": 1,
            "aeroacoustic_model_timestep": 0.004,
            "drone_config_file":drone_config_file,
            "payload_mass":payload_mass,
            "g_acceleration": 9.81,
            "group_id":group_id,
            "effective_start_time": mission_starts_at_unix,
            "initial_lon_lat_alt": initial_lon_lat_alt_corrected,
            "final_lon_lat_alt":op.get_landing_location()
        }

        return Mission(
            op_details.operation_id,
            self.find_ground_infrastructure_by_location(initial_lon_lat_alt_corrected[:-1]),
            seller,
            payload)

    def cancel_mission(self, delivery_id):
        def verb_for_operation_close(status):
            if status in ['Activated', "Non-Conforming", "Contingent"]:
                return 'End'
            else:
                return 'Cancel'
        try:
            self.__dis_api.abort_delivery(delivery_id)
            operation = self.__dis_api.get_operation_details_with_delivery_id(delivery_id)
            if operation is not None:
                verb = verb_for_operation_close(operation.state)
                self.__dis_api.end_or_close_delivery(delivery_id, verb)
        except Exception as e:
            print(f'Failed to cancel mission with id {delivery_id}')
            print(e)