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

temporary_db = DBAdapter("drones.db")

# Create a drone state manager
drone_state_manager = DroneStateManager(temporary_db)

print("Available drones:")
drone_state_manager.refetch_drones_from_db()
for i in drone_state_manager.get_drone_ids():
    d = drone_state_manager.get_drone_by_id(i)
    print("\t"+str(d))