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

from dataclasses import dataclass
from typing import Sequence, Optional, Any
import numpy as np
import numpy.typing as npt

from protocols import ISet, number
from enums import ESetTypes

@dataclass
class Gap:
    """
    Class to define a gap geometry.

    Args:
        elset: Set of gap elements to which the geometry definition applies
        clearance: Gap clearance
        direction:  Normalized direction vector of gap
        k: Optional. Spring stiffness in force/length
        f_inf: Optional. Tension spring force at infinite distance
        name: Optional. The name of this instance
        desc: Optional. A short description of this instance. This is written to the ccx input file.
    """

    elset:ISet
    """Set of gap elements to which the geometry definition applies"""
    clearance:number
    """Gap clearance"""
    direction: Sequence[number]|npt.NDArray[np.float64]
    """Normalized direction vector of gap"""
    k:Optional[number] = None
    """Spring stiffness in force/length"""
    f_inf:Optional[number] = None
    """Tension spring force at infinite distance"""
    name:str = ''
    """The name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    def __setattr__(self, name: str, value: Any) -> None:
        if name == 'elset' and value.type != ESetTypes.ELEMENT:
            raise ValueError(f'Set type of elset must be ELEMENT, got {value.type.name}')
        if name == 'direction':
            if len(value) != 3:
                raise ValueError(f'Length of direction must be 3, got {len(value)}')
            d = np.linalg.norm(np.array(value))
            if not np.isclose(d, 1):
                raise ValueError(f'Norm of direction must be 1., got {d}')
        if name in ('k', 'f_inf') and value is not None and value <= 0:
            raise ValueError(f'{name} must be > 0, got {value}')

        super().__setattr__(name, value)

    def __str__(self):
        s = f'*GAP,ELSET={self.elset.name}\n'
        nx, ny, nz = self.direction
        s += f'{self.clearance:.7e},{nx:.7e},{ny:.7e},{nz:.7e},'

        s += f',{self.k:.7e}' if self.k is not None else ','
        s += f',{self.f_inf:.7e}' if self.f_inf is not None else ','
        
        return s.rstrip(',') + '\n'