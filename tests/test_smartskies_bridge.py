import os
# load environment variables
from dotenv import load_dotenv
load_dotenv('.env.test')
from GroundInfrastructure.SmartSkiesBridge import SmartSkiesBridge
from PySmartSkies.Credentials import DIS_Credentials, CVMS_Credentials
import pytest

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
