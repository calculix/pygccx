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
from typing import Sequence, Any
import numpy as np
from protocols import ISet
from enums import EOrientationSystems, ESetTypes
from protocols import ICoordinateSystem, number

@dataclass
class Transform:

    """
    Class to specify a local axis system X'-Y'-Z' to be used for
    defining SPC's, MPC's and nodal force.

    Args:
        nset: Node set for which the transformation applies.
        pnt_a: First point to define the orientation in the form [x, y, z]
        pnt_b: Second point to define the orientation in the form [x, y, z]
        system: Optional. Type of the transformation system
        name: Optional. Name of this instance
        desc: Optional. A short description of this Instance. This is written to the ccx input file.
    """
    nset:ISet
    """Node set for which the transformation applies."""
    pnt_a:Sequence[number]|np.ndarray
    """First point to define the orientation in the form [x, y, z]"""
    pnt_b:Sequence[number]|np.ndarray
    """Second point to define the orientation in the form [x, y, z]"""
    system: EOrientationSystems = EOrientationSystems.RECTANGULAR
    """Type of the transformation system"""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this Instance. This is written to the ccx input file."""

    def __setattr__(self, name: str, value: Any) -> None:

        if name in ['pnt_a', 'pnt_b'] and len(value) != 3:
            raise ValueError(f'{name} must have exactly 3 elements, got {len(value)}')
        if name == 'nset' and value.type != ESetTypes.NODE:
            raise ValueError(f'Set type of {name} must be NODE, got {value.type.name}' )
        super().__setattr__(name, value)

    def __str__(self):
        s = f'*TRANSFORM,NSET={self.nset.name},TYPE={self.system.value[0]}\n'
        s += f'{",".join(map(str,self.pnt_a))},{",".join(map(str,self.pnt_b))}\n'


        return s

    @classmethod
    def from_coordinate_system(cls, nset:ISet, cs:ICoordinateSystem):
        """
        Returns a Transform object made from the given node set and coordinate system.
        """
        mat = cs.get_matrix()
        ori = cs.get_origin()

        if cs.type == EOrientationSystems.RECTANGULAR:       
            pnt_a, pnt_b, _ = mat
        else:
            pnt_a, pnt_b = ori, ori + mat[2]

        return cls(nset, pnt_a, pnt_b, system=cs.type)