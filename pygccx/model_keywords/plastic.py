'''
Copyright Matthias Sedlmaier 2022
This file is part of pygccx.

pygccx is free software: you can redistribute it 
and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

pygccx is distributed in the hope that it will 
be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pygccx.  
If not, see <http://www.gnu.org/licenses/>.
'''

from dataclasses import dataclass, field, InitVar
from typing import Sequence
import numpy as np
import numpy.typing as npt

from enums import EHardeningRules
from protocols import number
from auxiliary import f2s

@dataclass
class CyclicHardening:
    """
    Class to define the isotropic hardening curve of a material when in
    the Plastic object hardening == EHardeningRules.COMBINED is selected

    The plastic stress and strain for the first temperature have to be provided
    to the init of this class. Further sets to define temperature dependence
    can be added by the method add_plastic_params_for_temp()

    Args:
        stress: Sequence of mises stresses for first temperature. Must be same 
                length as strain
        strain: Sequence of equ. plastic strains for first temperature. Must be 
                same length as stress
        temp: temperature of first stress-strain table
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to 
                the ccx input file.

    """

    stress:InitVar[Sequence[number]|npt.NDArray[np.float64]]
    """Sequence of mises stresses for first temperature. Must be same length as strain"""
    strain:InitVar[Sequence[number]|npt.NDArray[np.float64]]
    """Sequence of equ. plastic strains for first temperature. Must be same length as stress"""
    temp:InitVar[number] = 294.
    """temperature of first stress-strain table"""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    plastic_params_for_temps:list = field(default_factory=list, init=False)

    def __post_init__(self, stress, strain, temp):
        self.add_plastic_stress_strain_for_temp(temp, stress, strain)


    def add_plastic_stress_strain_for_temp(self, temp:number, stress:Sequence[number]|npt.NDArray[np.float64], strain:Sequence[number]|npt.NDArray[np.float64]): 
        """
        Adds a table of plastic stress and strain for a given temperature.

        Args:
            temp (number): temperature for this table
            stress (Sequence[number]|npt.NDArray[np.float64]): Sequence of mises stresses. Must be same length as strain
            strain (Sequence[number]|npt.NDArray[np.float64]): Sequence of equ. plastic strains. Must be same length as stress

        Raises:
            ValueError: Raised if stress and strain have different lengths.
        """

        if len(stress) != len(strain):
            raise ValueError(f"stress and strain must have equal length.")
        self.plastic_params_for_temps.append((temp, stress, strain))


    def __str__(self):

        s = f'*CYCLIC HARDENING\n'

        for p in self.plastic_params_for_temps:
            temp, stress, strain = p
            for s_, e_ in zip(stress, strain):
                s += f'{f2s(s_)},{f2s(e_)},{f2s(temp)}\n' 
        
        return s


@dataclass
class Plastic(CyclicHardening):

    """
    Class to define the plastic properties of a material

    The plastic stress and strain for the first temperature have to be provided
    to the init of this class. Further sets to define temperature dependence
    can be added by the method add_plastic_params_for_temp()

    Args:
        stress: Sequence of mises stresses for first temperature. Must be same 
                length as strain
        strain: Sequence of equ. plastic strains for first temperature. Must be 
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

        for p in self.plastic_params_for_temps:
            temp, stress, strain = p
            for s_, e_ in zip(stress, strain):
                s += f'{f2s(s_)},{f2s(e_)},{f2s(temp)}\n' 
        
        return s
