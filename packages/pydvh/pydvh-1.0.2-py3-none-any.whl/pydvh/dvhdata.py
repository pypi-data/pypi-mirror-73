from enum import Enum
import numpy as np


class DVHType(Enum):
    DDVH = 1
    CDVH = 2


class DVHData:
    def __init__(self, structure: str,
                 dvh_type: DVHType,
                 lower_dose: float,
                 upper_dose: float,
                 bin_width: float,
                 dose_array,
                 dose_unit,
                 volume_array,
                 volume_unit,
                 structure_volume=None):
        """

        :type bin_width: float
        :type upper_dose: float
        :type lower_dose: float
        :type dvh_type: DVHType -> DDVH, CDVH, None
        """
        self.structure_volume = structure_volume
        self.volume_unit = volume_unit
        self.dose_unit = dose_unit
        self.volume_array = volume_array
        self.dose_array = dose_array
        self._structure = structure
        self.bin_width = bin_width
        self.upper_dose = upper_dose + np.finfo(float).eps
        self.lower_dose = lower_dose
        self.dvh_type = dvh_type
        self.bin_number = int((upper_dose - lower_dose) / bin_width)
        self.overflow = 0.0
        self.underflow = 0.0
        self._total_volume = None

    def __repr__(self) -> str:
        return f"{self.dvh_type} for {self._structure}, Bins={self.bin_number}, " \
               f"Bin_width={self.bin_width}, structure_volume={self.structure_volume}"

    def _add_entry(self, dose, volume):
        if dose > self.upper_dose:
            self.overflow += volume
        if dose < self.lower_dose:
            self.lower_dose += volume

        # find bin position for the dose
        pos = self._find_position_for_dose(dose)

        # update the volume_array
        self.volume_array[pos] += volume

        # update total volume of structure
        self._total_volume += volume

    def _find_position_for_dose(self, dose):
        return int((dose - self.lower_dose) / self.bin_width)

    def curve(self):
        """A generator that returns tuples of (dose, volume). The dose is the mean value of 'bin'."""
        return zip(self.dose_array, self.volume_array)

    @property
    def total_volume(self):
        if self._total_volume is None:
            self._total_volume = np.sum(self.volume_array)
        return self._total_volume

    @property
    def structure_name(self):
        return self._structure

    @classmethod
    def from_dose_matrix(cls, dose_array: np.array, voxel_volume: float):
        pass

    @classmethod
    def from_DDVH_fixed_bin_width(cls,
                                  structure,
                                  dvh_type,
                                  dose_array: np.array,
                                  volume_array: np.array,
                                  dose_unit=None,
                                  volume_unit=None):
        # Guard checks
        cls._validate_array_or_raise_exception(dose_array, "dose_array must be an array of float numbers.")
        cls._validate_array_or_raise_exception(volume_array, "volume_array must be an array of float numbers.")
        if len(dose_array) != len(volume_array):
            raise ValueError('dose_array and volume_array must have the same length.')

        dose_array = np.array(dose_array)
        volume_array = np.array(volume_array)
        bin_width = np.round(np.mean(np.diff(dose_array)), 5)
        return cls(structure=structure,
                   dvh_type=dvh_type,
                   lower_dose=0.0,
                   upper_dose=np.max(dose_array) + (bin_width / 2.0),
                   bin_width=bin_width,
                   dose_array=dose_array,
                   volume_array=volume_array,
                   dose_unit=dose_unit,
                   volume_unit=volume_unit,
                   structure_volume=np.sum(volume_array)
                   )

    @classmethod
    def _validate_array_or_raise_exception(cls, varray, message):
        if not isinstance(varray, (np.ndarray, list)):
            raise ValueError(message)
