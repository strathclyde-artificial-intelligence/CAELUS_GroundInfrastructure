from unittest import mock
from GroundInfrastructure.Drone import Drone
from GroundInfrastructure.DroneStateManager import DroneStateManager
from uuid import uuid4
from GroundInfrastructure.DBAdapter import DBAdapter
from GroundInfrastructure.Mission import Mission
from GroundInfrastructure.SmartSkiesBridge import SmartSkiesBridge
from PySmartSkies.Credentials import DIS_Credentials
from GroundInfrastructure.AuthenticationManager import AuthenticationManager
import os
from dotenv import load_dotenv
import json
from tempfile import NamedTemporaryFile

load_dotenv(".env.test")

def temporary_credentials_file():
    data = [
        {
            "name": "customer1",
            "lonlat": [1.0, 1.0],
            "phone": os.environ['CVMS_PHONE'],
            "password": os.environ['CVMS_PASSWORD'],
            "device_id": os.environ['CVMS_DEVICE_ID']
        },
        {
            "name": "customer2",
            "lonlat": [1.0, 1.0],
            "phone": os.environ['CVMS_PHONE'],
            "password": os.environ['CVMS_PASSWORD'],
            "device_id": os.environ['CVMS_DEVICE_ID']
        }
    ]
    # temporary file for testing
    mock_credentials = NamedTemporaryFile(mode='w+', delete=False)
    mock_credentials.write(json.dumps(data))
    mock_credentials.seek(0)
    return mock_credentials

# Create a list of drones with UUID4s
drones = [Drone(uuid4(), Drone.TYPE_QUADROTOR, "config_0") for _ in range(10)]
temporary_db = DBAdapter(":memory:")

dis_credentials = DIS_Credentials(
    os.environ['DIS_GRANT_TYPE'],
    os.environ['DIS_CLIENT_ID'],
    os.environ['DIS_USERNAME'],
    os.environ['DIS_PASSWORD']
)

auth_manager = AuthenticationManager(
    temporary_credentials_file().name,
    dis_credentials
)

# get a bridge for a customer
bridge = auth_manager.get_bridge_for_customer("customer1")

# Create a drone state manager
drone_state_manager = DroneStateManager(temporary_db)
smartskies_drone_ids = bridge.get_all_available_drone_ids()
for i in smartskies_drone_ids:
    drone_state_manager.add_drone(Drone(i))

print(drone_state_manager.get_available_drone_ids())


