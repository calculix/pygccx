'''
Copyright Matthias Sedlmaier 2024
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
from typing import Sequence, Any, Protocol
import numpy as np

from pygccx.enums import EOrientationSystems
from pygccx.protocols import ICoordinateSystem, number
from pygccx.auxiliary import f2s

@dataclass
class ITie(Protocol):
    name:str
    cyclic_symmetry:bool


@dataclass
class CyclicSymmetryModel:

    """
    Class to define the number of sectors and the axis of symmetry in a cyclic symmetric 
    structure for use in a cyclic symmetry calculation

    Args:
        n: Number of sectors
        tie: Tie constraint object to which the cyclic symmetry model definition applies      
        pnt_a: First point to define the axis of symmetry in the form [x, y, z]
        pnt_b: Second point to define the axis of symmetry in the form [x, y, z]
        check: Flag if CalculiX should compare the sector angle based on its geometry with its value based on.
        name: Optional. Name of this instance. Not used.
        desc: Optional. A short description of this Instance. This is written to the ccx input file.
    """

    n:int  
    """Number of sectors"""
    tie:ITie
    """Tie constraint object to which the cyclic symmetry model definition applies"""
    pnt_a:Sequence[number]|np.ndarray
    """First point to define the axis of symmetry in the form [x, y, z]"""
    pnt_b:Sequence[number]|np.ndarray
    """Second point to define the axis of symmetry in the form [x, y, z]"""
    check:bool = True
    """Flag if CalculiX should compare the sector angle based on its geometry 
    with its value based on."""
    name:str  = ''
    """Name of this instance. Not used."""
    desc:str = ''
    """A short description of this Instance. This is written to the ccx input file."""

    def __setattr__(self, name: str, value: Any) -> None:

        if name == 'n' and value < 1:
            raise ValueError(f'{name} must be greater or equal than 1, got {value}')
        if name == 'tie':
            tie:ITie = value
            if not tie.cyclic_symmetry:
                raise ValueError(f'{name} must be a cyclic symmetry tie with tie.cyclic_symmetry == True')
        if name in ['pnt_a', 'pnt_b'] and len(value) != 3:
            raise ValueError(f'{name} must have exactly 3 elements, got {len(value)}')
        super().__setattr__(name, value)

    def __str__(self):
        s = f'*CYCLIC SYMMETRY MODEL,N={self.n},TIE={self.tie.name}'
        if not self.check: s += ',CHECK=NO'
        s += '\n'

        s += f'{",".join(map(f2s, self.pnt_a))},{",".join(map(f2s, self.pnt_b))}\n'

        return s

    @classmethod
    def from_coordinate_system(cls, n:int, tie:ITie, cs:ICoordinateSystem, check:bool=True, name:str='', desc:str=''):
        """        
        Returns an CyclicSymmetryModel object made from the given coordinate system.
        Instead of providing two points, a and b, a cylindrical coordinate system is used.

        Args:
            n (int): Number of sectors
            tie (Tie): Tie constraint object to which the cyclic symmetry model definition applies
            check (bool): Specifies whether CalculiX should compare the sector angle based on its geometry with its value based on.
            cs (ICoordinateSystem): Cylindrical coordinate system. Z-axis is axis of symmetry.
            name (str, optional): Name of the returned instance. Not used.
            desc (str, optional): A short description of this Instance. This is written to the ccx input file.

        Raises:
            ValueError: Raised if coordinate system is not cylindrical  

        Returns:
            CyclicSymmetryModel
        """
        if cs.type != EOrientationSystems.CYLINDRICAL:
            raise ValueError(f'cs must be of type {EOrientationSystems.CYLINDRICAL.name}, got {cs.type.name}')
        
        mat = cs.get_matrix()
        ori = cs.get_origin()

        pnt_a, pnt_b = ori, ori + mat[2]

        return cls(n, tie, pnt_a, pnt_b, check, name, desc)