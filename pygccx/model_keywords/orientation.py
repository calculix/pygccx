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

from pygccx.enums import EOrientationSystems, EOrientationRotAxis
from pygccx.protocols import ICoordinateSystem, number
from pygccx.auxiliary import f2s

@dataclass
class Orientation:

    """
    Class to specify a local axis system X'-Y'-Z' to be used for
    defining material properties.

    Args:
        name: Name of this Orientation
        pnt_a: First point to define the orientation in the form [x, y, z]
        pnt_b: Second point to define the orientation in the form [x, y, z]
        system: Optional. Type of the orientation system
        rot_axis: Optional. Axis for additional rotation (only if system == RECTANGULAR)
        rot_angle: Optional. Additional rotation angle about rot_axis (only if system == RECTANGULAR and rot_axis != NONE
        desc: Optional. A short description of this Instance. This is written to the ccx input file.
    """

    name:str  
    """Name of this Orientation"""
    pnt_a:Sequence[number]|np.ndarray
    """First point to define the orientation in the form [x, y, z]"""
    pnt_b:Sequence[number]|np.ndarray
    """Second point to define the orientation in the form [x, y, z]"""
    system: EOrientationSystems = EOrientationSystems.RECTANGULAR
    """Type of the orientation system"""
    rot_axis:EOrientationRotAxis = EOrientationRotAxis.NONE
    """Axis for additional rotation (only if system == RECTANGULAR)"""
    rot_angle:number = 0.
    """Additional rotation angle about rot_axis (only if system == RECTANGULAR and rot_axis != NONE"""
    desc:str = ''
    """A short description of this Instance. This is written to the ccx input file."""

    def __setattr__(self, name: str, value: Any) -> None:

        if name in ['pnt_a', 'pnt_b'] and len(value) != 3:
            raise ValueError(f'{name} must have exactly 3 elements, got {len(value)}')
        super().__setattr__(name, value)

    def __str__(self):
        s = f'*ORIENTATION,NAME={self.name},SYSTEM={self.system.value}\n'
        s += f'{",".join(map(f2s, self.pnt_a))},{",".join(map(f2s, self.pnt_b))}\n'
        if self.rot_axis != EOrientationRotAxis.NONE and self.system == EOrientationSystems.RECTANGULAR:
            s += f'{self.rot_axis.value},{f2s(self.rot_angle)}\n'

        return s

    @classmethod
    def from_coordinate_system(cls, cs:ICoordinateSystem):
        """
        Returns an Orientation object made from the given coordinate system.
        The name of the orientation is the name of the coordinate system prefixed with 'OR_'
        """

        mat = cs.get_matrix()
        ori = cs.get_origin()

        if cs.type == EOrientationSystems.RECTANGULAR:       
            pnt_a, pnt_b, _ = mat
        else:
            pnt_a, pnt_b = ori, ori + mat[2]

        return cls('OR_' + cs.name, pnt_a, pnt_b, system=cs.type)


        