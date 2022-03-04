import os
# load environment variables
from dotenv import load_dotenv
load_dotenv('.env.test')
from GroundInfrastructure.SmartSkiesBridge import SmartSkiesBridge
from GroundInfrastructure.Drone import Drone
from PySmartSkies.Credentials import DIS_Credentials, CVMS_Credentials
import pytest

latest_delivery_id = None

# Before all
@pytest.fixture(name="bridge")
def setup_module():
    global bridge
    # Create a session
    dis_credentials = DIS_Credentials(
        os.environ['DIS_GRANT_TYPE'],
        os.environ['DIS_CLIENT_ID'],
        os.environ['DIS_USERNAME'],
        os.environ['DIS_PASSWORD']
    )

    cvms_credentials = CVMS_Credentials(
        os.environ['CVMS_PHONE'],
        os.environ['CVMS_PASSWORD'],
        os.environ['CVMS_DEVICE_ID']
    )

    return SmartSkiesBridge(dis_credentials, cvms_credentials)

def test_get_all_available_drone_ids(bridge):
    assert len(bridge.get_all_available_drone_ids()) > 0

def test_get_hospitals(bridge):
    assert len(bridge.get_hospitals()) > 0

def test_get_products_for_vendor(bridge):
    # get a random hospital
    hospital = bridge.get_hospitals()[0]
    # get the products for the hospital
    products = bridge.get_products_for_vendor(hospital)
    assert len(products) > 0

def test_get_charging_stations(bridge):
    assert len(bridge.get_charging_stations()) > 0

def test_create_simple_mission(bridge: SmartSkiesBridge):
    global latest_delivery_id
    # get a viable drone ID
    drone_id = bridge.get_all_available_drone_ids()[0]
    # make a drone
    # TODO auto sync drone with SmartSkies drones
    drone = Drone(drone_id, Drone.TYPE_QUADROTOR, "config_0")
    # get a seller
    royal_informary_id = 48
    seller = [h for h in bridge.get_hospitals() if int(h.get_id()) == royal_informary_id][0]
    # get a product
    products = [bridge.get_products_for_vendor(seller)[0]]
    # create a mission
    mission = bridge.generate_mission(seller, drone, products)
    latest_delivery_id = mission.get_payload()['delivery_id']
    assert mission is not None
    
def test_cancel_simple_mission(bridge: SmartSkiesBridge):
    global latest_delivery_id
    # cancel the mission
    bridge.cancel_mission(latest_delivery_id)