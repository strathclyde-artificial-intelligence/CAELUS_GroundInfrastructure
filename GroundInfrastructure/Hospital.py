from .GroundInfrastructure import GroundInfrastructure
from .Vendor import Vendor
from PySmartSkies.Models.Vendor import Vendor as SmartSkiesVendor
import json

class Hospital(GroundInfrastructure, Vendor):
    """
    A hospital.
    """
    
    @staticmethod
    def from_json(json_string):
        hospital = json.loads(json_string)
        return Hospital(hospital['id'], hospital['name'], [hospital['lon'], hospital['lat']])

    @staticmethod
    def from_smartskies_vendor(vendor: SmartSkiesVendor):
        """
        Creates a hospital from a smart skies vendor.
        :param vendor: The smart skies vendor.
        :return: The hospital.
        """
        return Hospital(vendor.vendor_id, vendor.name, [vendor.location_long, vendor.location_lat])

    def __init__(self, id, name, lonlat):
        super().__init__(str(id), name, lonlat, GroundInfrastructure.TYPE_HOSPITAL)

    def to_json(self) -> str:
        return json.dumps({"id": self.get_id(), "name": self.get_name(), "lon": self.get_lonlat()[0], "lat": self.get_lonlat()[1], "type": self.get_type()})

    def get_vendor_id(self):
        return self.get_id()

    def __repr__(self) -> str:
        return f'<Hospital|id={self.get_id()},name={self.get_name()},lonlat={self.get_lonlat()}>'
