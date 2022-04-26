import time
from unittest import mock
from GroundInfrastructure.Drone import Drone
from GroundInfrastructure.DroneStateManager import DroneStateManager
from uuid import uuid4
from GroundInfrastructure.DBAdapter import DBAdapter
from GroundInfrastructure.Mission import Mission
from GroundInfrastructure.SmartSkiesBridge import SmartSkiesBridge
from PySmartSkies.Models.JSONDeserialiser import JSONDeserialiser
from PySmartSkies.Credentials import DIS_Credentials
from GroundInfrastructure.AuthenticationManager import AuthenticationManager
import os
from dotenv import load_dotenv
import json
from tempfile import NamedTemporaryFile
from Orchestrator.api import OrchestratorAPI, Account

load_dotenv(".env.test")
load_dotenv('.env')

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
#drones = [Drone(uuid4(), Drone.TYPE_QUADROTOR, "config_0") for _ in range(10)]
#temporary_db = DBAdapter(":memory:")
temporary_db = DBAdapter("drones.db")

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

# fetch charging station list
charging_stations = bridge.get_charging_stations()

# Create a drone state manager
drone_state_manager = DroneStateManager(temporary_db)
smartskies_drones = bridge.get_all_available_drones()
for c,i in enumerate(smartskies_drones):
    if i.type_name=="Copter":
        drone_state_manager.add_drone(Drone(i.registration_number, Drone.TYPE_QUADROTOR, "x_quad_large.json", infrastructure_id=charging_stations[c%len(charging_stations)].get_id()))
    elif i.type_name=="FixedWing":
        drone_state_manager.add_drone(Drone(i.registration_number, Drone.TYPE_EVTOL_FW, "evtol_fw_large.json", infrastructure_id=charging_stations[c%len(charging_stations)].get_id()))
    else:
        print("Warning: unrecognised drone type " + i.type_name)

print("Charing Stations:")
for i in charging_stations:
    print('id=' + str(i.get_id()) + ' capacity=' + str(i.get_max_storing_capacity()) + ' ' + i.get_name())

print("Available drones:")
for i in drone_state_manager.get_available_drone_ids():
    d = drone_state_manager.get_drone_by_id(i)
    print("\t"+str(d))


try:

    while True:

        # wait
        time.sleep(10)

        # print current state of drones
        drone_state_manager.refetch_drones_from_db()
        print("Available drones:")
        for i in drone_state_manager.get_drone_ids():
            d = drone_state_manager.get_drone_by_id(i)
            print("\t"+str(d))

except KeyboardInterrupt:
    print('Closing Drone State Manager')