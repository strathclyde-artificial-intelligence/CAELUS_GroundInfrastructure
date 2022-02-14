from .GroundInfrastructure import GroundInfrastructure
from .Vendor import Vendor
from PySmartSkies.Models.Vendor import Vendor as SmartSkiesVendor

class Hospital(GroundInfrastructure, Vendor):
    """
    A hospital.
    """
    
    @staticmethod
    def from_smartskies_vendor(vendor: SmartSkiesVendor):
        """
        Creates a hospital from a smart skies vendor.
        :param vendor: The smart skies vendor.
        :return: The hospital.
        """
        return Hospital(vendor.vendor_id, vendor.name, [vendor.location_long, vendor.location_lat])

    def __init__(self, id, name, lonlat):
        super().__init__(id, name, lonlat, GroundInfrastructure.TYPE_HOSPITAL)

    def get_vendor_id(self):
        return self.get_id()

    def __repr__(self) -> str:
        return f'<Hospital|id={self.get_id()},name={self.get_name()},lonlat={self.get_lonlat()}>'
