from GroundInfrastructure.DBAdapter import DBAdapter
from GroundInfrastructure.DroneStateManager import DroneStateManager
from GroundInfrastructure.Drone import Drone
from GroundInfrastructure.Mission import Mission
from GroundInfrastructure.Hospital import Hospital
from uuid import uuid4
import json 

# Create an in-memory databse
# then create a drone state manager
db_adapter = DBAdapter(':memory:')
drone_state_manager = DroneStateManager.from_sqlite(db_adapter)
# add 10 drones to the manager
drones = [Drone(uuid4(), Drone.TYPE_EVTOL_FW) for _ in range(10)]
for drone in drones:
    drone_state_manager.add_drone(drone)

# Check that db contains 10 drones
def test_db_contains_10_drones():
    assert len(drone_state_manager.get_available_drone_ids()) == 10

# Check if transitions are stored in the database
def test_transitions_are_stored_in_db():
    # Get the first drone
    drone = drone_state_manager.get_drone_by_id(drone_state_manager.get_available_drone_ids()[0])
    # Make two hospitals
    hospital1 = Hospital(uuid4(), 'Hospital1', [0.0, 0.0])
    hospital2 = Hospital(uuid4(), 'Hospital2', [0.0, 0.0])

    # Get the first mission
    mission = Mission(uuid4(), hospital1, hospital2)
    # Reserve the drone
    drone_id, reservation_token = drone_state_manager.reserve_available_drone(drone.get_drone_id())
    # Assign the drone to the mission
    drone_state_manager.assign_mission(drone.get_drone_id(), reservation_token, mission)
    # Refetch the drones 
    drone_state_manager.refetch_drones_from_db()
    # Check that the database reflects the current state of the drone
    assert drone_state_manager.get_drone_by_id(drone.get_drone_id()).get_state() == Drone.MISSION
    # Release the drone
    drone_state_manager.release_drone(drone.get_drone_id(), reservation_token)
    # Check that the database reflects the current state of the drone
    assert drone_state_manager.get_drone_by_id(drone.get_drone_id()).get_state() == Drone.AVAILABLE