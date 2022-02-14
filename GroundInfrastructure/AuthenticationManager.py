import json
from .SmartSkiesBridge import SmartSkiesBridge
from PySmartSkies.Credentials import CVMS_Credentials, DIS_Credentials

class AuthenticationManager():

    def __init__(self, customer_credentials_file: str, dis_credentials: DIS_Credentials):
        self.__credentials_file = customer_credentials_file
        self.__dis_credentials: DIS_Credentials = dis_credentials
        self.__bridges = {}
        self.__load_credentials_file()

    def __load_credentials_file(self):
        """
            Load credentials from file and parse them
            Credentials are stored in a json object
            with schema
            [
             {
                name: str
                lonlat: [float]
                phone: str
                password: str
                device_id: str
             }
            ]
        """
        with open(self.__credentials_file, 'r') as f:
            credentials = json.loads(f.read())
        
        # Store credentials with name being their key
        # and map the credentials to a CVMS_Credentials object
        self.__credentials = {}
        for credential in credentials:
            self.__credentials[credential['name']] = CVMS_Credentials(credential['phone'], credential['password'], credential['device_id'])

    def get_bridge_for_customer(self, customer_name: str) -> SmartSkiesBridge:
        """
            Return a SmartSkiesBridge for the given customer
        """
        if customer_name not in self.__credentials:
            raise ValueError('Customer not found')
        bridge = SmartSkiesBridge(self.__dis_credentials, self.__credentials[customer_name])
        bridge.authenticate()
        self.__bridges[customer_name] = bridge
        return bridge
    
    def get_available_customers(self) -> list:
        """
            Return a list of available customers
        """
        return list(self.__credentials.keys())