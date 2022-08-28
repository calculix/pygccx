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

from dataclasses import dataclass, field
from typing import Optional, Iterable, Any
import numpy as np
import numpy.typing as npt

from pygccx.enums import EPressureOverclosures
from pygccx.protocols import number
from pygccx.auxiliary import f2s

@dataclass
class SurfaceBehavior:
    """ 
    Class to define the surface behavior of a surface interaction.
    The surface behavior is required for a contact analysis.

    Args:
        pressure_overclosure: Option for pressure-overclosure
        c0: Mandatory for pressure_overclosure == EXPONENTIAL, optional for LINEAR and 
            node-to-face-contact, not used for LINEAR face-to-face-contact.

            For EXPONENTIAL: 
                Distance from the master surface at which the pressure is decreased to 1 % of p0.

            For LINEAR node-to-face-contact: 
                Distance factor from which the maximum clearance is calculated for which a spring 
                contact element is generated (by multiplying with the square root of the spring 
                area). Default value 10−3.
                
        p0: Mandatory for pressure_overclosure == EXPONENTIAL\n
            Contact pressure at zero distance

        k:bMandatory for pressure_overclosure == LINEAR and TIED\n
            Slope of the pressure-overclosure curve

        sig_inf: Mandatory for pressure_overclosure == LINEAR and node-to-face contact,
            not used for face-to-face contact.\n
            Tension value for large clearances

        table: Mandatory for pressure_overclosure == TABULAR\n
            Table with pressure - overclosure pairs in ascending order.

        name: Name of this instance

        desc: A short description of this instance. This is written to the ccx input file.
    """

    pressure_overclosure:EPressureOverclosures
    """Option for pressure-overclosure"""

    c0:Optional[number] = field(kw_only=True, default=None)
    """Mandatory for pressure_overclosure == EXPONENTIAL, optional for LINEAR and 
    node-to-face-contact, not used for LINEAR face-to-face-contact.

    For EXPONENTIAL: 
        Distance from the master surface at which the pressure is decreased to 1 % of p0.

    For LINEAR node-to-face-contact: 
        Distance factor from which the maximum clearance is calculated for which a spring 
        contact element is generated (by multiplying with the square root of the spring 
        area). Default value 10−3."""

    p0:Optional[number] = field(kw_only=True, default=None)
    """Mandatory for pressure_overclosure == EXPONENTIAL\n
    Contact pressure at zero distance"""

    k:Optional[number] = field(kw_only=True, default=None)
    """Mandatory for pressure_overclosure == LINEAR and TIED\n
    Slope of the pressure-overclosure curve"""

    sig_inf:Optional[number] = field(kw_only=True, default=None)
    """Mandatory for pressure_overclosure == LINEAR and node-to-face contact,
    not used for face-to-face contact.\n
    Tension value for large clearances"""

    table:Optional[Iterable[Iterable[number]]|npt.NDArray[np.float64]] = field(kw_only=True, default=None)
    """Mandatory for pressure_overclosure == TABULAR\n
    Table with pressure - overclosure pairs in ascending order."""

    name:str = ''
    """Name of this instance"""

    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    _is_initialized:bool = field(init=False, default=False)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        self._validate()

    def __post_init__(self):
        self._is_initialized = True

    def _validate(self):

        if not self._is_initialized: return 
        if self.pressure_overclosure == EPressureOverclosures.EXPONENTIAL:
            if self.c0 is None:
                raise ValueError(f'c0 must be specified for pressure_overclosure == EXPONENTIAL')
            if self.c0 <= 0:
                raise ValueError(f'c0 must be greater than 0, got {self.c0}')
            if self.p0 is None:
                raise ValueError(f'p0 must be specified for pressure_overclosure == EXPONENTIAL')
            if self.p0 <= 0:
                raise ValueError(f'p0 must be greater than 0, got {self.p0}')
        if self.pressure_overclosure == EPressureOverclosures.LINEAR:
            if self.k is None:
                raise ValueError(f'k must be specified for pressure_overclosure == LINEAR')
            if self.k <= 0:
                raise ValueError(f'k must be greater than 0, got {self.k}')
            if self.sig_inf is not None and self.sig_inf <= 0:
                raise ValueError(f'sig_inf must be greater than 0, got {self.sig_inf}')
            if self.c0 is not None and self.c0 <= 0:
                raise ValueError(f'c0 must be greater than 0, got {self.c0}')
        if self.pressure_overclosure == EPressureOverclosures.TABULAR:
            if self.table is None:
                raise ValueError(f'tabl must be specified for pressure_overclosure == TABULAR')
        if self.pressure_overclosure == EPressureOverclosures.TIED:
            if self.k is None:
                raise ValueError(f'k must be specified for pressure_overclosure == TIED')
            if self.k <= 0:
                raise ValueError(f'k must be greater than 0, got {self.k}')

    def __str__(self):

        s = f'*SURFACE BEHAVIOR,PRESSURE-OVERCLOSURE={self.pressure_overclosure.value}\n'

        if self.pressure_overclosure == EPressureOverclosures.EXPONENTIAL:
            s += f'{f2s(self.c0)},{f2s(self.p0)}\n'  # type: ignore , values can't be None because of validation

        if self.pressure_overclosure == EPressureOverclosures.LINEAR:
            s += f'{f2s(self.k)}'  # type: ignore
            if self.sig_inf is not None:
                s += f',{f2s(self.sig_inf)}'
            if self.c0 is not None:
                s += f',{f2s(self.c0)}'
            s += '\n'

        if self.pressure_overclosure == EPressureOverclosures.TABULAR and self.table:
            for row in self.table:
                s += ','.join(f'{f2s(x)}' for x in row) + '\n'

        if self.pressure_overclosure == EPressureOverclosures.TIED:
            s += f'{f2s(self.k)}\n'  # type: ignore

        return s
