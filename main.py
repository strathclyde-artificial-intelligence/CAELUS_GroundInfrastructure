from GroundInfrastructure.Drone import Drone
from GroundInfrastructure.DroneStateManager import DroneStateManager
from uuid import uuid4
from GroundInfrastructure.DBAdapter import DBAdapter
from GroundInfrastructure.Mission import Mission
from GroundInfrastructure.SmartSkiesBridge import SmartSkiesBridge
from PySmartSkies.Credentials import DIS_Credentials
import os
from dotenv import load_dotenv
load_dotenv(".env.test")

# Create a list of drones with UUID4s
drones = [Drone(uuid4()) for _ in range(10)]
temporary_db = DBAdapter('./test.sqlite')

dis_credentials = DIS_Credentials(
    os.environ['DIS_GRANT_TYPE'],
    os.environ['DIS_CLIENT_ID'],
    os.environ['DIS_USERNAME'],
    os.environ['DIS_PASSWORD']
)

smartskies_bridge = SmartSkiesBridge(dis_credentials)

# Create a drone state manager
drone_state_manager = DroneStateManager(temporary_db)
smartskies_drone_ids = smartskies_bridge.get_all_available_drone_ids()
for i in smartskies_drone_ids:
    drone_state_manager.add_drone(Drone(i))

print(drone_state_manager.get_available_drone_ids())


