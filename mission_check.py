from unittest import mock

from matplotlib.font_manager import json_load
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

api = OrchestratorAPI(os.environ['ORCHESTRATOR_API_URL'])
account = api.authenticate('new_user', 'test')
jobs = api.get_activated_jobs(account=account)

jobs = json.loads(jobs.content)
for job in jobs:
    print(job['mission_payload']['operation_id'])
    print(job['status_str'])