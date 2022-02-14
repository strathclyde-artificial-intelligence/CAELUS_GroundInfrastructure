from abc import ABC

class Vendor(ABC):

    def get_vendor_id(self):
        raise NotImplementedError()