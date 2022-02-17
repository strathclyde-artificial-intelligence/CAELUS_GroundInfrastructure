from unittest import mock
from GroundInfrastructure.AuthenticationManager import AuthenticationManager
from tempfile import NamedTemporaryFile
from PySmartSkies.Credentials import DIS_Credentials, CVMS_Credentials
import json
import os
from dotenv import load_dotenv
import pytest

load_dotenv('.env.test')

data = [
    {
        "name": "customer1",
        "phone": os.environ['CVMS_PHONE'],
        "password": os.environ['CVMS_PASSWORD'],
        "device_id": os.environ['CVMS_DEVICE_ID']
    },
    {
        "name": "customer2",
        "phone": os.environ['CVMS_PHONE'],
        "password": os.environ['CVMS_PASSWORD'],
        "device_id": os.environ['CVMS_DEVICE_ID']
    }
]

dis_credentials = DIS_Credentials(
    os.environ['DIS_GRANT_TYPE'],
    os.environ['DIS_CLIENT_ID'],
    os.environ['DIS_USERNAME'],
    os.environ['DIS_PASSWORD']
)

# temporary file for testing
mock_credentials = NamedTemporaryFile(mode='w+')
mock_credentials.write(json.dumps(data))
mock_credentials.seek(0)

def test_load():
    AuthenticationManager(mock_credentials.name, dis_credentials)

def test_get_bridge_for_customer():
    manager = AuthenticationManager(mock_credentials.name, dis_credentials)
    assert manager.get_bridge_for_customer('customer1')
    assert manager.get_bridge_for_customer('customer2')
    # assert ValueException is raised when customer not found
    with pytest.raises(ValueError):
        manager.get_bridge_for_customer('customer3')

# test that there are a total of 2 customers
def test_get_customers():
    manager = AuthenticationManager(mock_credentials.name, dis_credentials)
    assert manager.get_available_customers() == ["customer1", "customer2"]
