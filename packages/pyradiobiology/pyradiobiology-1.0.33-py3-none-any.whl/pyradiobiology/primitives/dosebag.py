import numpy as np
from .dose import *


class DoseBag():
    error = 1E-9

    def __init__(self, data, unit, dose_type=DoseType.PHYSICAL_DOSE, param_dict={}):
        self.unit = unit
        self.data = np.array(data)
        self.dose_type = dose_type
        self.param_dict = param_dict

    def __repr__(self) -> str:
        return f"data={self.data}, unit={self.unit}, dose_type={self.dose_type}"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, DoseBag):
            return False
        if o.unit != self.unit:
            return False
        if o.dose_type != self.dose_type:
            return False
        for v1, v2 in zip(o.data, self.data):
            if np.abs(v1 - v2) >= DoseBag.error:
                return False
        return True

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    @classmethod
    def create(cls, data=[], unit=DoseUnit.GY, dose_type=DoseType.PHYSICAL_DOSE, param_dict={}):
        return cls(data, unit, dose_type, param_dict)
