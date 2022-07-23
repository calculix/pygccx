from dataclasses import dataclass, field
from enums import EHardeningRules
from typing import Sequence
import numpy as np
import numpy.typing as npt

number = int|float

@dataclass(frozen=True, slots=True)
class CyclicHardening:
    """
    Class to define the isotropic hardening curve of a material when in
    the Plastic object hardening == EHardeningRules.COMBINED is selected

    The plastic stress and strain for the first temperature have to be provided
    to the init of this class. Further sets to define temperature dependance
    can be added by the method add_plastic_params_for_temp()

    Args:
        stress: Sequence of mises stresses for first temperature. Must be same 
                length as strain
        strain: Sequence of equ. plastic srains for first temperature. Must be 
                same length as stress
        temp: temperature of first stress-strain table
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to 
                the ccx input file.

    """

    stress:Sequence[number]|npt.NDArray[np.float64]
    """Sequence of mises stresses for first temperature. Must be same length as strain"""
    strain:Sequence[number]|npt.NDArray[np.float64]
    """Sequence of equ. plastic srains for first temperature. Must be same length as stress"""
    temp:number = 294.
    """temperature of first stress-strain table"""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    _plastic_params_for_temps:list = field(default_factory=list, init=False)

    def __post_init__(self):
        self.add_plastic_stress_strain_for_temp(self.temp, self.stress,self.strain)


    def add_plastic_stress_strain_for_temp(self, temp:number, stress:Sequence[number]|npt.NDArray[np.float64], strain:Sequence[number]|npt.NDArray[np.float64]): 
        """
        Adds a table of plastic stress and strain for a given temperature.

        Args:
            temp (number): temperature for this 
            stress (Sequence[number]|npt.NDArray[np.float64]): Sequence of mises stresses. Must be same length as strain
            strain (Sequence[number]|npt.NDArray[np.float64]): Sequence of equ. plastic srains. Must be same length as stress

        Raises:
            ValueError: Raised if stress and strain have different lengths.
        """

        if len(stress) != len(strain):
            raise ValueError(f"stress and srain must have equal length.")
        self._plastic_params_for_temps.append((temp, stress, strain))


    def __str__(self):

        s = f'*CYCLIC HARDENING\n'

        for p in self._plastic_params_for_temps:
            temp, stress, strain = p
            for s_, e_ in zip(stress, strain):
                s += f'{s_:15.7e},{e_:15.7e},{temp:15.7e}\n' 
        
        return s


@dataclass(frozen=True, slots=True)
class Plastic(CyclicHardening):

    """
    Class to define the plastic properties of a material

    The plastic stress and strain for the first temperature have to be provided
    to the init of this class. Further sets to define temperature dependance
    can be added by the method add_plastic_params_for_temp()

    Args:
        stress: Sequence of mises stresses for first temperature. Must be same 
                length as strain
        strain: Sequence of equ. plastic srains for first temperature. Must be 
                same length as stress
        temp: temperature of first stress-strain table
        hardening: Optional. Hardening rule
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to 
                the ccx input file.

    """

    hardening:EHardeningRules = EHardeningRules.ISOTROPIC  
    """Hardening rule"""

    def __str__(self):

        s = f'*PLASTIC'
        if self.hardening != EHardeningRules.ISOTROPIC:
            s += f',HARDENING={self.hardening.value}'
        s += '\n'

        for p in self._plastic_params_for_temps:
            temp, stress, strain = p
            for s_, e_ in zip(stress, strain):
                s += f'{s_:15.7e},{e_:15.7e},{temp:15.7e}\n' 
        
        return s
