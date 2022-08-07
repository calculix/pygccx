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
from typing import Optional, Any
from enums import ESetTypes
from protocols import IKeyword, ISet

@dataclass
class SolidSection:
    """
    Class to assign material properties to 3D, plane stress, plane
    strain, axisymmetric and truss element set

    Args:
        elset: Element set where this solid section should be applied to.
        material: Material object which should be applies to elset.
        orientation: Optional. Orientation system for material.
        name: Optional. The name of this Instance. Not used.
        desc: Optional. A short description of this Instance. This is written to the ccx input file.

    """
    elset:ISet
    """Element set where this solid section should be applied to."""
    material:IKeyword
    """Material object which should be applies to elset"""
    orientation:Optional[IKeyword] = None
    """Orientation system for material"""
    name:str = ''
    """The name of this Instance. Not used"""
    desc:str = ''
    """A short description of this Instance. This is written to the ccx input file."""

    def __setattr__(self, name: str, value: Any) -> None:

        if name == "elset" and value.type != ESetTypes.ELEMENT:
            raise ValueError(f'type of elset must be ELEMENT, got {value.type}')
        super().__setattr__(name, value)

    def __str__(self):
        s = f'*SOLID SECTION,MATERIAL={self.material.name},ELSET={self.elset.name}'
        s += f',ORIENTATION={self.orientation.name}\n' if self.orientation else '\n'
        return s