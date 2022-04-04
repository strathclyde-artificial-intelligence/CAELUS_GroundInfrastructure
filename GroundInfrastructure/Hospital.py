from .ChargingStation import ChargingStation
from .GroundInfrastructure import GroundInfrastructure
from .Vendor import Vendor
from PySmartSkies.Models.Vendor import Vendor as SmartSkiesVendor
import json

class Hospital(ChargingStation, Vendor):
    """
    A hospital.
    """
    @classmethod
    def from_json(cls, charging_station) -> 'ChargingStation':
        return super().from_json({"maxStorageCapacity": 0, "maxChargingCapacity": 0, **charging_station})
        
    def __init__(self, id, name, lonlat, address, max_storing_capacity = 0, max_charging_capacity = 0):
        super().__init__(str(id), name, lonlat, address, max_storing_capacity, max_charging_capacity)
    
    def get_type(self):
        return GroundInfrastructure.TYPE_HOSPITAL

    def to_json(self):
        return {
            **super().to_json(),
            "type": self.get_type()
        }

    def get_vendor_id(self):
        return self.get_id()

    def __repr__(self) -> str:
        return f'<Hospital|id={self.get_id()},name={self.get_name()},lonlat={self.get_lonlat()}>'
