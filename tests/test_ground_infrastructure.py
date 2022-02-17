import json
from GroundInfrastructure.GroundInfrastructure import GroundInfrastructure
from GroundInfrastructure.Hospital import Hospital
from GroundInfrastructure.ChargingStation import ChargingStation
from GroundInfrastructure.GroundInfrastructureHelpers import ground_infrastructure_from_json

def test_load_hospital_from_json():
    json_str = '{"id": "1", "name": "Hospital 1", "location_long": 1.0, "location_lat": 2.0, "address":"some_address", "type": 4}'
    json_obj = json.loads(json_str)
    hospital = Hospital.from_json(json_obj)
    assert hospital is not None

def test_load_charging_station_from_json():
    json_str = '{"id": "1", "name": "Charging Station 1", "location_long": 1.0, "location_lat": 2.0, "type": 3, "address":"some_address", "max_storing_capacity":100, "max_charging_capacity":100}'
    json_obj = json.loads(json_str)
    charging_station = ChargingStation.from_json(json_obj)
    assert charging_station is not None

def test_load_hospital_using_ground_infrastructure_from_json():
    json_str = '{"id": "1", "name": "Hospital 1", "location_long": 1.0, "location_lat": 2.0, "address":"some_address", "type": 4}'
    json_obj = json.loads(json_str)
    ground_infrastructure = ground_infrastructure_from_json(json_obj)
    assert ground_infrastructure is not None
    assert isinstance(ground_infrastructure, Hospital)
    assert ground_infrastructure.get_id() == '1'
    assert ground_infrastructure.get_name() == 'Hospital 1'
    assert ground_infrastructure.get_type() == GroundInfrastructure.TYPE_HOSPITAL
    assert ground_infrastructure.get_lonlat() == [1.0, 2.0]

def test_load_charging_station_using_ground_infrastructure_from_json():
    json_str = '{"id": "1", "name": "Charging Station 1", "location_long": 1.0, "location_lat": 2.0, "type": 3, "address":"some_address", "max_storing_capacity":100, "max_charging_capacity":100}'
    json_obj = json.loads(json_str)
    ground_infrastructure = ground_infrastructure_from_json(json_obj)
    assert ground_infrastructure is not None
    assert isinstance(ground_infrastructure, ChargingStation)
    assert ground_infrastructure.get_id() == '1'
    assert ground_infrastructure.get_name() == 'Charging Station 1'
    assert ground_infrastructure.get_type() == GroundInfrastructure.TYPE_CHARGING_STATION
    assert ground_infrastructure.get_lonlat() == [1.0, 2.0]