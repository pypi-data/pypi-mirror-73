from enum import Enum
import numpy as np


class DVHType(Enum):
    DDVH = 1
    CDVH = 2


class DVHData:
    def __init__(self, structure: str,
                 dvh_type: DVHType,
                 min_dose,
                 max_dose,
                 bin_width,
                 dose_array,
                 dose_unit,
                 volume_array,
                 volume_unit,
                 structure_volume=None):
        """

        :type bin_width: float
        :type max_dose: float
        :type min_dose: float
        :type dvh_type: DVHType -> DDVH, CDVH, None
        """
        self.structure_volume = structure_volume
        self.volume_unit = volume_unit
        self.dose_unit = dose_unit
        self.volume_array = volume_array
        self.dose_array = dose_array
        self.structure = structure
        self.bin_width = bin_width
        self.max_dose = max_dose + np.finfo(float).eps
        self.min_dose = min_dose
        self.dvh_type = dvh_type
        self.bin_number = int((max_dose - min_dose) / bin_width)

    def __repr__(self) -> str:
        return f"{self.dvh_type} for {self.structure}, Bins={self.bin_number}, " \
               f"Bin_width={self.bin_width}, structure_volume={self.structure_volume}"

    @classmethod
    def from_dose_matrix(cls, dose_array: np.array, voxel_volume: float):
        pass

    @classmethod
    def from_dvh_file(cls, structure, dvh_type, dose_array: np.array, volume_array: np.array, dose_unit=None,
                      volume_unit=None, structure_volume=None):
        bin_width = np.round(np.mean(np.diff(dose_array)), 5)
        return cls(structure=structure,
                   dvh_type=dvh_type,
                   min_dose=0.0,
                   max_dose=np.max(dose_array),
                   bin_width=bin_width,
                   dose_array=dose_array,
                   volume_array=volume_array*bin_width,
                   dose_unit=dose_unit,
                   volume_unit=volume_unit,
                   structure_volume=structure_volume,
                   )
