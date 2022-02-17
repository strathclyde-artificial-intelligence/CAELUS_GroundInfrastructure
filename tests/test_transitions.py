import pytest
from GroundInfrastructure.DroneStateManager import DroneStateManager
from GroundInfrastructure.Drone import Drone
from GroundInfrastructure.DBAdapter import MockDBAdapter

# Before all unit tests, generate a global drone state manager
# and populate it with 10 drones.
@pytest.fixture(scope='session')
def drone_state_manager():
    from GroundInfrastructure.Drone import Drone
    from GroundInfrastructure.DroneStateManager import DroneStateManager
    from uuid import uuid4

    # Create a list of drones with UUID4s
    drones = [Drone(uuid4(), Drone.TYPE_QUADROTOR, "config_0") for _ in range(10)]

    # Create a mock database adapter
    db_adapter = MockDBAdapter()
    # Create a drone state manager
    drone_state_manager = DroneStateManager.from_sqlite(db_adapter)

    # add drones to the manager
    for drone in drones:
        drone_state_manager.add_drone(drone)

    return drone_state_manager

# Check that anyone can reserve an available drone
# make sure that the reservation token is returned
# make sure the number of total drones is the same after reservation
# make sure the number of available drones is one lower after reservation
def test_reserve_available_drone(drone_state_manager):
    drone_id = drone_state_manager.get_available_drone_ids()[0]
    reservation_token = drone_state_manager.reserve_available_drone(drone_id)
    assert reservation_token is not None
    assert len(drone_state_manager.get_available_drone_ids()) == 9
    assert len(drone_state_manager.get_reserved_drone_ids()) == 1

# Check that a reserved drone can't be assigned a mission without a reservation token
def test_assign_mission_to_reserved_drone_without_reservation_token(drone_state_manager):
    drone_id = drone_state_manager.get_reserved_drone_ids()[0]
    with pytest.raises(Exception):
        drone_state_manager.assign_mission_to_drone(drone_id, 'reservation_token', 'mission_token')

# Check that releasing a drone without a reservation token raises an exception
def test_release_drone_without_reservation_token(drone_state_manager):
    drone_id = drone_state_manager.get_reserved_drone_ids()[0]
    with pytest.raises(Exception):
        drone_state_manager.release_drone(drone_id, 'reservation_token')

# Check that releasing a drone with the right token works
def test_release_drone_with_right_reservation_token(drone_state_manager):
    drone_id = drone_state_manager.get_reserved_drone_ids()[0]
    reservation_token = drone_state_manager.get_drone_by_id(drone_id).get_reservation_token()
    drone_state_manager.release_drone(drone_id, reservation_token)
    assert drone_state_manager.get_drone_by_id(drone_id).get_state() == Drone.AVAILABLE

# Check that after state transitions the log is updated
def test_log_drone_state_change(drone_state_manager):
    drone_id, reservation_token = drone_state_manager.reserve_available_drone()
    drone_state_manager.release_drone(drone_id, reservation_token)
    assert drone_state_manager.get_drone_by_id(drone_id).get_state() == Drone.AVAILABLE
    assert drone_state_manager.get_log()[-1] == (drone_id, Drone.AVAILABLE)

# Check that after a drone transitions away from MISSION, the mission details are cleared
def test_clear_mission_details_after_drone_transitions_away_from_mission(drone_state_manager):
    drone_id, reservation_token = drone_state_manager.reserve_available_drone()
    drone_state_manager.assign_mission(drone_id, reservation_token, 'mission_token')
    assert drone_state_manager.get_drone_by_id(drone_id).get_mission() is not None
    drone_state_manager.release_drone(drone_id, reservation_token)
    assert drone_state_manager.get_drone_by_id(drone_id).get_mission() is None

# Check that after a drone transitions away from MISSION, the release token is cleared
def test_clear_release_token_after_drone_transitions_away_from_mission(drone_state_manager):
    drone_id, reservation_token = drone_state_manager.reserve_available_drone()
    drone_state_manager.assign_mission(drone_id, reservation_token, 'mission_token')
    assert drone_state_manager.get_drone_by_id(drone_id).get_reservation_token() is not None
    drone_state_manager.release_drone(drone_id, reservation_token)
    assert drone_state_manager.get_drone_by_id(drone_id).get_reservation_token() is None
