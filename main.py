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
from requests import Response

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
drone_state_manager.refetch_drones_from_db()

## ========================== ## 
## Testing from this point on ##
## ========================== ## 

print("Reserving available done")
#drone_id = drone_state_manager.get_available_drone_ids()[0]
drone_id, reservation_token = drone_state_manager.reserve_available_drone()
assert reservation_token is not None
print(reservation_token)

print("creating a mission")
#drone_id = bridge.get_all_available_drone_ids()[1]
drone = drone_state_manager.get_drone_by_id(drone_id)
royal_informary_id = 48
seller = [h for h in bridge.get_hospitals() if int(h.get_id()) == royal_informary_id][0]
products = [bridge.get_products_for_vendor(seller)[0]]
mission = bridge.generate_mission(seller, drone, products)
latest_delivery_id = mission.get_payload()['delivery_id']
assert mission is not None

print("seller: " + str(seller))
print("drone: " + str(drone))
print("mission: " + str(mission.get_origin()) + ' ' + str(mission.get_destination()) + ' ' + str(mission.get_payload()))

print("Assigning mission to drone.")
drone_state_manager.assign_mission(drone_id, reservation_token, mission)
drone = drone_state_manager.get_drone_by_id(drone_id)
print("drone: " + str(drone))

print("Simulating mission through the orchestrator.")
api = OrchestratorAPI(os.environ['ORCHESTRATOR_API_URL'])
account = api.authenticate('new_user', 'test')
response = api.schedule_new_mission(mission.get_payload(), account=account)
if 'job_id' in response:
    latest_job_id = response['job_id']
else:
    latest_job_id = None
print("Started with job_id: " + str(latest_job_id))

print("Waiting for mission to complete.")
print("\tMission: " + str(mission.get_operation_id()))
while True:

    time.sleep(10)

    jobs = json.loads(api.get_activated_jobs(account=account).content)
    current_mission = [ j for j in jobs if str(j['mission_payload']['operation_id'])==str(mission.get_operation_id()) ]
    if len(current_mission)==1 and "HALTED" in current_mission[0]['status_str']:
        print ("mission halted.")
        print("\toperation_id: " + current_mission[0]['mission_payload']['operation_id'])
        print("\tstatus: " + str(urrent_mission[0]['status']))
        print("\tstatus: " + current_mission[0]['status_str'])
        break
    if len(current_mission)==1 and "ERROR" in current_mission[0]['status_str']:
        print ("mission finished with error.")
        print("\toperation_id: " + str(current_mission[0]['mission_payload']['operation_id']))
        print("\tstatus: " + str(current_mission[0]['status']))
        print("\tstatus: " + str(current_mission[0]['status_str']))
        break
    elif len(current_mission)==1:
        print("Waiting for mission to complete.")
        print("\toperation_id: " + current_mission[0]['mission_payload']['operation_id'])
        print("\tstatus: " + current_mission[0]['status_str'])
    else:
        print("Waiting for mission to complete.")
        print("\toperation_id: " + current_mission[0]['mission_payload']['operation_id'])
        print("Mission not found:")
        for j in jobs:
            print("\t" + j['mission_payload']['operation_id'])


print("Releasing drone.")
drone_state_manager.release_drone(drone_id, reservation_token)
drone = drone_state_manager.get_drone_by_id(drone_id)
print(drone)
