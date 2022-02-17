from .GroundInfrastructure import GroundInfrastructure
from .Vendor import Vendor
from PySmartSkies.Models.Vendor import Vendor as SmartSkiesVendor
import json

class Hospital(GroundInfrastructure, Vendor):
    """
    A hospital.
    """
    
    @staticmethod
    def from_json(hospital):
        return Hospital(hospital['id'], hospital['name'], [hospital['location_long'], hospital['location_lat']], hospital['address'])

    @staticmethod
    def from_smartskies_vendor(vendor: SmartSkiesVendor):
        """
        Creates a hospital from a smart skies vendor.
        :param vendor: The smart skies vendor.
        :return: The hospital.
        """
        return Hospital(vendor.vendor_id, vendor.name, [vendor.location_long, vendor.location_lat], vendor.address)

    def __init__(self, id, name, lonlat, address):
        super().__init__(str(id), name, lonlat, address, GroundInfrastructure.TYPE_HOSPITAL)

    def to_json(self):
        return {
            **super().to_json(),
            "type": self.get_type()
        }

    def get_vendor_id(self):
        return self.get_id()

    def __repr__(self) -> str:
        return f'<Hospital|id={self.get_id()},name={self.get_name()},lonlat={self.get_lonlat()}>'
